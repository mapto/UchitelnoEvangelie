"""Functions for MainLangSemantics"""

from typing import Dict, List, Tuple

from const import NON_COUNTABLE
from const import MISSING_CH, SAME_CH, SPECIAL_CHARS
from const import OMMIT_SUBLEMMA
from model import Alternative, Source

from .const import LAST_LEMMA
from .util import collect


def collect_word(self, group: List[List[str]]) -> str:
    g = [e for e in collect(group, self.word) if e != SAME_CH]
    return " ".join(g)


def collect_lemma(self, group: List[List[str]], cidx: int, separator: str = "") -> str:
    g = [e for e in collect(group, cidx) if e.strip() != MISSING_CH]
    # do not repeat om.
    if g.count(OMMIT_SUBLEMMA) > 1:
        g = [
            e for i, e in enumerate(g) if e != OMMIT_SUBLEMMA or i > 0 or e != g[i - 1]
        ]
    if separator:
        return f" {separator} ".join(g)
    return f" ".join(g)


def level_var_alternatives(
    self, row: List[str], my_var: Source, lidx: int = 0
) -> Dict[Source, Alternative]:
    """
    Get alternative words and lemmas, ignoring variants that coincide with main.
    my_var is ignored, because it is MainLangSemantics.
    returns two dictionaries:
        for lemmas: Source->lemma
        for words: Source->(word, repetition count)
    """
    # print(my_var, lidx)
    assert self.var, "non-null value required by mypy"
    # print(self.var.multilemma(row, lidx))
    # print(row[self.lemmas[lidx]])
    alt_lemmas = {
        k: v
        for k, v in self.var.multilemma(row, lidx).items()
        if v != row[self.lemmas[lidx]] or v in SPECIAL_CHARS
    }

    # Get interpretative annotation (semantics) from sublemma if any
    # print(lidx, self.var.lemmas)
    semantics = {}
    # if lidx == 0 and len(self.var.lemmas) > 1:
    l2 = self.var.multilemma(row, lidx)
    for k2, v2 in l2.items():
        for prefix in SPECIAL_CHARS:
            if v2.startswith(prefix):
                semantics[k2] = prefix
                break

    aw = {l: self.var.compile_words_by_lemma(row, l) for l in alt_lemmas.keys()}
    alt_words = {l: (v[0], v[1]) for l, v in aw.items()}
    if Source() in alt_lemmas:
        src = Source("".join(str(s) for s in alt_words.keys()))
        alt_lemmas[src] = alt_lemmas[Source()]
        alt_lemmas.pop(Source())
        alt_words.pop(Source())

    result: Dict[Source, Alternative] = {}
    for wk, (wv, wc) in alt_words.items():
        # print(wk, alt_lemmas, wk in alt_lemmas)
        if wk in alt_lemmas:
            sem = semantics[wk] if wk in semantics else ""
            assert (
                not sem or alt_lemmas[wk][0] == sem
            ), f"Mismatch between semantic {sem} and lemmas {alt_lemmas} with variant {wk}"
            lem = alt_lemmas[wk][2:] if sem else alt_lemmas[wk]
            result[wk] = Alternative(wv, lem, wc, sem)
        else:
            # expected that several words have same lemma so their sources are merged
            for lk, lv in alt_lemmas.items():
                if lk.inside(wk) and lk not in result:
                    assert (
                        not semantics[lk] or lv[0] == semantics[lk]
                    ), f"Mismatch between semantics {semantics} and lemmas {alt_lemmas} with variant {lk}"
                    lem = lv[2:] if semantics[lk] else lv
                    result[lk] = Alternative(wv, lem, wc, semantics[lk])
    # print(result)
    return result


def multiword(self, row: List[str]) -> Dict[Source, str]:
    """Main variant does not have multiple words in a cell"""
    return {Source(""): row[self.word].strip()}


def multilemma(self, row: List[str], lidx: int = 0) -> Dict[Source, str]:
    """Main variant does not have multiple words in a cell"""
    if lidx == LAST_LEMMA:
        lidx = len(self.lemmas) - 1
        # print(lidx)
        # print(self.lemmas)
        # print(row)
        while not row[self.lemmas[lidx]]:
            lidx -= 1
        return self.multilemma(row, lidx)
    if not row[self.lemmas[lidx]].strip():
        return {}
    return {Source(""): row[self.lemmas[lidx]].strip()}


def compile_words_by_lemma(
    self, row: List[str], var: Source = Source()
) -> Tuple[str, int]:
    return (row[self.word], int(row[self.cnt_col]))


def add_count(self, row: List[str], row_counts: Dict[str, int]) -> Dict[str, int]:
    """based on first lemma (in column) expand row with counter
    *IN PLACE*
    Updates both row and row_counts"""
    if not self.cnt_col:
        self.cnt_col = len(row)
    while len(row) < self.cnt_col + 1:
        row += ["1"]

    if not row[self.lemmas[0]] or row[self.lemmas[0]] in NON_COUNTABLE:
        return row_counts
    if row[self.lemmas[0]] in row_counts:
        row_counts[row[self.lemmas[0]]] += 1
        row[self.cnt_col] = str(row_counts[row[self.lemmas[0]]])
    else:
        row_counts[row[self.lemmas[0]]] = 1
        # fallback to default value for cnt in Index
    return row_counts
