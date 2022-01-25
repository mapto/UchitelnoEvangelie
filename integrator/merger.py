#!/usr/bin/env python3

"""A processor merging multiple lines when they are related"""

from typing import Dict, List

from const import IDX_COL, MISSING_CH, SPECIAL_CHARS, STYLE_COL, V_LEMMA_SEP
from model import Index, Source
from semantics import LangSemantics, MainLangSemantics, VarLangSemantics, present
from util import clean_word, collect


def _group_variants(group: List[List[str]], sem: LangSemantics) -> Source:
    """Returns a list of variants (excluding main) that are present in this group"""
    variants = set()
    assert sem.var  # for mypy
    for row in group:
        for var in [k for k, val in sem.var.multiword(row).items() if val]:
            variants.add(var)
    return Source("".join(str(v) for v in variants).strip())


def _hilited(row: List[str], col: int) -> bool:
    """highlighting implemented via background colour"""
    return f"hl{col:02d}" in row[STYLE_COL]


def _hilited_lemma(osem: LangSemantics, tsem: LangSemantics, row: List[str]) -> bool:
    """
    >>> sl_sem = MainLangSemantics("sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3]))
    >>> gr_sem = MainLangSemantics("gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19]))
    >>> r = ['', '', '', '', '1/W168a15', 'б\ue205хомь', 'б\ue205хомь стрьпѣтї• ', 'бꙑт\ue205 ', '', 'gramm.', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl05|hl09']
    >>> _hilited_lemma(sl_sem, gr_sem, r)
    True
    >>> _hilited_lemma(gr_sem, sl_sem, r)
    True
    >>> r = ['', '', '', '', '1/W168a14', 'вьꙁмогл\ue205', 'мы брьньн\ue205 \ue205 ꙁемⷧ҇ьн\ue205\ue205• вьꙁмогл\ue205', 'въꙁмощ\ue205', '', '', '', 'ἠδυνήθημεν', 'δύναμαι', 'pass.', '', '', '', '', '', '', '', '', '', '', '', '', 'hl05']
    >>> _hilited_lemma(sl_sem, gr_sem, r)
    False
    >>> _hilited_lemma(gr_sem, sl_sem, r)
    False
    >>> r = ['+ \ue201сть GH', 'бꙑт\ue205', 'gramm.', '', '07/47a06', 'om.', 'сътвор\ue205лъ', 'om.', '', '', '', 'Ø', 'Ø', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl05|hl02']
    >>> _hilited_lemma(sl_sem, gr_sem, r)
    True
    >>> _hilited_lemma(sl_sem.var, gr_sem.var, r)
    True
    >>> r = ['', '', '', '', '12/67c10', 'бꙑхомъ•', 'в\ue205дѣл\ue205 бꙑхо-', 'бꙑт\ue205', '', 'gramm.', '', '', 'gramm.', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl05|hl09']
    >>> _hilited_lemma(sl_sem, gr_sem, r)
    True
    >>> _hilited_lemma(sl_sem.var, gr_sem, r)
    True
    """
    cols = osem.lem1_cols() + osem.lemn_cols() + tsem.lem1_cols() + tsem.lemn_cols()
    return any(_hilited(row, c) for c in cols)


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


def _expand_special_char(sem: LangSemantics, row: List[str]) -> List[str]:
    """
    *IN_PLACE*

    >> sl_sem = MainLangSemantics("sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3]))
    >>> sl_sem = VarLangSemantics("sl", 0, [1, 2, 3], None)
    >>> _expand_special_char(sl_sem, ["word", "lemma", "*", ""])
    ['word', 'lemma', '* lemma', '']
    >>> _expand_special_char(sl_sem, ["word", "lemma", "* l2", ""])
    ['word', 'lemma', '* l2', '']
    """
    if row[sem.lemmas[1]] in SPECIAL_CHARS:
        row[sem.lemmas[1]] = f"{row[sem.lemmas[1]]} {row[sem.lemmas[0]]}"
    return row


def _close(
    group: List[List[str]],
    orig: LangSemantics,
    trans: LangSemantics,
    incl_hilited: bool = False,
) -> List[List[str]]:
    """Wraps up a group that is currently being read.
    Redistributes content according to desired (complex) logic
    """
    if not group:
        return []

    # locate index
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

    # only lines without highlited lemmas, i.e. gramm. annotation
    merge_rows = [i for i, r in enumerate(group) if not _hilited_lemma(orig, trans, r)]
    merge_group = [group[i] for i in merge_rows]

    # collect content
    line = [""] * STYLE_COL

    line[orig.word] = orig.collect_word(group)
    line[trans.word] = trans.collect_word(group)

    line[orig.other().word] = orig.other().collect_word(group)
    # assert trans.var  # for mypy
    line[trans.other().word] = trans.other().collect_word(group)

    line[orig.other().lemmas[0]] = orig.other().collect_lemma(
        merge_group, orig.other().lemmas[0]
    )

    for c in trans.lem1_cols():
        line[c] = trans.collect_lemma(merge_group, c, V_LEMMA_SEP)
    for c in orig.lemn_cols() + trans.lemn_cols():
        line[c] = trans.collect_lemma(merge_group, c)

    # update content
    for i in range(len(group)):
        for c in orig.word_cols():
            group[i][c] = line[c]
        if incl_hilited or not _hilited_lemma(orig, trans, group[i]):
            group[i][IDX_COL] = idx.longstr()
            for c in orig.lemn_cols():
                group[i][c] = line[c]
            group[i][orig.other().lemmas[0]] = line[orig.other().lemmas[0]]
        for c in trans.cols():
            if i in merge_rows or c in trans.word_cols():
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
    corpus: List[List[str]],
    orig: MainLangSemantics,
    trans: MainLangSemantics,
    incl_hilited: bool = False,
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

        row = _expand_special_char(orig, row)
        row = _expand_special_char(trans, row)

        if _grouped(row, orig) or _grouped(row, trans):
            group.append(row)
        else:
            if group:
                group = _close(group, orig, trans, incl_hilited)
                result += group
                group = []
            result.append(row)

    if group:
        group = _close(group, orig, trans, incl_hilited)
        result += group

    return result
