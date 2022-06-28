#!/usr/bin/env python3

"""A processor merging multiple lines when they are related.
Takes care of construct grouping and repeated words counting"""

from typing import Dict, List

from const import IDX_COL, SAME_CH, SPECIAL_CHARS

from semantics import LangSemantics, MainLangSemantics, present
from util import clean_word
from grouper import _close_group, _hilited

TRIGGER_SAME = ""


def _expand_special_char(sem: LangSemantics, row: List[str]) -> List[str]:
    """*IN_PLACE*"""
    if row[sem.lemmas[1]].strip() in SPECIAL_CHARS:
        row[sem.lemmas[1]] = f"{row[sem.lemmas[1]]} {row[sem.lemmas[0]]}"
    return row


def _close_same(
    group: List[List[str]],
    orig: LangSemantics,
    trans: LangSemantics,
) -> List[List[str]]:
    if group[1][trans.word] == SAME_CH:
        group[1][trans.word] = group[0][trans.word]
    if group[1][orig.word] == SAME_CH:
        group[1][orig.word] = group[0][orig.word]
    return [group[1]]


def _close(
    group: List[List[str]],
    orig: LangSemantics,
    trans: MainLangSemantics,
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
                f"WARNING: липсва индекс в първия ред от група на {group[0][IDX_COL]}. Намерен в {idxline} ред"
            )
        else:
            for row in group:
                print(row)
            print(f"ГРЕШКА: липсва индекс в групата.")

    if _same(group[-1], trans) or _same(group[-1], orig):
        assert len(group) == 2
        # print(group)
        return _close_same(group, orig, trans)
    return _close_group(group, orig, trans)


def _same(row: List[str], sem: LangSemantics) -> bool:
    """Returns if the word is "=", meaning that it is the same as the previous row (for this direction of translation)"""
    if row[sem.word].strip() == SAME_CH:
        return True
    return False


def merge(
    corpus: List[List[str]],
    orig: LangSemantics,
    trans: MainLangSemantics,
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

    row_owords: Dict[str, int] = {}
    row_owords_var: Dict[str, int] = {}
    row_twords: Dict[str, int] = {}
    row_twords_var: Dict[str, int] = {}
    cur_idx = ""
    prev_row: List[str] = []
    group_triggers: List[str] = []

    for raw in corpus:
        try:
            row = [clean_word(v) if v else "" for v in raw]

            # if "19/94d08" in row[IDX_COL] or "2/W169a17" in row[IDX_COL]:
            # if "05/28c21" in row[IDX_COL] or "05/28d01" in row[IDX_COL]:
            # if "14/72d1" in row[IDX_COL]:
            # print(row)

            if not row[IDX_COL] and any(row):
                row[IDX_COL] = group[-1][IDX_COL] if group else result[-1][IDX_COL]

            # in lemmas
            row = _expand_special_char(orig, row)
            row = _expand_special_char(trans, row)

            if cur_idx != row[IDX_COL]:
                cur_idx = row[IDX_COL]
                row_owords = {}
                row_owords_var = {}
                row_twords = {}
                row_twords_var = {}

            # based on word column expand data with it with count in a column at the end
            row_owords = orig.add_count(row, row_owords)
            row_owords_var = orig.other().add_count(row, row_owords_var)
            row_twords = trans.add_count(row, row_twords)
            row_twords_var = trans.other().add_count(row, row_twords_var)

            hi = {**_hilited(row, orig), **_hilited(row, trans)}
            # print(f"{row[IDX_COL]}: {hi}")

            if _same(row, orig) or _same(row, trans) and not group_triggers:
                group = [prev_row]
                group_triggers += [TRIGGER_SAME]

            if hi and all(t in hi.values() for t in group_triggers):
                group += [row]
                group_triggers = list(hi.values())
            elif (
                _same(row, orig) or _same(row, trans)
            ) and TRIGGER_SAME in group_triggers:
                group += [row]
            else:
                if group:
                    group = _close(group, orig, trans)
                    result += group
                    group = []
                group_triggers = []
                result += [row]
            prev_row = row
            # print(group_triggers)
        except Exception as e:
            print(
                f"ГРЕШКА: При събиране възникна проблем в ред {row[IDX_COL]} ({row[orig.word]}/{row[trans.word]}) или групата му"
            )
            print(e)
            break
    if group:
        group = _close(group, orig, trans)
        result += group

    return result
