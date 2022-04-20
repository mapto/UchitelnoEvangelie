from typing import Dict, List
from dataclasses import dataclass, field
from sortedcontainers import SortedDict  # type: ignore

from const import IDX_COL, EXAMPLE_COL, STYLE_COL
from util import ord_word

from .lang import LangSemantics


@dataclass
class TableSemantics:
    """Overall table column mapping"""

    orig: LangSemantics
    trans: LangSemantics
    idx: int = IDX_COL
    example: int = EXAMPLE_COL  # actually not used
    style: int = STYLE_COL
    label: str = ""
    result: SortedDict = field(default_factory=lambda: SortedDict(ord_word))

    def cols(self) -> List[int]:
        """extract word and lemma columns"""
        c = []
        c += self.orig.cols()
        c += self.trans.cols()
        return c

    def word_cols(self) -> List[int]:
        """extract word columns"""
        c = []
        c += self.orig.word_cols()
        c += self.trans.word_cols()
        return c

    def lem1_cols(self) -> List[int]:
        """extract first lemma columns"""
        c = []
        c += self.orig.lem1_cols()
        c += self.trans.lem1_cols()
        return c

    def lemn_cols(self) -> List[int]:
        """extract word and lemma columns"""
        c = []
        c += self.orig.lemn_cols()
        c += self.trans.lemn_cols()
        return c
