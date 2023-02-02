from typing import Dict, List, Optional
import logging as log

from const import IDX_COL, STYLE_COL, V_LEMMA_SEP

from model import Index, Source
from semantics import LangSemantics, MainLangSemantics, present


def _hilited_col(row: List[str], col: int) -> Optional[str]:
    """highlighting implemented via background colour.
    If column visibly highlighted, return its non-white color, else None

    >>> r = [""] * 4 + ["02/W169b26", "на", "ма же \ue201д\ue205нь ѿ ѡбою на де-", "на", "на + Loc."] + [""] * 17 + ["hl00:FFFFFFFF|hl05:AAAAAAAA|hl08:BBBBBBBB|bold|italic"]
    >>> _hilited_col(r, 5)
    'AAAAAAAA'
    >>> _hilited_col(r, 8)
    'BBBBBBBB'
    >>> _hilited_col(r, 9)
    >>> _hilited_col(r, 0)
    """
    style = row[STYLE_COL]
    if f"hl{col:02d}" in style:
        pos = style.index(f"hl{col:02d}")
        # log.debug(style[pos + 5 : pos + 13])
        if style[pos + 5 : pos + 11] == "FFFFFF":
            return None
        return style[pos + 5 : pos + 13]
    return None


def _hilited_gram(osem: LangSemantics, tsem: LangSemantics, row: List[str]) -> bool:
    """highlighting in third lemma and further.
    This highlighting has impact on variants. If undesired better create separate rows in variants."""
    cols = [
        osem.lemmas[2],
        osem.other().lemmas[2],
        tsem.lemmas[2],
        tsem.other().lemmas[2],
    ]
    return any(_hilited_col(row, c) for c in cols)


def _hilited_union(
    osem: LangSemantics, tsem: LangSemantics, row: List[str], col: int = -1
) -> bool:
    """highlighting in second lemma. Also checks if passed column is in second lemma, if passed at all"""
    cols = [osem.lemmas[1], tsem.lemmas[1]]
    if col != -1 and col not in cols:
        return False
    return any(_hilited_col(row, c) for c in cols)


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


def _collect_group(
    group: List[List[str]],
    orig: LangSemantics,
    trans: MainLangSemantics,
    merge_rows_main: List[int],
    merge_rows_var: List[int],
) -> List[str]:
    """Creates an combined line, based on lemma highlighting in group"""
    non_gram_group_main = [group[i] for i in merge_rows_main]
    non_gram_group_var = [group[i] for i in merge_rows_var]
    non_union_group_main = [
        r for r in non_gram_group_main if not _hilited_union(orig, trans, r)
    ]
    non_union_group_var = (
        [r for r in non_gram_group_var if not _hilited_union(orig, trans.var, r)]
        if trans.var
        else []
    )

    line = [""] * STYLE_COL

    # Words from any type of highlighting are added to the merged line
    line[orig.word] = orig.collect_word(group)
    line[trans.word] = trans.collect_word(group)

    line[orig.other().word] = orig.other().collect_word(group)
    line[trans.other().word] = trans.other().collect_word(group)

    # TODO: which trans should orig other depend on?
    line[orig.other().lemmas[0]] = orig.other().collect_lemma(
        non_gram_group_main, orig.other().lemmas[0]
    )

    line[trans.lemmas[0]] = trans.collect_lemma(
        non_gram_group_main, trans.lemmas[0], V_LEMMA_SEP
    )
    if trans.var:
        line[trans.var.lemmas[0]] = trans.var.collect_lemma(
            non_gram_group_var, trans.var.lemmas[0], V_LEMMA_SEP
        )

    for c in orig.lemn_cols()[1:] + trans.lemmas[1:]:
        line[c] = trans.collect_lemma(non_gram_group_main, c)
    if trans.var:
        for c in trans.var.lemmas[1:]:
            line[c] = trans.var.collect_lemma(non_gram_group_var, c)

    for c in [orig.lemmas[1], trans.lemmas[1]]:
        line[c] = trans.collect_lemma(non_union_group_main, c)
    if trans.var:
        line[trans.var.lemmas[1]] = trans.var.collect_lemma(
            non_union_group_var, trans.var.lemmas[1]
        )
    return line


def _update_group(
    g: List[List[str]],
    orig: LangSemantics,
    trans: MainLangSemantics,
    line: List[str],
    merge_rows_main: List[int],
    merge_rows_var: List[int],
) -> List[List[str]]:

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
            update = True
            if c in trans.lemmas and _hilited_gram(orig, trans, group[i]):
                update = False
            if i in merge_rows_main or c == trans.word:
                if _hilited_union(orig, trans, group[i], c):
                    update = False
            # log.debug(trans.var, merge_rows_var)
            if trans.var and group[i][trans.var.word]:
                if c in trans.var.lemmas and _hilited_gram(orig, trans.var, group[i]):
                    update = False
                if i in merge_rows_var or c == trans.var.word:
                    if _hilited_union(orig, trans.var, group[i], c):
                        update = False
            if update:
                group[i][c] = line[c]

    return group


def _close_group(
    group: List[List[str]],
    orig: LangSemantics,
    trans: MainLangSemantics,
) -> List[List[str]]:
    """Close a group formed by highlighting."""
    # populate variants equal to main
    assert orig.main  # for mypy
    variants = _group_variants(group, orig.main)
    assert orig.var  # for mypy
    if variants:
        for row in group:
            if present(row, orig.var) and row[orig.word] and not row[orig.var.word]:
                row[orig.var.word] = f"{row[orig.word]} {variants}"

    # only lines without highlited lemmas, i.e. gramm. annotation or union annotation
    merge_rows_main = [
        i for i, r in enumerate(group) if not _hilited_gram(orig, trans, r)
    ]
    merge_rows_var = (
        [i for i, r in enumerate(group) if not _hilited_gram(orig, trans.var, r)]
        if trans.var
        else []
    )

    # collect content
    line = _collect_group(group, orig, trans, merge_rows_main, merge_rows_var)

    # update content
    try:
        return _update_group(group, orig, trans, line, merge_rows_main, merge_rows_var)
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
