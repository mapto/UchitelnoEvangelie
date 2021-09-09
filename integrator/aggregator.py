#!/usr/bin/env python3

"""A processor aggregating different usages into a dictionary hierarchy"""

from typing import List, Optional, Dict
from sortedcontainers import SortedDict  # type: ignore

from const import IDX_COL, H_LEMMA_SEP, V_LEMMA_SEP, MISSING_CH

from util import ord_word, base_word

from semantics import present
from semantics import LangSemantics, MainLangSemantics, VarLangSemantics

ord_tuple = lambda x: ord_word(x[0])


def _build_usages(
    row: List[str],
    orig: LangSemantics,
    trans: LangSemantics,
    d: SortedDict,
    olemma: str,
    tlemma: str,
) -> SortedDict:
    assert row[IDX_COL]

    return orig.build_usages(trans, row, d, olemma, tlemma)


def _multilemma(row: List[str], sem: Optional[LangSemantics]) -> Dict[str, str]:
    if not present(row, sem):
        return {}
    assert sem
    return sem.multilemma(row)


def _agg_lemma(
    row: List[str],
    orig: Optional[LangSemantics],
    trans: Optional[LangSemantics],
    d: SortedDict,
    col: int = -1,
    olemma: str = "",
    tlemma: str = "",
) -> SortedDict:
    """Adds a lemma. Recursion ensures that this works with variable depth.

    Args:
        row (List[str]): spreadsheet row
        orig (LangSemantics): original language to iterate through lemma columns, do nothing if absent
        trans (LangSemantics): translation for lemma columns, do nothing if absent
        key (Tuple[str, str]): word pair
        d (SortedDict): see return value
        col (int): lemma column being currently processed, -1 for autodetect/first, -2 for exhausted/last,
        olemma: the processed original first lemma, potentially from variant multilemma
        tlemma: the translation first lemma being considered, potentially from variant multilemma

    Returns:
        SortedDict: *IN PLACE* hierarchical dictionary
    """
    if not present(row, orig) or not present(row, trans):
        return d
    assert orig  # for mypy
    assert trans  # for mypy

    omultilemmas = {}
    tmultilemmas = {}
    if col == -1:  # autodetect/first
        col = orig.lemmas[0]
        omultilemmas = _multilemma(row, orig)
        tmultilemmas = _multilemma(row, trans)
    elif col == -2:  # exhausted/last
        return _build_usages(row, orig, trans, d, olemma, tlemma)

    # TODO: implement variants here
    if type(orig) == VarLangSemantics and row[col]:
        row[col] = row[col].replace(H_LEMMA_SEP, V_LEMMA_SEP)
    # lemmas = row[col].split(V_LEMMA_SEP) if row[col] else [""]
    if not omultilemmas:
        omultilemmas[""] = row[col]
    if not tmultilemmas:
        tmultilemmas[""] = tlemma

    lem_col = orig.lemmas
    for oli in omultilemmas.values():
        for tli in tmultilemmas.values():
            if oli.strip() == MISSING_CH:
                continue
            nxt = base_word(oli)
            if nxt not in d:
                d[nxt] = SortedDict(ord_word)
            next_idx = lem_col.index(col) + 1
            next_c = lem_col[next_idx] if next_idx < len(lem_col) else -2
            ol = olemma if olemma else oli
            tl = tlemma if tlemma else tli
            d[nxt] = _agg_lemma(
                row,
                orig,
                trans,
                d[nxt],
                next_c,
                ol,
                tl,
            )
    return d


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

        # if "1/W168a25" in row[IDX_COL]:
        #     print(row)

        result = _agg_lemma(row, orig, trans, result)
        result = _agg_lemma(row, orig.var, trans, result)
        result = _agg_lemma(row, orig, trans.var, result)
        result = _agg_lemma(row, orig.var, trans.var, result)

    return result
