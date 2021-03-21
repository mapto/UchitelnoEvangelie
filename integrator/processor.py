#!/usr/bin/env python3

from typing import List, Tuple, Optional
import unicodedata
from sortedcontainers import SortedDict, SortedSet  # type: ignore
import re

from const import IDX_COL, STYLE_COL, H_LEMMA_SEP, V_LEMMA_SEP, PATH_SEP
from model import Index, LangSemantics
from util import ord_word, base_word

ord_tuple = lambda x: ord_word(x[0])


def expand_idx(corpus: List[List[str]]) -> List[List[str]]:
    """*IN_PLACE*"""
    for row in corpus:
        if row[IDX_COL]:
            row[IDX_COL] = Index.unpack(row[IDX_COL]).longstr()
    return corpus


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
    """*IN_PLACE*

    >>> sl_sem = LangSemantics(lang='sl', word=4, lemmas=[6, 7, 8, 9], var=LangSemantics(lang='sl_var', word=0, lemmas=[1, 2, 19, 20], var=None))
    >>> gr_sem = LangSemantics(lang='gr', word=10, lemmas=[11, 12, 13], var=LangSemantics(lang='gr_var', word=15, lemmas=[16, 17, 19], var=None))
    >>> group = [['все WH', 'вьсь', '', '1/7c12', 'въ', 'въ сел\ue205ко', 'въ', 'въ + Acc.', '', '', 'εἰς', 'εἰς', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10'], ['\ue201л\ue205ко WH', '\ue201л\ue205къ', '', '1/7c12', 'сел\ue205ко', 'въ сел\ue205ко', 'сел\ue205къ', '', '', '', 'τοῦτο', 'οὗτος', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10']]
    >>> _close(group, gr_sem, sl_sem)
    [['все WH \ue201л\ue205ко WH', 'вьсь & \ue201л\ue205къ', '', '01/007c12', 'въ сел\ue205ко', 'въ сел\ue205ко', 'въ & сел\ue205къ', 'въ + Acc.', '', '', 'εἰς τοῦτο', 'εἰς', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10'], ['все WH \ue201л\ue205ко WH', 'вьсь & \ue201л\ue205къ', '', '01/007c12', 'въ сел\ue205ко', 'въ сел\ue205ко', 'въ & сел\ue205къ', 'въ + Acc.', '', '', 'εἰς τοῦτο', 'οὗτος', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10']]
    >>> group = [['', '', '', '1/5a10', 'беꙁ', 'ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ', 'беꙁ ', 'беꙁ вѣдѣн\ue205ꙗ', '', '', 'ἀπείρως', 'ἀπείρως', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl10'], ['', '', '', '1/5a10', 'вѣдѣн\ue205ꙗ', 'ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ', 'вѣдѣн\ue205\ue201', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl10']]
    >>> _close(group, sl_sem, gr_sem)
    [['', '', '', '01/005a10', 'беꙁ вѣдѣн\ue205ꙗ', 'ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ', 'беꙁ ', 'беꙁ вѣдѣн\ue205ꙗ', '', '', 'ἀπείρως', 'ἀπείρως', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl10'], ['', '', '', '01/005a10', 'беꙁ вѣдѣн\ue205ꙗ', 'ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ', 'вѣдѣн\ue205\ue201', 'беꙁ вѣдѣн\ue205ꙗ', '', '', 'ἀπείρως', 'ἀπείρως', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl10']]
    >>> group = [['все WH', 'вьсь', '', '1/7c12', 'въ', 'въ сел\ue205ко', 'въ', 'въ + Acc.', '', '', 'εἰς', 'εἰς', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl07|hl10'], ['\ue201л\ue205ко WH', '\ue201л\ue205къ', '', '1/7c12', 'сел\ue205ко', 'въ сел\ue205ко', 'сел\ue205къ', '', '', '', 'τοῦτο', 'οὗτος', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10']]
    >>> _close(group, gr_sem, sl_sem)
    [['все WH \ue201л\ue205ко WH', 'вьсь & \ue201л\ue205къ', '', '01/007c12', 'въ сел\ue205ко', 'въ сел\ue205ко', 'въ & сел\ue205къ', 'въ + Acc.', '', '', 'εἰς τοῦτο', 'εἰς', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl07|hl10'], ['все WH \ue201л\ue205ко WH', 'вьсь & \ue201л\ue205къ', '', '01/007c12', 'въ сел\ue205ко', 'въ сел\ue205ко', 'въ & сел\ue205къ', 'въ + Acc.', '', '', 'εἰς τοῦτο', 'οὗτος', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10']]
    >>> group = [['', '', '', '1/5a16', 'ꙁан\ue201', 'еще же \ue205 ꙁан\ue201 въꙁвѣст\ue205лъ', 'ꙁан\ue201', '', '', '', 'διὰ', 'διά ', 'διά + Acc.', 'διὰ τό', '', '', '', '', '', '', '', '', '', 'hl04|hl10|hl12'], ['', '', '', '1/5a16', '', '', '', '', '', '', 'τὸ', 'ὁ', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl10']]
    >>> _close(group, gr_sem, sl_sem)
    [['', '', '', '01/005a16', 'ꙁан\ue201', 'еще же \ue205 ꙁан\ue201 въꙁвѣст\ue205лъ', 'ꙁан\ue201', '', '', '', 'διὰ τὸ', 'διά ', 'διά + Acc.', 'διὰ τό', '', '', '', '', '', '', '', '', '', 'hl04|hl10|hl12'], ['', '', '', '01/005a16', 'ꙁан\ue201', '', 'ꙁан\ue201', '', '', '', 'διὰ τὸ', 'ὁ', '', 'διὰ τό', '', '', '', '', '', '', '', '', '', 'hl04|hl10']]
    >>> group = [['все WH', 'вьсь', '', '1/7c12', 'въ', 'въ сел\ue205ко', 'въ', 'въ + Acc.', '', '', 'εἰς', 'εἰς', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl07|hl10'], ['\ue201л\ue205ко WH', '\ue201л\ue205къ', '', '1/7c12', 'сел\ue205ко', 'въ сел\ue205ко', 'сел\ue205къ', '', '', '', 'τοῦτο', 'οὗτος', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10']]
    >>> _close(group, sl_sem, gr_sem)
    [['все WH \ue201л\ue205ко WH', 'вьсь', '', '01/007c12', 'въ сел\ue205ко', 'въ сел\ue205ко', 'въ', 'въ + Acc.', '', '', 'εἰς τοῦτο', 'εἰς & οὗτος', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl07|hl10'], ['все WH \ue201л\ue205ко WH', '\ue201л\ue205къ', '', '01/007c12', 'въ сел\ue205ко', 'въ сел\ue205ко', 'сел\ue205къ', '', '', '', 'εἰς τοῦτο', 'εἰς & οὗτος', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10']]
    """
    if not group:
        return []

    assert group[0][IDX_COL]
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
        line[c] = " & ".join(_collect(group, c))
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


def _grouped(row: List[str], sem: LangSemantics) -> bool:
    """
    >>> sem = LangSemantics(lang='gr', word=10, lemmas=[11, 12, 13], var=LangSemantics(lang='gr_var', word=15, lemmas=[16, 17, 19], var=None))
    >>> row = ['\ue201л\ue205ко WH', '\ue201л\ue205къ', '', '1/7c12', 'сел\ue205ко', 'въ сел\ue205ко', 'сел\ue205къ', '', '', '', 'τοῦτο', 'οὗτος', '', '', '', '', '', '', '', '', '', '', '', 'hl04|hl00|hl10']
    >>> _grouped(row, sem)
    True

    >>> sem = LangSemantics(lang='sl', word=4, lemmas=[6, 7, 8, 9], var=LangSemantics(lang='sl_var', word=0, lemmas=[1, 2, 19, 20], var=None))
    >>> row = ['', '', '', '1/7d1', 'насъ', 'оу насъ', 'мꙑ', '', '', '', 'om.', 'om.', '', '', '', 'ἡμῖν', 'ἡμεῖς', '', '', '', '', '', '', '']
    >>> _grouped(row, sem)
    False
    >>> row = ['вѣроу GH', 'вѣра', 'вѣрѫ ѩт\ue205', '1/7b19', 'вѣроують', 'вьс\ue205 вѣроують', 'вѣроват\ue205', '', '', '', 'πιστεύσωσι', 'πιστεύω', '', '', '', '', '', '', '', '', '', '', '', 'hl00']
    >>> _grouped(row, sem)
    True
    >>> row = ['\ue205моуть GH', 'ѩт\ue205', '', '1/7b19', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl00']
    >>> _grouped(row, sem)
    True
    """
    if f"hl{sem.word:02d}" in row[STYLE_COL]:
        return True
    if sem.var and f"hl{sem.var.word:02d}" in row[STYLE_COL]:
        return True
    return False


def merge(
    corpus: List[List[str]], orig: LangSemantics, trans: LangSemantics
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


def extract_letters(corpus: List[List[str]], col: int) -> SortedSet:
    letters = SortedSet()
    for row in corpus:
        if row[col]:
            letters = letters.union(
                [ch for ch in unicodedata.normalize("NFKC", row[col].lower())]
            )
            # letters = letters.union([ch for ch in row[col].lower()])
    return {l: ord(l) for l in letters}


def _build_paths(row: List[str], tlem_col: List[int]) -> List[str]:
    """
    >>> _build_paths(['one', 'two', 'three', 'four'], [0, 1, 2, 3])
    ['four >> three >> two >> one']
    >>> _build_paths(['one/two', 'three/four'], [0, 1])
    ['three >> one', 'three >> two', 'four >> one', 'four >> two']
    """
    paths: List[List[str]] = [[]]
    for c in tlem_col:
        bw = base_word(row[c])
        new_paths = []
        for w in bw.split(H_LEMMA_SEP):
            for path in paths:
                n = path.copy()
                n.append(w.strip())
                new_paths.append(n)
        paths = new_paths

    result: List[str] = []
    for cols in paths:
        cols.reverse()
        empty = True
        while empty:
            if not cols[0]:
                cols.pop(0)
                empty = len(cols) > 0
            else:
                empty = False
        result.append(PATH_SEP.join(cols))

    return result


def _compile(val: Index, nxt: str, key: Tuple[str, str], d: SortedDict) -> SortedDict:
    """*IN PLACE*"""
    if nxt in d:
        if key not in d[nxt]:
            d[nxt][key] = SortedSet()
        d[nxt][key].add(val)
    else:
        d[nxt] = {key: SortedSet([val])}
    return d


def _agg_lemma(
    row: List[str],
    col: int,
    orig: LangSemantics,
    trans: LangSemantics,
    key: Tuple[str, str],
    d: SortedDict,
    var: bool = False,
) -> SortedDict:
    """Adds a lemma. Recursion ensures that this works with variable depth.
    
    Args:
        row (List[str]): spreadsheet row
        col (int): lemma column being currently processed
        orig (LangSemantics): original language to iterate through lemma columns
        trans (LangSemantics): translation for lemma columns
        key (Tuple[str, str]): word pair
        d (SortedDict): see return value
        var (bool): variant or not

    Returns:
        SortedDict: *IN PLACE* hierarchical dictionary
    """
    if col == -1:
        assert row[IDX_COL]
        b = "bold" in row[STYLE_COL]
        i = "italic" in row[STYLE_COL]
        val = Index.unpack(row[IDX_COL], b, i, var)
        for nxt in _build_paths(row, trans.lemmas):
            d = _compile(val, nxt, key, d)

    else:
        if var and row[col]:
            row[col] = row[col].replace(H_LEMMA_SEP, V_LEMMA_SEP)
        lemmas = row[col].split(V_LEMMA_SEP) if row[col] else [""]
        lem_col = orig.lemmas
        for l in lemmas:
            next = base_word(l)
            if next not in d:
                d[next] = SortedDict(ord_word)
            next_idx = lem_col.index(col) + 1
            next_c = lem_col[next_idx] if next_idx < len(lem_col) else -1
            d[next] = _agg_lemma(row, next_c, orig, trans, key, d[next], var)

    return d


def _variant(row: List[str], var: Optional[LangSemantics]) -> bool:
    """
    >>> sem = LangSemantics(lang='sl_var', word=0, lemmas=[1, 2, 19, 20], var=None)
    >>> row = ['вѣроу GH', 'вѣра', 'вѣрѫ ѩт\ue205', '1/7b19', 'вѣроують', 'вьс\ue205 вѣроують', 'вѣроват\ue205', '', '', '', 'πιστεύσωσι', 'πιστεύω', '', '', '', '', '', '', '', '', '', '', '', 'hl00']
    >>> _variant(row, sem)
    True
    >>> row = ['\ue205моуть GH', 'ѩт\ue205', '', '1/7b19', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl00']
    >>> _variant(row, sem)
    True
    >>> row = ['\ue205моуть GH', '', '', '1/7b19', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl00']
    >>> _variant(row, sem)
    False

    >>> sem = LangSemantics(lang='gr_var', word=15, lemmas=[16, 17, 19], var=None)
    >>> row = ['вѣроу GH', 'вѣра', 'вѣрѫ ѩт\ue205', '1/7b19', 'вѣроують', 'вьс\ue205 вѣроують', 'вѣроват\ue205', '', '', '', 'πιστεύσωσι', 'πιστεύω', '', '', '', '', '', '', '', '', '', '', '', 'hl00']
    >>> _variant(row, sem)
    False
    >>> row = ['\ue205моуть GH', 'ѩт\ue205', '', '1/7b19', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'hl00']
    >>> _variant(row, sem)
    False
    """
    return not not var and not not row[var.lemmas[0]]


def aggregate(
    corpus: List[List[str]], orig: LangSemantics, trans: LangSemantics
) -> SortedDict:
    """Generate an aggregated index of translations. Recursion ensures that this works with variable depth.

    Args:
        corpus (List[List[str]]): input spreadsheet
        orig (LangSemantics): original language table column mapping
        trans (LangSemantics): translation language table column mapping

    Returns:
        SortedDict: hierarchical dictionary of all lemma levels in original language, that contains rows of the form: translation_lemma: word/tword (index)
    """
    result = SortedDict(ord_word)
    for row in corpus:
        if not row[IDX_COL]:
            continue

        orig_key_var = (
            f" {{{base_word(row[orig.var.word])}}}"
            if _variant(row, orig.var)
            and orig.var  # for mypy
            and orig.var.word  # for mypy
            else ""
        )
        orig_key = base_word(row[orig.word])
        trans_key_var = (
            f" {{{base_word(row[trans.var.word])}}}"
            if _variant(row, trans.var)
            and trans.var  # for mypy
            and trans.var.word  # for mypy
            else ""
        )
        trans_key = base_word(row[trans.word])
        key = (f"{orig_key}{orig_key_var}", f"{trans_key}{trans_key_var}")

        # print(row[IDX_COL])
        # TODO: Do not skip, but collect lemma
        if not [v for v in key if v]:
            continue

        # print(row[IDX_COL])
        result = _agg_lemma(row, orig.lemmas[0], orig, trans, key, result)
        if _variant(row, orig.var):
            assert orig.var  # for mypy
            result = _agg_lemma(
                row, orig.var.lemmas[0], orig.var, trans, key, result, True,
            )

        if _variant(row, trans.var):
            assert trans.var  # for mypy
            result = _agg_lemma(row, orig.lemmas[0], orig, trans.var, key, result, True)
            if _variant(row, orig.var):
                assert orig.var  # for mypy
                result = _agg_lemma(
                    row, orig.var.lemmas[0], orig.var, trans.var, key, result, True,
                )

    return result
