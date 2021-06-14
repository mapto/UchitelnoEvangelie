#!/usr/bin/env python3

from typing import List, Tuple, Optional, Dict
from sortedcontainers import SortedDict, SortedSet  # type: ignore
import re

from const import IDX_COL, STYLE_COL, H_LEMMA_SEP, V_LEMMA_SEP, PATH_SEP, MISSING_CH
from const import DEFAULT_SL, DEFAULT_GR
from model import Index, Usage, LangSemantics, MainLangSemantics, VarLangSemantics
from util import ord_word, base_word

ord_tuple = lambda x: ord_word(x[0])


def _build_paths(row: List[str], tlem_col: List[int]) -> List[str]:
    """
    >>> _build_paths(['боудеть', 'бꙑт\ue205 ', '', 'gram.'], [0,1,2,3])
    ['gram. → бꙑт\ue205 → боудеть']
    >>> _build_paths(['one', 'two', 'three', 'four'], [0, 1, 2, 3])
    ['four → three → two → one']
    >>> _build_paths(['one/two', 'three/four'], [0, 1])
    ['three → one', 'three → two', 'four → one', 'four → two']
    """
    paths: List[List[str]] = [[]]
    for c in tlem_col:
        bw = base_word(row[c])
        new_paths = []
        for w in bw.split(H_LEMMA_SEP):
            for path in paths:
                n = path.copy()
                if w.strip():
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
    val: Usage, nxt: str, key: Tuple[str, str], d: SortedDict
) -> SortedDict:
    """*IN PLACE*"""
    if nxt in d:
        if key not in d[nxt]:
            d[nxt][key] = SortedSet()
        d[nxt][key].add(val)
    else:
        d[nxt] = {key: SortedSet([val])}
    return d


def _get_variant(row, orig: LangSemantics) -> str:
    return "".join([k for k in _multiword(row, orig).keys()])


def _build_usage(
    row: List[str],
    orig: LangSemantics,
    trans: LangSemantics,
    key: Tuple[str, str],
    d: SortedDict,
) -> SortedDict:
    assert row[IDX_COL]

    b = "bold" in row[STYLE_COL]
    i = "italic" in row[STYLE_COL]
    idx = Index.unpack(row[IDX_COL], b, i)
    var = _get_variant(row, orig) + _get_variant(row, trans)
    oalt = orig.alternatives(row)
    talt = trans.alternatives(row)
    val = Usage(idx, orig.lang, var, oalt[0], oalt[1], talt[0], talt[1])
    for nxt in _build_paths(row, trans.lemmas):
        d = _compile_usage(val, nxt, key, d)
    return d


def _multilemma(row: List[str], sem: Optional[VarLangSemantics]) -> Dict[str, str]:
    """
    >>> sem = VarLangSemantics("sl", 0, [1])
    >>> _multilemma(["ноедаго G  днородоу H", "днородъ H / ноѧдъ G"], sem)
    {'H': '\ue201д\ue205нородъ', 'G': '\ue205но\ue20dѧдъ'}
    >>> _multilemma(["", ""], sem)
    {}
    >>> _multilemma(["дноеды WH Ø G", "дноѧдъ"], sem)
    {}
    """
    if not _present(row, sem):
        return {}
    assert sem
    return sem.multilemma(row)


def _multiword(row: List[str], sem: LangSemantics) -> Dict[str, str]:
    """
    >>> sem = VarLangSemantics("sl", 0, [1])
    >>> _multiword(["ноедаго G  днородоу H", "днородъ H / ноѧдъ G"], sem)
    {'G': '\ue205но\ue20dедаго', 'H': '\ue201д\ue205нородоу'}
    >>> _multiword(["ноедаго G", "днородъ H / ноѧдъ G"], sem)
    {'G': '\ue205но\ue20dедаго'}
    >>> _multiword(["", ""], sem)
    {}
    >>> _multiword(["дноеды WH Ø G", "дноѧдъ"], sem)
    {'WH': 'дноеды', 'G': 'Ø'}
    >>> _multiword(["дноеды", "дноѧдъ"], sem)
    {'WGH': 'дноеды'}
    """
    if not _present(row, sem):
        return {}
    return sem.multiword(row)


def _agg_lemma(
    row: List[str],
    orig: Optional[LangSemantics],
    trans: Optional[LangSemantics],
    key: Tuple[str, str],
    d: SortedDict,
    col: int = -1,
) -> SortedDict:
    """Adds a lemma. Recursion ensures that this works with variable depth.

    Args:
        row (List[str]): spreadsheet row
        orig (LangSemantics): original language to iterate through lemma columns, do nothing if absent
        trans (LangSemantics): translation for lemma columns, do nothing if absent
        key (Tuple[str, str]): word pair
        d (SortedDict): see return value
        col (int): lemma column being currently processed, -1 for autodetect/first, -2 for exhausted/last

    Returns:
        SortedDict: *IN PLACE* hierarchical dictionary

    >>> row = [''] * STYLE_COL
    >>> sem = VarLangSemantics(lang='sl_var', word=0, lemmas=[1, 2, 19, 20])
    >>> d = SortedDict()
    >>> _agg_lemma(row, None, sem, ("dummy","pair"), d)
    SortedDict({})
    >>> _agg_lemma(row, sem, None, ("dummy","pair"), d)
    SortedDict({})
    """
    if not _present(row, orig) or not _present(row, trans):
        return d
    assert orig  # for mypy
    assert trans  # for mypy

    if col == -1:  # autodetect/first
        col = orig.lemmas[0]
    elif col == -2:  # exhausted/last
        return _build_usage(row, orig, trans, key, d)

    # TODO: implement variants here
    if type(orig) == VarLangSemantics and row[col]:
        row[col] = row[col].replace(H_LEMMA_SEP, V_LEMMA_SEP)
    lemmas = row[col].split(V_LEMMA_SEP) if row[col] else [""]
    lem_col = orig.lemmas
    for l in lemmas:
        if l.strip() == MISSING_CH:
            continue
        next = base_word(l)
        if next not in d:
            d[next] = SortedDict(ord_word)
        next_idx = lem_col.index(col) + 1
        next_c = lem_col[next_idx] if next_idx < len(lem_col) else -2
        d[next] = _agg_lemma(row, orig, trans, key, d[next], next_c)
    return d


def _present(row: List[str], sem: Optional[LangSemantics]) -> bool:
    return not not sem and not not row[sem.lemmas[0]]


def _build_key(row, sem):
    if _present(row, sem) and sem and sem.word != None and not not row[sem.word]:
        return sem.key(f"{base_word(row[sem.word])}")
    return ""


def aggregate(
    corpus: List[List[str]], orig: MainLangSemantics, trans: MainLangSemantics
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

        # print(row)
        orig_key = _build_key(row, orig)
        orig_key_var = _build_key(row, orig.var)
        trans_key = _build_key(row, trans)
        trans_key_var = _build_key(row, trans.var)
        key = (f"{orig_key}{orig_key_var}", f"{trans_key}{trans_key_var}")

        # print(row[IDX_COL])
        if not [v for v in key if v]:
            continue

        if row[IDX_COL] == "1/W168a25":
            print("plain")
            print(row)
        result = _agg_lemma(row, orig, trans, key, result)
        orig_vars = _multilemma(row, orig.var)
        orig_words = _multiword(row, orig.var)
        trans_vars = _multilemma(row, trans.var)
        trans_words = _multiword(row, trans.var)

        for k in orig_words.keys():
            subrow = list(row)
            subrow[orig.var.word] = orig_words[k]
            if k in orig_vars:
                subrow[orig.var.lemmas[0]] = orig_vars[k]
            orig_subkey_var = _build_key(subrow, orig.var)
            subkey = (f"{orig_key}{orig_subkey_var}", f"{trans_key}{trans_key_var}")
            if row[IDX_COL] == "1/W168a25":
                print("orig var")
                print(subrow)
            result = _agg_lemma(subrow, orig.var, trans, subkey, result)
            for j in trans_words.keys():
                ssubrow = list(subrow)
                ssubrow[trans.var.word] = trans_words[j]
                if j in trans_vars:
                    ssubrow[trans.var.lemmas[0]] = trans_vars[j]
                trans_subkey_var = _build_key(ssubrow, trans.var)
                subkey = (
                    f"{orig_key}{orig_subkey_var}",
                    f"{trans_key}{trans_subkey_var}",
                )
                if row[IDX_COL] == "1/W168a25":
                    print("both var")
                    print(ssubrow)
                result = _agg_lemma(ssubrow, orig.var, trans.var, subkey, result)
        for j in trans_words.keys():
            subrow = list(row)
            subrow[trans.var.word] = trans_words[j]
            if j in trans_vars:
                subrow[trans.var.lemmas[0]] = trans_vars[j]
            trans_subkey_var = _build_key(subrow, trans.var)
            subkey = (f"{orig_key}{orig_key_var}", f"{trans_key}{trans_subkey_var}")
            if row[IDX_COL] == "1/W168a25":
                print("trans var")
                print(subrow)
            result = _agg_lemma(subrow, orig, trans.var, subkey, result)

    return result
