#!/usr/bin/env python3

from typing import List, Tuple
import unicodedata
from sortedcontainers import SortedDict, SortedList, SortedSet  # type: ignore

# from model import Usage
from util import ord_word, base_word

ord_tuple = lambda x: ord_word(x[0])


def merge(
    corpus: List[List[str]], word_col: int, lem_col: List[int], tr_col: int, tr_lem_col: List[int]
) -> List[List[str]]:
    """Merge lines according to distribution of =. This is an asymmetric operation

    Args:
        corpus (List[List[str]]): original corpus
        sl_word (str): word
        gr_slem (List[str]): translation lemmas

    Returns:
        List[List[str]]: merged corpus
    """
    result: List[List[str]] = []
    for row in corpus:
        if row[word_col] == "=":
            row[3] = result[-1][3]
            row[word_col] = result[-1][word_col]
            row[lem_col[0]] = result[-1][lem_col[0]]
            result[-1][tr_col] = result[-1][tr_col] + " " + row[tr_col]
            row[tr_col] = result[-1][tr_col]
            for col in tr_lem_col[1:]:
                if result[-1][col]:
                    if row[col] and row[col] != "=":
                        result[-1][col] = result[-1][col] + " " + row[col]
                    row[col] = result[-1][col]

        result.append(row)
    return result


def extract_letters(corpus: List[List[str]], col: int) -> SortedSet:
    letters = SortedSet()
    for row in corpus:
        if row[col]:
            letters = letters.union(
                [ch for ch in unicodedata.normalize("NFKC", row[col].lower())]
            )
            # letters = letters.union([ch for ch in row[col].lower()])
    return {l: ord(l) for l in letters}


def _agg_lemma(
    row: List[str],
    col: int,
    lem_col: List[int],
    tlem_col: List[int],
    key: Tuple[str, str],
    d: SortedDict,
) -> SortedDict:
    """Adds a lemma. Recursion ensures that this works with variable depth.

    Args:
        row (List[str]): spreadsheet row
        col (int): lemma column being currently processed
        lem_col (List[int]): all lemma columns in original language
        tlem_col (List[int]): translation lemma columns
        key (Tuple[str, str]): word pair
        d (SortedDict): see return value

    Returns:
        SortedDict: *IN PLACE* hierarchical dictionary
    """
    if col == -1:
        cols = [base_word(row[c]) for c in tlem_col if row[c]]
        cols.reverse()
        next = "→".join(cols)
        # include style in index string
        val = f"{row[3]}~{row[16]}"
        if next in d:
            if key not in d[next]:
                d[next][key] = SortedList()
            d[next][key].add(val)
        else:
            d[next] = SortedDict(ord_tuple, {key: SortedList([val])})
    else:
        next = base_word(row[col])
        if next not in d:
            d[next] = SortedDict(ord_word)
        next_idx = lem_col.index(col) + 1
        next_col = lem_col[next_idx] if next_idx < len(lem_col) else -1
        d[next] = _agg_lemma(row, next_col, lem_col, tlem_col, key, d[next])

    return d


def aggregate(
    corpus: List[List[str]],
    word_col: int,
    trans_col: int,
    lem_col: List[int],
    tlem_col: List[int],
) -> SortedDict:
    """Generate an aggregated index of translations. Recursion ensures that this works with variable depth.

    Args:
        corpus (List[List[str]]): input spreadsheet
        word_col (int): word column
        trans_col (int): translation word column
        lem_col (List[int]): lemma columns
        tlem_col (List[int]): translation lemma columns

    Returns:
        SortedDict: hierarchical dictionary of all lemma levels in original language, that contains rows of the form: translation_lemma: word/tword (index)
    """
    result = SortedDict(ord_word)
    for row in corpus:
        if not row[3]:
            continue
        key = (base_word(row[word_col]), base_word(row[trans_col]))
        result = _agg_lemma(row, lem_col[0], lem_col, tlem_col, key, result)
    return result
