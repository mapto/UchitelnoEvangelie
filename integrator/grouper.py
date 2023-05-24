from typing import Dict, List, Set
import logging as log

from const import H_LEMMA_SEP, IDX_COL, STYLE_COL, V_LEMMA_SEP

from model import Index, Source
from semantics import LangSemantics, MainLangSemantics, present
from hiliting import Hiliting, _hilited_col, _hilited_gram, _hilited_union


def _group_variants(group: List[List[str]], sem: LangSemantics) -> Source:
    """Returns a list of variants (excluding main) that are present in this group"""
    variants = set()
    assert sem.var  # for mypy
    for row in group:
        for var in [k for k, val in sem.var.multiword(row).items() if val]:
            variants.add(var)
    return Source("".join(str(v) for v in variants).strip())


def _merge_indices(group: List[List[str]]) -> Index:
    """Merge the individual indices of a group into a group/multiline index"""
    s_start = None
    s_end = None

    for r in group:
        if r[IDX_COL]:
            if not s_start or r[IDX_COL] < s_start:
                s_start = r[IDX_COL]
            if not s_end or r[IDX_COL] > s_end:
                s_end = r[IDX_COL]

    assert s_start
    return Index(f"{s_start}-{s_end}") if s_start != s_end else Index(s_start)


# TODO
def _collect_main(
    group: List[List[str]],
    osem: LangSemantics,
    h: Hiliting,
    line: List[str],
):
    """*IN_PLACE*"""
    line[osem.word] = osem.collect_word(group)
    line[osem.lemmas[1]] = osem.collect_lemma(h.non_union_group, osem.lemmas[1])
    for c in osem.lemmas[2:]:
        line[c] = osem.collect_lemma(h.non_gram_group, c)


# TODO
def _collect_other(
    group: List[List[str]],
    orig: LangSemantics,
    h: Hiliting,
    line: List[str],
):
    """*IN_PLACE*"""
    line[orig.other().word] = orig.other().collect_word(group)
    # TODO: which trans should orig other depend on?
    # TODO: first lemma should be with V_LEMMA_SEP?
    line[orig.other().lemmas[0]] = orig.other().collect_lemma(
        h.non_gram_group, orig.other().lemmas[0]
    )
    for c in orig.other().lemmas[1:]:
        line[c] = orig.collect_lemma(h.non_gram_group, c)


def _collect_trans(
    group: List[List[str]],
    tsem: LangSemantics,
    h: Hiliting,
    line: List[str],
):
    """*IN_PLACE*"""
    line[tsem.word] = tsem.collect_word(group)
    line[tsem.lemmas[0]] = tsem.collect_lemma(
        h.non_gram_group, tsem.lemmas[0], V_LEMMA_SEP
    )
    line[tsem.lemmas[1]] = tsem.collect_lemma(h.non_union_group, tsem.lemmas[1])
    for c in tsem.lemmas[2:]:
        line[c] = tsem.collect_lemma(h.non_gram_group, c)
    return line


def _collect_group(
    group: List[List[str]], orig: LangSemantics, trans: MainLangSemantics, h: Hiliting
) -> List[str]:
    """Creates an combined line, based on lemma highlighting in group.
    This is later to be inserted in the lines making part of the group"""

    line = [""] * STYLE_COL

    # Words from any type of highlighting are added to the merged line
    # line = _collect_main(group, orig, non_gram_group_main, non_union_group_main, line)
    line[orig.word] = orig.collect_word(group)
    line[orig.lemmas[1]] = orig.collect_lemma(h.non_union_group, orig.lemmas[1])
    for c in orig.lemmas[2:]:
        line[c] = orig.collect_lemma(h.non_gram_group, c)

    # line = _collect_other(group, orig.other(), non_gram_group_main, non_union_group_main, line)
    line[orig.other().word] = orig.other().collect_word(group)
    line[orig.other().lemmas[0]] = orig.other().collect_lemma(
        group, orig.other().lemmas[0]  # , V_LEMMA_SEP
    )
    for c in orig.other().lemmas[1:]:
        line[c] = orig.other().collect_lemma(h.non_gram_group, c)

    line = _collect_trans(group, trans, h, line)
    line = _collect_trans(group, trans.other(), h, line)

    return line


def _needs_update(
    group: List[List[str]],
    orig: LangSemantics,
    trans: LangSemantics,
    i: int,
    c: int,
    h: Hiliting,
):
    if c in trans.lemmas and _hilited_gram(orig, trans, group[i]):
        return False
    if i in h.merge_rows or c == trans.word:
        if _hilited_union(orig, trans, group[i], c):
            return False
    return True


def _update_group(
    g: List[List[str]],
    orig: LangSemantics,
    trans: MainLangSemantics,
    line: List[str],
    h: Hiliting,
) -> List[List[str]]:
    """Update group content with the collected information"""
    idx = _merge_indices(g)

    group = g.copy()
    for i in range(len(group)):
        if not _hilited_gram(orig, trans, group[i]):
            group[i][IDX_COL] = idx.longstr()

        for c in orig.word_cols():
            group[i][c] = line[c]
        if not _hilited_gram(orig, trans, group[i]):
            for c in orig.lemn_cols():
                if not _hilited_union(orig, trans, group[i], c):
                    group[i][c] = line[c]
            group[i][orig.other().lemmas[0]] = line[orig.other().lemmas[0]]

        for c in trans.cols():
            # do not update lines that have union highlighting in translation
            update = _needs_update(group, orig, trans, i, c, h)
            if group[i][trans.other().word]:
                update &= _needs_update(group, orig, trans.other(), i, c, h)
            if update:
                group[i][c] = line[c]

    return group


def _collect_missing_var_lemma(
    group: List[List[str]], orig: LangSemantics, row: List[str], v: Source
) -> str:
    collected = [orig.multilemma(r) for r in group]
    addition: Set[str] = set()
    for r in collected:
        for s, l in r.items():
            if s in v:
                addition.add(f"{l} {s}")

    syntetic_rows = [[""] * STYLE_COL for i in range(len(addition) + 1)]
    for i, a in enumerate(addition):
        syntetic_rows[i][orig.lemmas[0]] = a
    syntetic_rows[-1][orig.lemmas[0]] = row[orig.lemmas[0]]
    return orig.collect_lemma(syntetic_rows, orig.lemmas[0], H_LEMMA_SEP)


def _close_group(
    group: List[List[str]], orig: LangSemantics, trans: MainLangSemantics, h: Hiliting
) -> List[List[str]]:
    """Close a group formed by highlighting."""
    assert orig.main  # for mypy
    variants = _group_variants(group, orig.main)
    if variants:
        for row in group:
            # populate variants equal to main
            if (
                present(row, orig.other())
                and row[orig.word]
                and not row[orig.other().word]
            ):
                row[orig.other().word] = f"{row[orig.word]} {variants}"
            # populate variants in lemma from word, if left implicit
            elif orig == orig.var and row[orig.lemmas[0]]:
                ml = orig.multilemma(row).keys()
                mw = orig.multiword(row).keys()
                lv = str(next(iter(ml)))
                wv = str(next(iter(mw)))
                if (
                    len(mw) == len(ml) == 1
                    and ml == mw
                    and not row[orig.lemmas[0]].endswith(lv)
                ):
                    row[orig.lemmas[0]] = f"{row[orig.lemmas[0]]} {wv}"
                    ml = orig.multilemma(row).keys()
                mls = Source([str(s) for s in ml])
                if mls in variants:
                    v = variants - mls
                    row[orig.lemmas[0]] = _collect_missing_var_lemma(
                        group, orig, row, v
                    )

    line = _collect_group(group, orig, trans, h)
    try:
        return _update_group(group, orig, trans, line, h)
    except Exception as e:
        log.error(
            f"Неуспешно затваряне на група при редове {[row[IDX_COL] for row in group]}"
        )
        log.error(e)
        return []


def _hilited(row: List[str], sem: LangSemantics) -> Dict[int, str]:
    """Returns if the row takes part of a group with respect to this language (and its variants).
    The result indicates which column is highlited (change in highlited column results in change of group

    >>> from semantics import VarLangSemantics
    >>> sl = MainLangSemantics("sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3]))
    >>> r = [""] * 4 + ["02/W169b26", "на", "ма же \ue201д\ue205нь ѿ ѡбою на де-", "на", "на + Loc."] + [""] * 17 + ["hl00:CCCCCCCC|hl05:AAAAAAAA|hl11:BBBBBBBB|bold|italic"]
    >>> _hilited(r, sl)
    {5: 'AAAAAAAA', 0: 'CCCCCCCC'}
    >>> sg = MainLangSemantics("gr", 11, [12, 13, 14, 15], VarLangSemantics("gr", 16, [17, 18, 19, 20]))

    >>> _hilited(r, sg)
    {11: 'BBBBBBBB'}
    """
    result = {}
    v = _hilited_col(row, sem.word)
    if v:
        result[sem.word] = v
    v = _hilited_col(row, sem.other().word)
    if v:
        result[sem.other().word] = v
    return result
