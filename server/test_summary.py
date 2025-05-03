import pytest
import summary
from unittest.mock import AsyncMock, patch
from collections import namedtuple

Note = namedtuple("Note", ["note_id", "section_id", "owner_id", "content", "content_type"])
Comment = namedtuple("Comment", ["content"])


@pytest.mark.asyncio
async def test_get_top_keyphrases_from_note_comments():
    """
    Test keyphrase extraction from a list of comments associated with a note:
    - Mocks comments containing repeated and unique keyphrases.
    - Verifies that the top extracted keyphrases reflect frequency and relevance.
    """
    mock_db_pool = AsyncMock()
    comments = [
        Comment("Dynamic programming is great."),
        Comment("Greedy algorithms can be tricky."),
        Comment("Dynamic programming saves time.")
    ]

    with patch("database.get_comments_for_note", return_value=comments):
        result = await summary.get_top_keyphrases_from_note_comments(mock_db_pool, note_id=1, top_n=3)

    assert "dynamic programming" in result
    assert "greedy" in result or "greedy algorithms" in result


@pytest.mark.asyncio
async def test_get_top_keyphrases_from_note():
    """
    Test keyphrase extraction from the binary content of a note:
    - Mocks a note containing multiple algorithm descriptions.
    - Checks that top keyphrases reflect the main concepts like binary search, merge sort, and hash tables.
    """
    mock_db_pool = AsyncMock()
    note_text = (
        "Binary search is an efficient algorithm for finding an element in a sorted list. "
        "Binary search repeatedly divides the search space in half. "
        "Merge sort is a divide-and-conquer algorithm. "
        "Merge sort divides the list, sorts each half, and merges them. "
        "Hash tables are useful for fast lookups. "
        "Hash tables use a hash function to map keys to values."
    )

    # in get_keyphrases_from_note, the note content is in binary
    note_binary = note_text.encode("utf-8")

    note = Note(1, 1, 1, note_binary, "text")

    with patch("database.get_note", return_value=note):
        result = await summary.get_top_keyphrases_from_note(mock_db_pool, note_id=1, top_n=3)

    assert "binary search" in result
    assert "merge sort" in result
    assert "hash tables" in result


def test_extract_keywords_from_commment():
    """
    Test keyphrase extraction directly from a comment string:
    - Prints the top 3 keyphrases extracted from a realistic comment about AI and data analysis.
    """
    comment = ("AI and machine learning are changing the world. Companies are using them to analyze data and make "
               "predictions.")

    print(summary.top_keyphrases_from_comment(comment, 3))


def test_extract_keywords_from_note():
    """
    Test keyphrase extraction directly from a raw note string:
    - Prints the top 3 keyphrases from a note summarizing core algorithm techniques.
    """
    note = (
        'basic algorithm techniques \n brute force: trying every possible combination until you find the solution \n '
        'divide and conquer: split task into pieces, solve on each piece, merge piece solutions into a total solution \n greedy: at each step, make the locally optimal choice \n dynamic programming: consider sub-problems, solve on each, combine to a global solution \n use a recurrence relation to define the algorithm \n will need to prove that we can combine optimal sub-solutions into a global solution \n each piece might be used many times in finding solution \n store solution to each sub-problem in a table so we can reuse it')

    print(summary.top_keyphrases_from_note(note, 3))
