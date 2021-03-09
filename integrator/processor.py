#!/usr/bin/env python3

from typing import List, Tuple
import unicodedata
from sortedcontainers import SortedDict, SortedList, SortedSet  # type: ignore
import re

from const import IDX_COL, STYLE_COL
from model import Index, LangSemantics
from util import ord_word, base_word

ord_tuple = lambda x: ord_word(x[0])


def expand_idx(corpus: List[List[str]]) -> List[List[str]]:
    """*IN_PLACE*"""
    for row in corpus:
        if row[IDX_COL]:
            row[IDX_COL] = Index.unpack(row[IDX_COL]).longstr()
    return corpus


def _collect(group: List[List[str]], col: int) -> List[str]:
    return [group[i][col] for i in range(len(group)) if group[i][col]]


def _highlighted(group: List[List[str]], col: int) -> bool:
    for i in range(len(group)):
        if f"hl{col}" in group[i][STYLE_COL]:
            return True
    return False


def _close(
    group: List[List[str]], orig: LangSemantics, trans: LangSemantics
) -> List[List[str]]:
    """*IN_PLACE*"""
    if not group:
        return []

    assert group[0][IDX_COL]
    idx = Index.unpack(group[0][IDX_COL])
    i_end = None
    for i in range(len(group) - 1, 0, -1):
        s_end = group[i][IDX_COL]
        if s_end:
            i_end = Index.unpack(s_end)
            break
    idx.end = i_end

    # collect content
    word = " ".join(_collect(group, orig.word))
    tr_word = " ".join(_collect(group, trans.word))
    var_word = " ".join(_collect(group, orig.var.word)) if orig.var else ""
    tvar_word = " ".join(_collect(group, trans.var.word)) if trans.var else ""

    tr_lemma = " & ".join(_collect(group, trans.lemmas[0]))
    tvar_lemma = " & ".join(_collect(group, trans.var.lemmas[0])) if trans.var else ""

    var_subl = (
        " ".join(_collect(group, orig.var.lemmas[1]))
        if orig.var and not _highlighted(group, orig.var.lemmas[1])
        else ""
    )
    tvar_subl = (
        " ".join(_collect(group, trans.var.lemmas[1]))
        if trans.var and not _highlighted(group, trans.var.lemmas[1])
        else ""
    )

    tr_subl = [
        "" if _highlighted(group, c) else " ".join(_collect(group, c))
        for c in trans.lemmas[1:]
    ]

    subl = [
        "" if _highlighted(group, c) else " ".join(_collect(group, c))
        for c in orig.lemmas[1:]
    ]

    # update content
    for i in range(len(group)):
        row = group[i]

        row[IDX_COL] = idx.longstr()
        row[orig.word] = word
        row[trans.word] = tr_word
        if orig.var:
            row[orig.var.word] = var_word
            row[orig.var.lemmas[1]] = var_subl
        if trans.var:
            row[trans.var.word] = tvar_word
            row[trans.var.lemmas[0]] = tvar_lemma
            row[trans.var.lemmas[1]] = tvar_subl
        row[trans.lemmas[0]] = tr_lemma

        # subl are missing the first lemma
        for c in range(1, len(orig.lemmas)):
            if subl[c - 1]:
                row[orig.lemmas[c]] = subl[c - 1]

        for c in range(1, len(trans.lemmas)):
            if tr_subl[c - 1]:
                row[trans.lemmas[c]] = tr_subl[c - 1]

    return group


def _grouped(row: List[str], sem: LangSemantics) -> bool:
    if f"hl{sem.word:02d}" in row[STYLE_COL]:
        return True
    if sem.var and f"hl{sem.word:02d}" in row[STYLE_COL]:
        return True
    return False


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

    for raw in corpus:
        row = [v if v else "" for v in raw]
        not_blank = [v for v in row if v]
        if not row[IDX_COL] and not_blank:
            row[IDX_COL] = group[-1][IDX_COL] if group else result[-1][IDX_COL]

        if _grouped(row, orig) or _grouped(row, trans):
            group.append(row)
        else:
            if group:
                group = _close(group, orig, trans)
                result.extend(group)
                group = []
            result.append(row)

    if group:
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
    var: bool = False,
) -> SortedDict:
    """Adds a lemma. Recursion ensures that this works with variable depth.

    Args:
        row (List[str]): spreadsheet row
        col (int): lemma column being currently processed
        lem_col (List[int]): all lemma columns in original language
        tlem_col (List[int]): translation lemma columns
        key (Tuple[str, str]): word pair
        d (SortedDict): see return value
        var: variant or not

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

        assert row[IDX_COL]
        val = Index.unpack(row[IDX_COL])
        val.bold = "bold" in row[STYLE_COL]
        val.italic = "italic" in row[STYLE_COL]
        val.var = var
        if next in d:
            if key not in d[next]:
                # print(key)
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
            d[next] = _agg_lemma(row, next_col, lem_col, tlem_col, key, d[next], var)

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
        if not row[IDX_COL]:
            continue

        orig_key_var = (
            f" {{{base_word(row[orig.var.word])}}}"
            if orig.var and row[orig.var.word]
            else ""
        )
        orig_key = base_word(row[orig.word])
        trans_key_var = (
            f" {{{base_word(row[trans.var.word])}}}"
            if trans.var and row[trans.var.word]
            else ""
        )
        trans_key = base_word(row[trans.word])
        key = (f"{orig_key}{orig_key_var}", f"{trans_key}{trans_key_var}")

        # print(row[IDX_COL])
        # TODO: Do not skip, but collect lemma
        if not [v for v in key if v]:
            continue

        # print(row[IDX_COL])
        result = _agg_lemma(row, orig.lemmas[0], orig.lemmas, trans.lemmas, key, result)
        if orig.var and orig.var.lemmas[0]:
            result = _agg_lemma(
                row,
                orig.var.lemmas[0],
                orig.var.lemmas,
                trans.lemmas,
                key,
                result,
                True,
            )

    return result


def join(a: SortedDict, b: SortedDict) -> SortedDict:
    """*IN_PLACE* for a"""
    for k, v in b.items():
        if k in a:
            if type(v) == SortedDict:
                join(a[k], v)
            elif type(v) == SortedList:
                a[k].update(v)
        else:
            a[k] = v
    return a
