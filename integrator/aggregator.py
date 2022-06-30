#!/usr/bin/env python3

"""A processor aggregating different usages into a dictionary hierarchy"""

from typing import List, Optional, Dict
from sortedcontainers import SortedDict  # type: ignore

from const import IDX_COL, H_LEMMA_SEP, V_LEMMA_SEP, MISSING_CH

from util import ord_word, base_word

from model import Source

from semantics import present
from semantics import LangSemantics, MainLangSemantics, VarLangSemantics

FIRST_LEMMA = -1
LAST_LEMMA = -2


def _multilemma(
    row: List[str], sem: Optional[LangSemantics], lidx: int = 0
) -> Dict[Source, str]:
    if not present(row, sem):
        return {}
    assert sem
    return sem.multilemma(row, lidx)


def _agg_lemma(
    row: List[str],
    orig: LangSemantics,
    trans: LangSemantics,
    d: SortedDict,
    col: int = FIRST_LEMMA,
    olemma: str = "",
    olemvar: Source = Source(),
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

    lem_cols = orig.lemmas
    omultilemmas = {}
    tmultilemmas = {}
    if col == FIRST_LEMMA:  # autodetect
        col = lem_cols[0]
        tmultilemmas = _multilemma(row, trans)
    elif col == LAST_LEMMA:  # exhausted
        assert row[IDX_COL]
        return orig.compile_usages(trans, row, d, olemma, tlemma, olemvar)
    lidx = lem_cols.index(col)
    omultilemmas = _multilemma(row, orig, lidx)

    # if orig.is_variant() and row[col]:
    #     row[col] = row[col].replace(H_LEMMA_SEP, V_LEMMA_SEP)
    # lemmas = row[col].split(V_LEMMA_SEP) if row[col] else [""]
    if not omultilemmas:
        omultilemmas[Source("")] = row[col]
    if not tmultilemmas:
        tmultilemmas[Source("")] = tlemma

    for oliv, oli in omultilemmas.items():
        for tli in tmultilemmas.values():
            if oli.strip() == MISSING_CH:
                continue
            if oliv and olemvar and oliv not in olemvar:
                continue
            nxt = base_word(oli)
            if nxt not in d:
                d[nxt] = SortedDict(ord_word)
            next_idx = lem_cols.index(col) + 1
            next_c = lem_cols[next_idx] if next_idx < len(lem_cols) else LAST_LEMMA
            ol = olemma if olemma else oli
            # pick last present lemma source
            olv = oliv if oliv else olemvar
            tl = tlemma if tlemma else tli
            d[nxt] = _agg_lemma(
                row,
                orig,
                trans,
                d[nxt],
                next_c,
                ol,
                olv,
                tl,
            )
    return d


def _expand_and_aggregate(
    row: List[str],
    orig: Optional[LangSemantics],
    trans: Optional[LangSemantics],
    d: SortedDict,
) -> SortedDict:
    if not present(row, orig) or not present(row, trans):
        return d
    assert orig  # for mypy
    assert trans  # for mypy

    result = _agg_lemma(row, orig, trans, d)
    return result


def aggregate(
    corpus: List[List[str]],
    orig: LangSemantics,
    trans: LangSemantics,
    result: SortedDict,
) -> SortedDict:
    """Generate an aggregated index of translations. Recursion ensures that this works with variable depth.

    Args:
        corpus (List[List[str]]): input spreadsheet
        orig (LangSemantics): original language table column mapping
        trans (LangSemantics): translation language table column mapping
        result: mutable return value

    Returns:
        SortedDict: hierarchical dictionary of all lemma levels in original language, that contains rows of the form: translation_lemma: word/tword (index)
    """
    for row in corpus:
        if not row[IDX_COL]:
            continue

        # if "05/028d18" in row[IDX_COL]:
        # if "μονογεν" in row[orig.lemmas[0]]:
        #    print(row)

        try:
            _expand_and_aggregate(row, orig, trans, result)
            _expand_and_aggregate(row, orig, trans.var, result)
        except Exception as e:
            print(
                f"ГРЕШКА: При кондензиране възникна проблем в ред {row[IDX_COL]} ({row[orig.word]}/{row[trans.word]})"
            )
            print(e)
            break

    return result
