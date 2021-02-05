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
    row: List[str], col: int, agg_col: List[int], key: Tuple[str, str], d: SortedDict
) -> SortedDict:
    next = base_word(row[col])
    if col == agg_col[-1]:
        val = row[3]
        if next in d:
            if key not in d[next]:
                d[next][key] = SortedList()
            d[next][key].add(val)
        else:
            d[next] = SortedDict(ord_tuple, {key: SortedList([val])})
    else:
        if next not in d:
            d[next] = SortedDict(ord_word)
        d[next] = _agg_lemma(row, agg_col[agg_col.index(col) + 1], agg_col, key, d[next])
    return d


def aggregate(
    corpus: List[List[str]], word_col: int, trans_col: int, lem_col: List[int]
) -> SortedDict:
    result = SortedDict(ord_word)
    for row in corpus:
        if not row[3]:
            continue
        key = (base_word(row[word_col]), base_word(row[trans_col]))
        result = _agg_lemma(row, lem_col[0], lem_col, key, result)
    return result
