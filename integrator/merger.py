#!/usr/bin/env python3

"""A processor merging multiple lines when they are related"""

from typing import Dict, List

from const import IDX_COL, MISSING_CH, STYLE_COL, V_LEMMA_SEP
from model import Index
from semantics import LangSemantics, MainLangSemantics, VarLangSemantics
from util import ord_word

ord_tuple = lambda x: ord_word(x[0])


def _group_variants(group: List[List[str]], sem: MainLangSemantics) -> str:
    """Returns a list of variants (excluding main) that are present in this group"""
    variants = set()
    for row in group:
        for var in [k for k, val in sem.var.multiword(row).items() if val]:
            variants.add(var)
    return "".join(variants).strip()


def _collect(group: List[List[str]], col: int) -> List[str]:
    """Collects the actual content in the group column"""
    return [group[i][col] for i in range(len(group)) if group[i][col]]


def _normalise_multiword(multiword: Dict[str, str]) -> Dict[str, str]:
    result = {}
    for k, v in multiword.items():
        # split keys in single characters
        for c in k:
            result[c] = v
    return result


def _collect_multiword(group: List[List[str]], sem: MainLangSemantics) -> str:
    """Collects the content of the multiwords for a variant in a group into a single string.
    The output is conformant with the multiword syntax.
    Yet it might contain redundancies, due to the normalisation process (split of equal variants)"""
    collected: Dict[str, str] = {}
    for row in group:
        # for k, v in _normalise_multiword(sem.var.multiword(row)).items():
        for k, v in sem.var.multiword(row).items():
            if k in collected:
                collected[k] = collected[k] + " " + v
            else:
                collected[k] = v
    return " ".join([f"{v} {k}" for k, v in collected.items() if v.strip()])


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
    group: List[List[str]], orig: MainLangSemantics, trans: MainLangSemantics
) -> List[List[str]]:
    """Wraps up a group that is currently being read.
    *IN_PLACE*
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
    variants = _group_variants(group, orig)
    if variants:
        for row in group:
            if row[orig.word] and not row[orig.var.word]:
                row[orig.var.word] = f"{row[orig.word]} {variants}"
            if row[orig.lemmas[0]] and not row[orig.var.lemmas[0]]:
                row[orig.var.lemmas[0]] = row[orig.lemmas[0]]

    # only lines without highlited sublemmas, i.e. gramm. annotation
    merge_rows = [
        i for i, r in enumerate(group) if not _highlighted_sublemma(orig, trans, r)
    ]
    merge_group = [group[i] for i in merge_rows]

    # collect content
    line = [""] * STYLE_COL

    line[orig.word] = " ".join(_collect(group, orig.word))
    line[trans.word] = " ".join(_collect(group, trans.word))

    line[orig.var.word] = _collect_multiword(group, orig)
    line[trans.var.word] = _collect_multiword(group, trans)

    for c in trans.lem1_cols():
        g = [e for e in _collect(merge_group, c) if e.strip() != MISSING_CH]
        line[c] = f" {V_LEMMA_SEP} ".join(g)
    for c in orig.lemn_cols() + trans.lemn_cols():
        g = [e for e in _collect(merge_group, c) if e.strip() != MISSING_CH]
        line[c] = " ".join(g)

    # update content
    for i in range(len(group)):
        group[i][IDX_COL] = idx.longstr()
        for c in orig.word_cols():
            if not _highlighted_sublemma(orig, trans, group[i]):
                group[i][c] = line[c]
        for c in orig.lemn_cols() + trans.cols():
            if i in merge_rows:
                group[i][c] = line[c]

    return group


def _grouped(row: List[str], sem: MainLangSemantics) -> bool:
    """Returns if the row takes part of a group with respect to this language (and its variants)"""
    if f"hl{sem.word:02d}" in row[STYLE_COL]:
        return True
    if f"hl{sem.var.word:02d}" in row[STYLE_COL]:
        return True
    return False


def merge(
    corpus: List[List[str]], orig: MainLangSemantics, trans: MainLangSemantics
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

        # if "1/6a10" in row[IDX_COL]:
        #     print(row)

        not_blank = [v for v in row if v]
        if not row[IDX_COL] and not_blank:
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
