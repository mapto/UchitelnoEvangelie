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
    if not word:
        return False
    word = word.strip().lower()
    if word == "=":
        return False
    return True


def _collect(group: List[List[str]], col: int) -> List[str]:
    return [group[i][col] for i in range(len(group)) if _present(group[i][col])]


def _close(
    group: List[List[str]], orig: LangSemantics, trans: LangSemantics
) -> List[List[str]]:
    """*IN_PLACE*"""
    if not group:
        return []

    assert group[0][3]
    idx = Index.unpack(group[0][3])
    i_end = None
    for i in range(len(group) - 1, 0, -1):
        s_end = group[i][3]
        if s_end:
            i_end = Index.unpack(s_end)
            break
    idx.end = i_end

    word = " ".join(_collect(group, orig.word))
    tr_word = " ".join(_collect(group, trans.word))
    tr_lemma = " & ".join(_collect(group, trans.lemmas[0]))

    tr_subl = [" ".join(_collect(group, c)) for c in trans.lemmas[1:]]
    subl = [" ".join(_collect(group, c)) for c in orig.lemmas[1:]]

    for i in range(len(group)):
        row = group[i]

        row[3] = idx.longstr()
        row[orig.word] = word
        row[trans.word] = tr_word
        row[trans.lemmas[0]] = tr_lemma

        # subl are missing the first lemma
        for c in range(1, len(orig.lemmas)):
            row[orig.lemmas[c]] = subl[c - 1]
        for c in range(1, len(trans.lemmas)):
            row[trans.lemmas[c]] = tr_subl[c - 1]

    return group


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
    group: List[List[str]] = []
    result: List[List[str]] = []

    for old_row in corpus:
        row = [v if v else "" for v in old_row]
        if not row[3]:
            row[3] = group[-1][3] if group else result[-1][3]
        absence = [row[c] for c in (orig.word, trans.word) if not _present(row[c])]
        absence.extend([row[c] for c in orig.lemmas[1:] if row[c] == "="])
        if not absence and group:
            group = _close(group, orig, trans)
            result.extend(group)
            group = []
        group.append(row)

    group = _close(group, orig, trans)
    result.extend(group)
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
        # next = "→ ".join(cols)
        next = " >> ".join(cols)

        assert row[3]
        val = Index.unpack(row[3])
        val.bold = "bold" in row[16]
        val.italic = "italic" in row[16]
        if next in d:
            if key not in d[next]:
                d[next][key] = SortedList()
            d[next][key].add(val)
        else:
            d[next] = {key: SortedList([val])}

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
    result = SortedDict(ord_word)
    for row in corpus:
        if not row[3]:
            continue
        key = (base_word(row[orig.word]), base_word(row[trans.word]))
        result = _agg_lemma(row, orig.lemmas[0], orig.lemmas, trans.lemmas, key, result)
    return result
