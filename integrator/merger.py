#!/usr/bin/env python3

"""A processor merging multiple lines when they are related.
Takes care of construct grouping and repeated words counting"""

from typing import Dict, List, Set
import logging as log

from const import IDX_COL, SAME_CH, SPECIAL_CHARS

from semantics import LangSemantics, MainLangSemantics, present
from util import clean_word
from repetition import Repetitions
from grouper import _close_group, _hilited

TRIGGER_SAME = -1


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
    Redistributes content according to desired (complex) logic.
    Does nothing if group empty, so if added to a list, it adds nothing.
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
            log.info(
                f"Липсва индекс в първия ред от група на {group[0][IDX_COL]}."
                f" Намерен в {idxline} ред"
            )
        else:
            for row in group:
                log.info(row)
            log.error(f"Липсва индекс в групата.")

    same = _same(group[-1], trans) or _same(group[-1], orig)
    assert not same or len(group) == 2
    close_fn = _close_same if same else _close_group
    return close_fn(group, orig, trans)


def _same(row: List[str], sem: LangSemantics) -> bool:
    """Returns if the word is "=", meaning that it is the same as the previous row (for this direction of translation)"""
    return row[sem.word].strip() == SAME_CH


def preprocess(
    row: List[str],
    group: List[List[str]],
    prev_row: List[str],
    orig: LangSemantics,
    trans: MainLangSemantics,
    repetitions: Repetitions,
) -> List[str]:
    """repetitinos updated *IN_PLACE*"""

    if not row[IDX_COL] and any(row):
        # print(row, group)
        if group and group[-1][IDX_COL]:
            row[IDX_COL] = group[-1][IDX_COL]
        elif prev_row and prev_row[IDX_COL]:
            row[IDX_COL] = prev_row[IDX_COL]
        else:
            log.info(row)
            log.error(f"Липсва индекс за ред.")

    # in lemmas
    row = _expand_special_char(orig, row)
    row = _expand_special_char(trans, row)

    repetitions.update(row)

    return row


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

    # handles repeating lemmas with same address
    repetitions = Repetitions(orig, trans)
    prev_row: List[str] = []
    # triggers ignore hiliting colours
    group_triggers: Set[int] = set()

    for raw in corpus:
        try:
            row = [clean_word(v) if v else "" for v in raw]

            # if "19/94d08" in row[IDX_COL] or "2/W169a17" in row[IDX_COL]:
            # if "05/28c21" in row[IDX_COL] or "05/28d01" in row[IDX_COL]:
            # if "18/89c21" in row[IDX_COL]:
            #     print(row)

            row = preprocess(row, group, prev_row, orig, trans, repetitions)

            if _same(row, orig) or _same(row, trans):
                if not group_triggers:
                    group = [prev_row]
                group += [row]
                prev_row = row
                continue

            hi = {**_hilited(row, orig), **_hilited(row, trans)}
            if hi:
                if not any(t in hi.keys() for t in group_triggers):
                    result += _close(group, orig, trans)
                    group = []

                group += [row]
            else:
                result += _close(group, orig, trans) + [row]
                group = []

            group_triggers = set(hi.keys())
            prev_row = row
        except Exception as e:
            log.error(
                "При събиране възникна проблем в ред "
                f"{row[IDX_COL]} ({row[orig.word]}/{row[trans.word]})"
                " или групата му"
            )
            log.error(e)
            break
    result += _close(group, orig, trans)

    return result
