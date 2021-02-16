#!/usr/bin/env python3

from typing import List, Tuple
import unicodedata
from sortedcontainers import SortedDict, SortedList, SortedSet  # type: ignore
import re

from model import Index, LangSemantics
from util import ord_word, base_word

ord_tuple = lambda x: ord_word(x[0])


def expand_idx(corpus: List[List[str]]) -> List[List[str]]:
    """*IN_PLACE*"""
    for row in corpus:
        if row[3]:
            row[3] = Index.unpack(row[3]).longstr()
    return corpus


def _present(word: str) -> bool:
    return not not word and word.strip().lower()[:2] != "om"


def merge(
    corpus: List[List[str]], orig: LangSemantics, trans: LangSemantics
) -> List[List[str]]:
    """Merge lines according to distribution of =. This is an asymmetric operation

    Args:
        corpus (List[List[str]]): original corpus
        sl_word (str): word
        gr_slem (List[str]): translation lemmas

    Returns:
        List[List[str]]: merged corpus
    """
    word_col = orig.word
    lem_col = orig.lemmas
    tr_col = trans.word
    tr_lem_col = trans.lemmas

    result: List[List[str]] = []
    for old_row in corpus:
        row = [v if v else "" for v in old_row]
        if row[word_col] == "=":
            row[word_col] = result[-1][word_col]
            # if not row[tr_lem_col[0]]:
            result[-1][tr_col] = result[-1][tr_col] + " " + row[tr_col]
            if row[tr_lem_col[0]]:
                result[-1][tr_lem_col[0]] = (
                    result[-1][tr_lem_col[0]] + " & " + row[tr_lem_col[0]]
                )
            for col in tr_lem_col[1:]:
                if not row[col]:
                    continue
                if row[col] == "=":
                    row[tr_lem_col[0]] = result[-1][tr_lem_col[0]]
                else:
                    result[-1][col] = result[-1][col] + " " + row[col]
                row[col] = result[-1][col]
            for col in lem_col[1:]:
                if row[col] == "=":
                    row[col] = result[-1][col]

        else:
            if row[tr_col] == "=":
                result[-1][word_col] = result[-1][word_col] + " " + row[word_col]
                row[word_col] = result[-1][word_col]
                row[tr_col] = result[-1][tr_col]
                if row[tr_lem_col[0]]:
                    result[-1][tr_lem_col[0]] = (
                        result[-1][tr_lem_col[0]] + " & " + row[tr_lem_col[0]]
                    )
                row[tr_lem_col[0]] = result[-1][tr_lem_col[0]]
            for col in tr_lem_col[1:]:
                if row[col] == "=":
                    row[col] = result[-1][col]
            for col in lem_col[1:]:
                if row[col] == "=":
                    row[col] = result[-1][col]
            # result.append(row)

        if not row[tr_col] or row[tr_col] == "=":
            row[tr_col] = result[-1][tr_col]
        if not row[3]:
            row[3] = result[-1][3]
        if _present(row[lem_col[0]]) and _present(row[word_col]):
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
        cols = [base_word(row[c]) for c in tlem_col]
        cols.reverse()
        empty = True
        while empty:
            if not cols[0]:
                cols.pop(0)
                # if not len(cols):
                # print(row)
                # TODO: Might need to be removed
                empty = len(cols) > 0  # empty = False
            else:
                empty = False
        next = "→ ".join(cols)

        val = Index.unpack(row[3])
        val.bold = "bold" in row[16]
        val.italic = "italic" in row[16]
        if next in d:
            if key not in d[next]:
                d[next][key] = SortedList()
            d[next][key].add(val)
        else:
            d[next] = SortedDict(ord_tuple, {key: SortedList([val])})

    else:
        lemmas = row[col].split("&") if row[col] else [""]
        for l in lemmas:
            next = base_word(l)
            if next not in d:
                d[next] = SortedDict(ord_word)
            next_idx = lem_col.index(col) + 1
            next_col = lem_col[next_idx] if next_idx < len(lem_col) else -1
            d[next] = _agg_lemma(row, next_col, lem_col, tlem_col, key, d[next])

    return d


def aggregate(
    corpus: List[List[str]], orig: LangSemantics, trans: LangSemantics
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
    word_col = orig.word
    lem_col = orig.lemmas
    trans_col = trans.word
    tlem_col = trans.lemmas

    result = SortedDict(ord_word)
    for row in corpus:
        if not row[3]:
            continue
        key = (base_word(row[word_col]), base_word(row[trans_col]))
        result = _agg_lemma(row, lem_col[0], lem_col, tlem_col, key, result)
    return result
