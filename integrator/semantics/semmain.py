"""Functions for MainLangSemantics"""

from typing import Dict, List, Tuple

from const import NON_COUNTABLE
from const import MISSING_CH, SAME_CH
from const import OMMIT_SUBLEMMA
from model import Source

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
