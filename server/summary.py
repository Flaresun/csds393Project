from rake_nltk import Rake
from nltk.corpus import stopwords
import nltk 
nltk.download('punkt_tab')  # Note: This may be a typo. Common usage is 'punkt'.
nltk.download('stopwords')
import string
import database
from collections import defaultdict

# ------------------------------------------------------------
# Extracts top keyphrases from a single comment using RAKE.
# This version uses default stopwords and removes most punctuation.
# Suitable for natural language comments where common words are noise.
# ------------------------------------------------------------
def top_keyphrases_from_comment(comment, top_n):
    rake = Rake()
    rake.extract_keywords_from_text(comment)
    return rake.get_ranked_phrases_with_scores()[:top_n]  # returns top_n (score, phrase) tuples

# ------------------------------------------------------------
# Extracts top keyphrases from a technical note using RAKE.
# Preserves technical punctuation like "+", "-", "*", "(", ")".
# Uses NLTK's standard English stopwords for filtering.
# Suitable for structured text where symbols are meaningful.
# ------------------------------------------------------------
def top_keyphrases_from_note(note, top_n):
    custom_punct = string.punctuation.replace('+', '').replace('-', '').replace('*', '').replace('(', '').replace(')', '')
    custom_stopwords = set(stopwords.words('english'))

    rake = Rake(stopwords=custom_stopwords, punctuations=custom_punct)
    rake.extract_keywords_from_text(note)
    return rake.get_ranked_phrases_with_scores()[:top_n]  # returns top_n (score, phrase) tuples

# ------------------------------------------------------------
# Normalizes overlapping keyphrases by grouping shorter and longer versions.
# Ensures phrases like "deep learning" and "deep learning model" are grouped.
# Returns a mapping: normalized_phrase -> list of (score, original_phrase) tuples.
# ------------------------------------------------------------
def normalize_phrases(ranked_phrases):
    phrases = sorted(ranked_phrases, key=lambda x: len(x[1]))  # sort by phrase length
    normalized_map = defaultdict(list)

    for score, phrase in phrases:
        matched = False
        for norm_phrase in normalized_map:
            if phrase in norm_phrase:
                # Replace shorter norm_phrase with longer current phrase
                normalized_map[phrase].extend(normalized_map.pop(norm_phrase))
                normalized_map[phrase].append((score, phrase))
                matched = True
                break
            elif norm_phrase in phrase:
                # Append to existing normalized phrase
                normalized_map[norm_phrase].append((score, phrase))
                matched = True
                break

        if not matched:
            # Add new normalized phrase group
            normalized_map[phrase].append((score, phrase))

    return normalized_map

# ------------------------------------------------------------
# Async function to compute top keyphrases from all comments of a note.
# Combines all comment keywords, normalizes similar phrases, and scores them.
# Final ranking is by frequency and average RAKE score.
# ------------------------------------------------------------
async def get_top_keyphrases_from_note_comments(db_conn_pool, note_id, top_n=3):
    comments = await database.get_comments_for_note(db_conn_pool, note_id)

    all_ranked = []
    for comment in comments:
        all_ranked.extend(top_keyphrases_from_comment(comment.content, 10))  # Top 10 from each comment

    normalized = normalize_phrases(all_ranked)

    # Compute frequency and average score per normalized phrase
    phrase_stats = []
    for phrase, instances in normalized.items():
        count = len(instances)
        avg_score = sum(score for score, _ in instances) / count
        phrase_stats.append((phrase, count, avg_score))

    # Sort by frequency (desc) and then by average score (desc)
    phrase_stats.sort(key=lambda x: (-x[1], -x[2]))

    return [phrase for phrase, _, _ in phrase_stats[:top_n]]

# ------------------------------------------------------------
# Async function to compute top keyphrases from the note content itself.
# Similar to the comment version, but only analyzes the note text.
# Decodes binary data, normalizes phrases, and ranks by frequency and score.
# ------------------------------------------------------------
async def get_top_keyphrases_from_note(db_conn_pool, note_id, top_n=3):
    note = await database.get_note(db_conn_pool, note_id)
    note_text = note.content.decode('utf-8')  # Decode binary content into string

    ranked_phrases = top_keyphrases_from_note(note_text, 10)
    normalized_map = normalize_phrases(ranked_phrases)

    # Score normalized phrases by frequency and max RAKE score
    phrase_data = []
    for norm_phrase, occurrences in normalized_map.items():
        frequency = len(occurrences)
        max_score = max(score for score, _ in occurrences)
        phrase_data.append((frequency, max_score, norm_phrase))

    # Sort by frequency (desc), then max score (desc)
    phrase_data.sort(key=lambda x: (-x[0], -x[1]))

    return [phrase for _, _, phrase in phrase_data[:top_n]]
