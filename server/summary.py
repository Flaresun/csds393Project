from rake_nltk import Rake
from nltk.corpus import stopwords
import string
import database
from collections import defaultdict


# uses default stopwords and punctuation removal, since they shouldn't be important in comments
def top_keyphrases_from_comment(comment, top_n):
    rake = Rake()
    rake.extract_keywords_from_text(comment)
    return rake.get_ranked_phrases_with_scores()[:top_n]  # returns a list of (score, phrase)

# preserves punctuation marks like "+", "-", ",", etc., which are more important in technical documents like notes
def top_keyphrases_from_note(note, top_n):
    custom_punct = string.punctuation.replace('+', '').replace('-', '').replace('*', '').replace('(', '').replace(')', '')
    custom_stopwords = set(stopwords.words('english'))

    rake = Rake(stopwords=custom_stopwords, punctuations=custom_punct)
    rake.extract_keywords_from_text(note)
    return rake.get_ranked_phrases_with_scores()[:top_n] # returns a list of (score, phrase)

"""
replaces longer phrases in the list with shorter ones if one is a substring of the other.
returns a mapping from normalized phrase -> list of (original_score, original_phrase)
"""
def normalize_phrases(ranked_phrases):
    phrases = sorted(ranked_phrases, key=lambda x: len(x[1]))
    normalized_map = defaultdict(list)

    for score, phrase in phrases:
        matched = False
        for norm_phrase in normalized_map:
            if phrase in norm_phrase:
                # merges current (longer) phrase into the shorter one
                normalized_map[phrase].extend(normalized_map.pop(norm_phrase))
                normalized_map[phrase].append((score, phrase))
                matched = True
                break
            elif norm_phrase in phrase:
                normalized_map[norm_phrase].append((score, phrase))
                matched = True
                break

        if not matched:
            normalized_map[phrase].append((score, phrase))

    return normalized_map

async def get_top_keyphrases_from_note_comments(db_conn_pool, note_id, top_n=3):
    comments = await database.get_comments_for_note(db_conn_pool, note_id)

    all_ranked = []
    for comment in comments:
        all_ranked.extend(top_keyphrases_from_comment(comment.content, 10))

    # merges phrases
    normalized = normalize_phrases(all_ranked)

    # scores phrases by count and average RAKE relevance
    phrase_stats = []
    for phrase, instances in normalized.items():
        count = len(instances)
        avg_score = sum(score for score, _ in instances) / count
        phrase_stats.append((phrase, count, avg_score))

    # sorts by count descending, then avg RAKE score descending
    phrase_stats.sort(key=lambda x: (-x[1], -x[2]))

    return [phrase for phrase, _, _ in phrase_stats[:top_n]]

async def get_top_keyphrases_from_note(db_conn_pool, note_id, top_n=3):
    note = await database.get_note(db_conn_pool, note_id)
    note_text = note.content.decode('utf-8') # decodes the note content since it is stored in binary

    ranked_phrases = top_keyphrases_from_note(note_text, 10)
    normalized_map = normalize_phrases(ranked_phrases)

    # counts frequency of normalized phrases, uses max score to break ties
    phrase_data = []
    for norm_phrase, occurrences in normalized_map.items():
        frequency = len(occurrences)
        max_score = max(score for score, _ in occurrences)
        phrase_data.append((frequency, max_score, norm_phrase))

    # sorts by frequency descending, then score descending
    phrase_data.sort(key=lambda x: (-x[0], -x[1]))

    return [phrase for _, _, phrase in phrase_data[:top_n]]