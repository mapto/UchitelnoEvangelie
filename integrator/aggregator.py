#!/usr/bin/env python3

from typing import List, Tuple, Optional, Dict
from sortedcontainers import SortedDict, SortedSet  # type: ignore
import re

from const import IDX_COL, STYLE_COL, H_LEMMA_SEP, V_LEMMA_SEP, PATH_SEP
from model import Index, LangSemantics
from util import ord_word, base_word

ord_tuple = lambda x: ord_word(x[0])


def _build_paths(row: List[str], tlem_col: List[int]) -> List[str]:
    """
    >>> _build_paths(['one', 'two', 'three', 'four'], [0, 1, 2, 3])
    ['four >> three >> two >> one']
    >>> _build_paths(['one/two', 'three/four'], [0, 1])
    ['three >> one', 'three >> two', 'four >> one', 'four >> two']
    """
    paths: List[List[str]] = [[]]
    for c in tlem_col:
        bw = base_word(row[c])
        new_paths = []
        for w in bw.split(H_LEMMA_SEP):
            for path in paths:
                n = path.copy()
                n.append(w.strip())
                new_paths.append(n)
        paths = new_paths

    result: List[str] = []
    for cols in paths:
        cols.reverse()
        empty = True
        while empty:
            if not cols[0]:
                cols.pop(0)
                empty = len(cols) > 0
            else:
                empty = False
        result.append(PATH_SEP.join(cols))

    return result


def _compile_usage(
    val: Index, nxt: str, key: Tuple[str, str], d: SortedDict
) -> SortedDict:
    """*IN PLACE*"""
    if nxt in d:
        if key not in d[nxt]:
            d[nxt][key] = SortedSet()
        d[nxt][key].add(val)
    else:
        d[nxt] = {key: SortedSet([val])}
    return d


def _build_usage(
    row: List[str],
    trans: LangSemantics,
    key: Tuple[str, str],
    d: SortedDict,
    var: str = "",
) -> SortedDict:
    assert row[IDX_COL]

    b = "bold" in row[STYLE_COL]
    i = "italic" in row[STYLE_COL]
    val = Index.unpack(row[IDX_COL], b, i, var)
    for nxt in _build_paths(row, trans.lemmas):
        d = _compile_usage(val, nxt, key, d)
    return d


def _agg_lemma(
    row: List[str],
    orig: Optional[LangSemantics],
    trans: Optional[LangSemantics],
    key: Tuple[str, str],
    d: SortedDict,
    var: str = "",
    col: int = -1,
) -> SortedDict:
    """Adds a lemma. Recursion ensures that this works with variable depth.

    Args:
        row (List[str]): spreadsheet row
        orig (LangSemantics): original language to iterate through lemma columns, do nothing if absent
        trans (LangSemantics): translation for lemma columns, do nothing if absent
        key (Tuple[str, str]): word pair
        d (SortedDict): see return value
        var (bool): variant or not
        col (int): lemma column being currently processed, -1 for autodetect/first, -2 for exhausted/last

    Returns:
        SortedDict: *IN PLACE* hierarchical dictionary

    >>> row = [''] * STYLE_COL
    >>> sem = LangSemantics(lang='sl_var', word=0, lemmas=[1, 2, 19, 20], var=None)
    >>> d = SortedDict()
    >>> _agg_lemma(row, None, sem, ("dummy","pair"), d)
    SortedDict({})
    >>> _agg_lemma(row, sem, None, ("dummy","pair"), d)
    SortedDict({})
    """

    if not _present(row, orig) or not _present(row, trans):
        return d
    assert orig  # for mypy

    if col == -1:  # autodetect/first
        col = orig.lemmas[0]
    elif col == -2:  # exhausted/last
        assert trans  # for mypy
        return _build_usage(row, trans, key, d, var)

    # TODO: implement variants here
    if var and row[col]:
        row[col] = row[col].replace(H_LEMMA_SEP, V_LEMMA_SEP)
    lemmas = row[col].split(V_LEMMA_SEP) if row[col] else [""]
    lem_col = orig.lemmas
    for l in lemmas:
        next = base_word(l)
        if next not in d:
            d[next] = SortedDict(ord_word)
        next_idx = lem_col.index(col) + 1
        next_c = lem_col[next_idx] if next_idx < len(lem_col) else -2
        d[next] = _agg_lemma(row, orig, trans, key, d[next], var, next_c)
    return d


def _present(row: List[str], sem: Optional[LangSemantics]) -> bool:
    return not not sem and not not row[sem.lemmas[0]]


def _build_key(row, sem, var=False):
    """
    >>> sem = LangSemantics(lang='sl', word=4, lemmas=[6, 7, 8, 9], var=LangSemantics(lang='sl_var', word=0, lemmas=[1, 2, 19, 20], var=None))
    >>> row = ['\ue201л\ue205ко WH', '\ue201л\ue205къ', '', '1/7c12', 'сел\ue205ко', 'въ сел\ue205ко', 'сел\ue205къ', '', '', '', 'τοῦτο', 'οὗτος', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10']
    >>> _build_key(row, sem)
    'сел\ue205ко'
    >>> _build_key(row, sem.var, True)
    ' {\ue201л\ue205ко WH}'
    """
    word = (
        f"{base_word(row[sem.word])}"
        if _present(row, sem)
        and sem  # for mypy
        and sem.word != None  # for mypy
        and not not row[sem.word]
        else ""
    )
    if not word:
        return ""
    return f" {{{word}}}" if var else f"{word}"


def aggregate(
    corpus: List[List[str]], orig: LangSemantics, trans: LangSemantics
) -> SortedDict:
    """Generate an aggregated index of translations. Recursion ensures that this works with variable depth.

    Args:
        corpus (List[List[str]]): input spreadsheet
        orig (LangSemantics): original language table column mapping
        trans (LangSemantics): translation language table column mapping

    Returns:
        SortedDict: hierarchical dictionary of all lemma levels in original language, that contains rows of the form: translation_lemma: word/tword (index)
    """
    result = SortedDict(ord_word)
    for row in corpus:
        if not row[IDX_COL]:
            continue

        orig_key = _build_key(row, orig)
        orig_key_var = _build_key(row, orig.var, True)
        trans_key = _build_key(row, trans)
        trans_key_var = _build_key(row, trans.var, True)
        key = (f"{orig_key}{orig_key_var}", f"{trans_key}{trans_key_var}")

        # print(row[IDX_COL])
        if not [v for v in key if v]:
            continue

        result = _agg_lemma(row, orig, trans, key, result)
        result = _agg_lemma(row, orig.var, trans, key, result, "WH")
        result = _agg_lemma(row, orig, trans.var, key, result, "WH")
        result = _agg_lemma(row, orig.var, trans.var, key, result, "WH")

    return result
