#!/usr/bin/env python3

"""A processor merging multiple lines when they are related"""

from typing import Dict, List

from const import IDX_COL, MISSING_CH, STYLE_COL, V_LEMMA_SEP
from model import Index, Source
from semantics import LangSemantics, MainLangSemantics, VarLangSemantics, present
from util import clean_word


def _group_variants(group: List[List[str]], sem: LangSemantics) -> Source:
    """Returns a list of variants (excluding main) that are present in this group"""
    variants = set()
    assert sem.var  # for mypy
    for row in group:
        for var in [k for k, val in sem.var.multiword(row).items() if val]:
            variants.add(var)
    return Source("".join(str(v) for v in variants).strip())


def _collect(group: List[List[str]], col: int) -> List[str]:
    """Collects the actual content in the group column"""
    return [group[i][col] for i in range(len(group)) if group[i][col]]


def _collect_multiword(group: List[List[str]], sem: LangSemantics) -> str:
    """Collects the content of the multiwords for a variant in a group into a single string.
    The output is conformant with the multiword syntax.
    Yet it might contain redundancies, due to the normalisation process (split of equal variants)"""
    collected: Dict[Source, str] = {}
    assert sem.var  # for mypy
    for row in group:
        # for k, v in _normalise_multiword(sem.var.multiword(row)).items():
        for k, v in sem.var.multiword(row).items():
            if k in collected:
                collected[k] = collected[k] + " " + v
            else:
                collected[k] = v
    return " ".join([f"{v} {k}" for k, v in collected.items() if v.strip()])


def _collect_multilemma(group: List[List[str]], sem: LangSemantics) -> str:
    """TODO implement the multilemma part"""
    return " ".join(_collect(group, sem.other().lemmas[0]))


def _highlighted(row: List[str], col: int) -> bool:
    return f"hl{col:02d}" in row[STYLE_COL]


def _highlighted_sublemma(
    osem: LangSemantics, tsem: LangSemantics, row: List[str]
) -> bool:
    """
    >>> sl_sem = MainLangSemantics("sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3]))
    >>> gr_sem = MainLangSemantics("gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19]))
    >>> r = ['', '', '', '', '1/W168a15', 'б\ue205хомь', 'б\ue205хомь стрьпѣтї• ', 'бꙑт\ue205 ', '', 'gramm.', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl05|hl09']
    >>> _highlighted_sublemma(sl_sem, gr_sem, r)
    True
    >>> _highlighted_sublemma(gr_sem, sl_sem, r)
    True
    >>> r = ['', '', '', '', '1/W168a14', 'вьꙁмогл\ue205', 'мы брьньн\ue205 \ue205 ꙁемⷧ҇ьн\ue205\ue205• вьꙁмогл\ue205', 'въꙁмощ\ue205', '', '', '', 'ἠδυνήθημεν', 'δύναμαι', 'pass.', '', '', '', '', '', '', '', '', '', '', '', '', 'hl05']
    >>> _highlighted_sublemma(sl_sem, gr_sem, r)
    False
    >>> _highlighted_sublemma(gr_sem, sl_sem, r)
    False
    >>> r = ['+ \ue201сть GH', 'бꙑт\ue205', 'gramm.', '', '07/47a06', 'om.', 'сътвор\ue205лъ', 'om.', '', '', '', 'Ø', 'Ø', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl05|hl02']
    >>> _highlighted_sublemma(sl_sem, gr_sem, r)
    True
    >>> _highlighted_sublemma(sl_sem.var, gr_sem.var, r)
    True
    >>> r = ['', '', '', '', '12/67c10', 'бꙑхомъ•', 'в\ue205дѣл\ue205 бꙑхо-', 'бꙑт\ue205', '', 'gramm.', '', '', 'gramm.', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl05|hl09']
    >>> _highlighted_sublemma(sl_sem, gr_sem, r)
    True
    >>> _highlighted_sublemma(sl_sem.var, gr_sem, r)
    True
    """
    return any([_highlighted(row, c) for c in osem.lemn_cols() + tsem.lemn_cols()])


def _merge_indices(group: List[List[str]]) -> Index:
    """Merge the individual indices of a group into a group/multiline index"""
    s_end = None
    for i in range(len(group) - 1, 0, -1):
        s_end = group[i][IDX_COL]
        if s_end:
            break
    if not s_end:
        s_end = group[0][IDX_COL]
    return Index.unpack(f"{group[0][IDX_COL]}-{s_end}")


def _close(
    group: List[List[str]], orig: LangSemantics, trans: LangSemantics
) -> List[List[str]]:
    """Wraps up a group that is currently being read.
    Redistributes content according to desired (complex) logic
    """
    if not group:
        return []
    if not group[0][IDX_COL]:
        idxline = 0
        for i, row in enumerate(group):
            if row[IDX_COL]:
                group[0][IDX_COL] = row[IDX_COL]
                idxline = i + 1
                break
        if idxline:
            print(
                f"WARNING: липсва индекс в първия ред от групата. Намерен в {idxline} ред"
            )
        else:
            for row in group:
                print(row)
            print(f"ГРЕШКА: липсва индекс в групата.")

    idx = _merge_indices(group)

    # populate variants equal to main
    assert orig.main  # for mypy
    variants = _group_variants(group, orig.main)
    assert orig.var  # for mypy
    if variants:
        for row in group:
            if present(row, orig.var) and row[orig.word] and not row[orig.var.word]:
                row[orig.var.word] = f"{row[orig.word]} {variants}"

    # only lines without highlited sublemmas, i.e. gramm. annotation
    merge_rows = [
        i for i, r in enumerate(group) if not _highlighted_sublemma(orig, trans, r)
    ]
    merge_group = [group[i] for i in merge_rows]

    # collect content
    line = [""] * STYLE_COL

    line[orig.word] = " ".join(_collect(merge_group, orig.word))
    line[trans.word] = " ".join(_collect(group, trans.word))

    line[orig.var.word] = _collect_multiword(merge_group, orig)
    assert trans.var  # for mypy
    line[trans.var.word] = _collect_multiword(group, trans)

    line[orig.other().lemmas[0]] = _collect_multilemma(merge_group, orig)

    for c in trans.lem1_cols():
        g = [e for e in _collect(merge_group, c) if e.strip() != MISSING_CH]
        line[c] = f" {V_LEMMA_SEP} ".join(g)
    for c in orig.lemn_cols() + trans.lemn_cols():
        g = [e for e in _collect(merge_group, c) if e.strip() != MISSING_CH]
        line[c] = " ".join(g)

    # update content
    for i in range(len(group)):
        if not _highlighted_sublemma(orig, trans, group[i]):
            group[i][IDX_COL] = idx.longstr()
            for c in orig.word_cols() + orig.lemn_cols():
                group[i][c] = line[c]
            group[i][orig.other().lemmas[0]] = line[orig.other().lemmas[0]]
        for c in trans.cols():
            if i in merge_rows:
                group[i][c] = line[c]

    return group.copy()


def _grouped(row: List[str], sem: LangSemantics) -> bool:
    """Returns if the row takes part of a group with respect to this language (and its variants)"""
    if f"hl{sem.word:02d}" in row[STYLE_COL]:
        return True
    if f"hl{sem.other().word:02d}" in row[STYLE_COL]:
        return True
    return False


def merge(
    corpus: List[List[str]], orig: MainLangSemantics, trans: MainLangSemantics
) -> List[List[str]]:
    """Merge lines according to color groups. This is an asymmetric operation

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
        row = [clean_word(v) if v else "" for v in raw]

        # if "1/6a10" in row[IDX_COL]:
        #     print(row)

        if not row[IDX_COL] and any(row):
            row[IDX_COL] = group[-1][IDX_COL] if group else result[-1][IDX_COL]

        if _grouped(row, orig) or _grouped(row, trans):
            group.append(row)
        else:
            if group:
                group = _close(group, orig, trans)
                result += group
                group = []
            result.append(row)

    if group:
        group = _close(group, orig, trans)
        result += group

    return result
