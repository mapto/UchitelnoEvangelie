#!/usr/bin/env python3

from typing import List, Tuple
import unicodedata
from sortedcontainers import SortedDict, SortedList, SortedSet  # type: ignore

# from model import Usage
from util import ord_word, base_word

ord_tuple = lambda x: ord_word(x[0])


def merge(corpus: List[List[str]]) -> List[List[str]]:
    result: List[List[str]] = []
    for row in corpus:
        presence = [e for e in row if e == "="]
        if presence:
            for col in range(len(row)):
                if row[col] and row[col] != "=":
                    if result[-1][col]:
                        result[-1][col] += " " + row[col]
                    else:
                        result[-1][col] = row[col]
        else:
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
    row: List[str], col: int, lem_col: List[int], tlem_col: List[int], key: Tuple[str, str], d: SortedDict
) -> SortedDict:
    if col == lem_col[-1]:
        val = row[3]
        cols = [base_word(row[col]) for col in tlem_col if row[col]]
        cols.reverse()
        next = "→".join(cols)
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
        d[next] = _agg_lemma(row, lem_col[lem_col.index(col) + 1], lem_col, tlem_col, key, d[next])
    return d


def aggregate(
    corpus: List[List[str]], word_col: int, trans_col: int, lem_col: List[int], tlem_col: List[int]
) -> SortedDict:
    """Generate an aggregated index of translations

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
