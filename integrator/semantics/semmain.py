"""Functions for MainLangSemantics"""

from typing import Dict, List, Tuple

from const import NON_COUNTABLE, ERR_SUBLEMMA
from const import MISSING_CH, SPECIAL_CHARS
from const import OMMIT_SUBLEMMA
from model import Source

from .const import LAST_LEMMA
from .util import collect


def collect_word(self, group: List[List[str]]) -> str:
    return " ".join(collect(group, self.word))


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
) -> Tuple[Dict[Source, str], Dict[Source, Tuple[str, int]]]:
    """
    Get alternative words and lemmas, ignoring variants that coincide with main.
    my_var is ignored, because it is MainLangSemantics.
    """
    # print(my_var, lidx)
    assert self.var  # for mypy
    alt_lemmas = {
        k: v
        for k, v in self.var.multilemma(row, lidx).items()
        if v != row[self.lemmas[lidx]]
    }
    # Get interpretative annotation from sublemma if any
    if lidx == 0 and len(self.var.lemmas) > 1:
        l2 = self.var.multilemma(row, 1)
        for k2, v2 in l2.items():
            for prefix in SPECIAL_CHARS + [ERR_SUBLEMMA]:
                if v2.startswith(prefix):
                    for k1 in alt_lemmas.keys():
                        if k1.inside(k2):
                            alt_lemmas[k1] = f"{prefix} {alt_lemmas[k1]}"
                    break

    aw = {l: self.var.compile_words_by_lemma(row, l) for l in alt_lemmas.keys()}
    alt_words = {l: (v[0], v[1]) for l, v in aw.items()}
    if Source() in alt_lemmas:
        alt_lemmas[Source("".join(str(s) for s in alt_words.keys()))] = alt_lemmas[
            Source()
        ]
        alt_lemmas.pop(Source())
        alt_words.pop(Source())

    # print(alt_lemmas, alt_words)
    return alt_lemmas, alt_words


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
