#!/usr/bin/env python3

"""A processor aggregating different usages into a dictionary hierarchy"""

from typing import List, Optional, Dict
import logging as log
from sortedcontainers import SortedDict  # type: ignore

from const import IDX_COL, MISSING_CH, SPECIAL_CHARS

from util import ord_word, base_word

from model import Source

from semantics import present
from semantics import LangSemantics, MainLangSemantics, VarLangSemantics

FIRST_LEMMA = -1
LAST_LEMMA = -2


def _multilemma(row: List[str], sem: LangSemantics, lidx: int = 0) -> Dict[Source, str]:
    if not present(row, sem):
        return {}
    assert sem
    return sem.multilemma(row, lidx)


def reorganise_orig_special(
    row: List[str], orig: LangSemantics, trans: LangSemantics
) -> List[str]:
    """In cases when in the original side of semantics,
    a sublemma contains only a special character,
    this should not show up as a level in the lemma hierarchy,
    but appended to the translation word usage"""
    # remove sublemma
    olast = next(
        iter(i for i in range(len(orig.lemmas) - 1, -1, -1) if row[orig.lemmas[i]])
    )

    # get only the SPECIAL_CHARS from variant that might contain also source
    special = row[orig.lemmas[olast]][0]
    assert special in SPECIAL_CHARS
    row[orig.lemmas[olast]] = ""

    # add special_char sublemma to translation
    tlast = next(
        iter(i for i in range(len(trans.lemmas) - 1, -1, -1) if row[trans.lemmas[i]])
    )
    # print(tlast)
    # if not tlast:
    #     row[trans.lemmas[1]] = f"{special} {row[trans.lemmas[0]]}"
    # else:
    row[trans.lemmas[tlast]] = f"{special} {row[trans.lemmas[tlast]]}"
    return row


def reorganise_trans_special(row: List[str], trans: LangSemantics) -> List[str]:
    """In cases when in the translation side of semantics,
    a sublemma contains only a special character,
    this should be appended to the previous lemma in the word usage"""

    tlast = next(
        iter(i for i in range(len(trans.lemmas) - 1, -1, -1) if row[trans.lemmas[i]])
    )
    assert tlast > 0

    # get only the SPECIAL_CHARS from variant that might contain also source
    special = row[trans.lemmas[tlast]][0]
    assert special in SPECIAL_CHARS
    row[trans.lemmas[tlast]] = ""

    row[trans.lemmas[tlast - 1]] = f"{special} {row[trans.lemmas[tlast-1]]}"
    return row


def breakdown_multilemmas(
    multilemmas: Dict[Source, str], olemvar: Source
) -> Optional[Dict[Source, str]]:
    """If two upper lemmas have one sublemma, separate them to make operations easier

    >>> breakdown_multilemmas({Source('CsFbMdPcPePgPhPiVZaAPaSpCh'): 'Gen.'}, Source('CsMdSp'))
    {Source('CsMdSp'): 'Gen.', Source('FbPcPePgPhPiVZaAPaCh'): 'Gen.'}
    >>> breakdown_multilemmas({Source('CsFbMdPcPePgPhPiVZaAPaSpCh'): 'Gen.'}, Source())
    >>> breakdown_multilemmas({Source('PcPePgPhPiPa'): 'Gen.'}, Source('CsCh'))
    """
    if not olemvar:
        return None
    change = False
    cp = multilemmas.copy()
    for oliv, oli in multilemmas.items():
        if olemvar in oliv and olemvar != oliv:
            change = True
            val = cp.pop(oliv)
            cp[olemvar] = val
            rem = oliv.remainder(olemvar)
            assert rem  # for mypy
            cp[rem] = val

    return cp if change else None


def _agg_lemma(
    row: List[str],
    orig: LangSemantics,
    trans: LangSemantics,
    d: SortedDict,
    col: int = FIRST_LEMMA,
    olemvar: Source = Source(),
    tlemma: str = "",
) -> SortedDict:
    """Adds a lemma. Recursion ensures that this works with variable depth.

    Args:
        row (List[str]): spreadsheet row
        orig (LangSemantics): original language to iterate through lemma columns, do nothing if absent
        trans (LangSemantics): translation for lemma columns, do nothing if absent
        d (SortedDict): see return value
        col (int): lemma column being currently processed, -1 for autodetect/first, -2 for exhausted/last,
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
        return orig.compile_usages(trans, row, d, tlemma, olemvar)
    lidx = lem_cols.index(col)
    omultilemmas = _multilemma(row, orig, lidx)

    if not omultilemmas:
        omultilemmas[Source("")] = row[col]
    if not tmultilemmas:
        tmultilemmas[Source("")] = tlemma

    next_idx = lem_cols.index(col) + 1
    next_col = lem_cols[next_idx] if next_idx < len(lem_cols) else LAST_LEMMA

    # if a source was indicated in previous lemmas, but not in this one,
    # just add empties to fill rest of lemma hierarchy for it
    if lidx > 0 and olemvar:
        missing = olemvar.remainder(omultilemmas.keys())
        if missing:
            if "" not in d:
                d[""] = SortedDict(ord_word)
            d[""] = _agg_lemma(
                row,
                orig,
                trans,
                d[""],
                next_col,
                missing,
                tlemma,
            )
    breakdown = breakdown_multilemmas(omultilemmas, olemvar)
    omultilemmas = breakdown if breakdown else omultilemmas

    # process sources indicated in this lemma
    for oliv, oli in omultilemmas.items():
        if oli.strip() == MISSING_CH:
            continue
        if oliv and olemvar and oliv not in olemvar:
            continue
        nxt = base_word(oli)
        if nxt in SPECIAL_CHARS:
            row = reorganise_orig_special(row, orig, trans)
            nxt = ""
            # TODO: combination of multilemmas and standalone special symbols is only partially implemented.
            # Is it possible that a special symbol is relevant to only one variant? What should we do in this case?
            multilemma = trans.multilemma(row)
            assert len(multilemma) == 1
            tlemma = next(iter(multilemma.values()))
        if nxt not in d:
            d[nxt] = SortedDict(ord_word)
        # pick last present lemma source
        olv = oliv if oliv else olemvar
        for tli in tmultilemmas.values():
            tl = tlemma if tlemma else tli
            d[nxt] = _agg_lemma(
                row,
                orig,
                trans,
                d[nxt],
                next_col,
                olv,
                tl,
            )
    return d


def _expand_and_aggregate(
    row: List[str],
    orig: LangSemantics,
    trans: LangSemantics,
    d: SortedDict,
) -> SortedDict:
    if not present(row, orig) or not present(row, trans):
        return d
    assert orig  # for mypy
    assert trans  # for mypy

    tother = trans.other()
    inv_lemmas = [
        tother.lemmas[i]
        for i in range(len(tother.lemmas) - 1, -1, -1)
        if row[tother.lemmas[i]]
    ]
    if inv_lemmas and row[inv_lemmas[0]][0] in SPECIAL_CHARS:
        row = reorganise_trans_special(row, tother)

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
            _expand_and_aggregate(row.copy(), orig, trans, result)
            assert trans.var
            _expand_and_aggregate(row.copy(), orig, trans.var, result)
        except Exception as e:
            log.error(
                f"При кондензиране възникна проблем в ред {row[IDX_COL]} ({row[orig.word]}/{row[trans.word]})"
            )
            log.error(e)
            continue

    return result
