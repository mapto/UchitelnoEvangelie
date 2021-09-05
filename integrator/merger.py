#!/usr/bin/env python3

from typing import List, Dict

from const import IDX_COL, MISSING_CH, STYLE_COL, V_LEMMA_SEP
from model import Index
from semantics import LangSemantics, MainLangSemantics
from util import ord_word

ord_tuple = lambda x: ord_word(x[0])


def _collect(group: List[List[str]], col: int) -> List[str]:
    return [group[i][col] for i in range(len(group)) if group[i][col]]


def _highlighted(group: List[List[str]], col: int) -> bool:
    """
    >>> group = [['все WH', 'вьсь', '', '1/7c12', 'въ', 'въ сел\ue205ко', 'въ', 'въ + Acc.', '', '', 'εἰς', 'εἰς', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl07|hl10'], ['\ue201л\ue205ко WH', '\ue201л\ue205къ', '', '1/7c12', 'сел\ue205ко', 'въ сел\ue205ко', 'сел\ue205къ', '', '', '', 'τοῦτο', 'οὗτος', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10']]
    >>> _highlighted(group, 7)
    True
    """
    for i in range(len(group)):
        if f"hl{col:02d}" in group[i][STYLE_COL]:
            return True
    return False


def _close(
    group: List[List[str]], orig: LangSemantics, trans: LangSemantics
) -> List[List[str]]:
    """*IN_PLACE*"""
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

    s_end = None
    for i in range(len(group) - 1, 0, -1):
        s_end = group[i][IDX_COL]
        if s_end:
            break
    if not s_end:
        s_end = group[0][IDX_COL]
    idx = Index.unpack(f"{group[0][IDX_COL]}-{s_end}")

    # collect content
    line = [""] * STYLE_COL
    for c in orig.word_cols() + trans.word_cols():
        line[c] = " ".join(_collect(group, c))
    for c in trans.lem1_cols():
        g = [e for e in _collect(group, c) if e.strip() != MISSING_CH]
        line[c] = f" {V_LEMMA_SEP} ".join(g)
    for c in orig.lemn_cols() + trans.lemn_cols():
        line[c] = " ".join(_collect(group, c))

    # update content
    for i in range(len(group)):
        group[i][IDX_COL] = idx.longstr()
        for c in orig.word_cols() + trans.cols():
            group[i][c] = line[c]
        for c in orig.lemn_cols():
            if not _highlighted(group, c):
                group[i][c] = line[c]

    return group


def _grouped(row: List[str], sem: MainLangSemantics) -> bool:
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
