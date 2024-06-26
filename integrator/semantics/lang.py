"""A collection of model classes, specific to the interpretation of the input spreadsheet"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
from sortedcontainers import SortedDict  # type: ignore

from const import IDX_COL, STYLE_COL

from .util import _add_usage
from util import base_word
from model import Alignment, Index, Source, Usage


def present(row: List[str], sem: Optional["LangSemantics"]) -> bool:
    """Not present if not semantics specified or if row misses first lemma according to semantics"""
    return not not sem and bool(row[sem.lemmas[0]])


def _build_content(
    row: List[str], sem: "LangSemantics", var: Source, word: str, cnt: int
) -> Usage:
    main_alt, var_alt = sem.alternatives(row, var)
    lemmas = []
    for lvl in range(0, len(sem.lemmas)):
        found = False
        ml = sem.multilemma(row, lvl)
        # print(ml)
        for k, v in ml.items():
            if not k or var in k:
                lemmas += [v]
                found = True
                break
        if not found:
            lemmas += [""]
    while lemmas and not lemmas[-1]:
        lemmas.pop()
    return Usage(sem.lang, var, word, lemmas, cnt, main_alt, var_alt)


def _is_variant_lemma(
    row: List[str], sem: "LangSemantics", current_var: Source, current_lemma: str
) -> bool:
    mlem = sem.multilemma(row)
    if not mlem:
        return False
    if not sem.is_variant():
        assert (
            not current_var
        ), f"Main variant should not have a source, but is {current_var}"
        assert len(mlem) == 1, f"TODO: multilemmas not yet supported for {mlem}"
        return current_lemma in mlem[Source()]
    loc = current_var.inside(mlem)
    result = loc is not None and current_lemma in mlem[loc]
    return result


@dataclass
class LangSemantics(ABC):
    """Table column mapping for a language."""

    lang: str
    word: int
    lemmas: List[int]

    """Nullable just because recursive reference and setting up needs to happen post-init. Non-null during runtime"""
    var: Optional["VarLangSemantics"] = None
    main: Optional["MainLangSemantics"] = None

    cnt_col: int = 0

    def cols(self) -> List[int]:
        c = []
        c += self.word_cols()
        c += self.lem1_cols()
        c += self.lemn_cols()
        return c

    def word_cols(self) -> List[int]:
        return [self.word, self.other().word]

    def lem1_cols(self) -> List[int]:
        return [self.lemmas[0], self.other().lemmas[0]]

    def lemn_cols(self) -> List[int]:
        """sublemmas (excluding first lemma)"""
        return self.lemmas[1:] + self.other().lemmas[1:]

    @abstractmethod
    def other(self) -> "LangSemantics":
        """For main returns variant, for variant returns main.
        When implementing, be careful not to enter in infinite recursion"""
        raise NotImplementedError("abstract method")

    def is_variant(self) -> bool:
        return False

    @abstractmethod
    def collect_word(self, group: List[List[str]]) -> str:
        raise NotImplementedError("abstract method")

    @abstractmethod
    def collect_lemma(
        self, group: List[List[str]], cidx: int, separator: str = ""
    ) -> str:
        raise NotImplementedError("abstract method")

    @abstractmethod
    def main_alt_lemmas(self, row: List[str], my_var: Source) -> List[str]:
        """Get alternative lemmas in main."""
        raise NotImplementedError("abstract method")

    @abstractmethod
    def build_keys(self, row: List[str]) -> List[str]:
        raise NotImplementedError("abstract method")

    @abstractmethod
    def multiword(self, row: List[str]) -> Dict[Source, str]:
        raise NotImplementedError("abstract method")

    @abstractmethod
    def multilemma(self, row: List[str], lidx: int = 0) -> Dict[Source, str]:
        raise NotImplementedError("abstract method")

    @abstractmethod
    def compile_words_by_lemma(self, row: List[str], var: Source) -> Tuple[str, int]:
        raise NotImplementedError("abstract method")

    def compile_usages(
        self,
        trans: "LangSemantics",
        row: List[str],
        rtlemma: str,
        rolv: Source = Source(),
        d: SortedDict = SortedDict(),
        special_char="",
    ) -> SortedDict:
        for tvar in trans.multilemma(row).keys():
            for nxt in trans.build_paths(row):
                tvl = _is_variant_lemma(row, trans, tvar, rtlemma)
                if not tvl or rtlemma not in nxt:
                    continue
                (oword, ocnt) = self.compile_words_by_lemma(row, rolv)
                (tword, tcnt) = trans.compile_words_by_lemma(row, tvar)
                idx = Index(row[IDX_COL])
                # print(repr(rolv), oword, ocnt)
                ocontent = _build_content(row, self, rolv, oword, ocnt)
                # print(ocontent)
                tcontent = _build_content(row, trans, tvar, tword, tcnt)
                b = "bold" in row[STYLE_COL]
                i = "italic" in row[STYLE_COL]
                val = Alignment(idx, ocontent, tcontent, b, i, special_char)
                key = (oword, tword)
                d = _add_usage(val, nxt, key, d)
        return d

    @abstractmethod
    def add_count(self, row: List[str], row_counts: Dict[str, int]) -> Dict[str, int]:
        raise NotImplementedError("abstract method")

    from .semabs import (  # type: ignore
        alternatives as abs_alternatives,
        build_paths as abs_build_paths,
        var_alt_lemmas as abs_var_alt_lemmas,
    )

    alternatives = abs_alternatives
    build_paths = abs_build_paths
    var_alt_lemmas = abs_var_alt_lemmas


@dataclass
class MainLangSemantics(LangSemantics):
    def __post_init__(self):
        """
        If there is variant, make sure add correct number of lemma columns.
        relevant, because different language/variant combinations have different number of lemma columns.
        """
        assert (
            self.lang == self.var.lang
        ), f"Mismatch in language of related variants: main is {self.lang}, var is {self.var.lang}"
        self.main = self
        self.var.main = self

        if len(self.lemmas) == len(self.var.lemmas):
            return
        delta = len(self.lemmas) - len(self.var.lemmas)
        if delta > 0:
            self.var.lemmas += [STYLE_COL - 4 + i for i in range(delta)]
        else:
            self.lemmas += [STYLE_COL - 4 + i for i in range(-delta)]

    def other(self) -> "VarLangSemantics":
        assert self.var, "non-null value required by mypy"
        return self.var

    def main_alt_lemmas(self, row: List[str], my_var: Source) -> List[str]:
        """
        Main variant does not contain alternatives to itself.
        """
        return []

    def build_keys(self, row: List[str]) -> List[str]:
        if present(row, self) and self.word != None and bool(row[self.word]):
            return [base_word(row[self.word])]
        return [""]

    from .semmain import (  # type: ignore
        collect_word as main_collect_word,
        collect_lemma as main_collect_lemma,
        multiword as main_multiword,
        multilemma as main_multilemma,
        compile_words_by_lemma as main_compile_words_by_lemma,
        add_count as main_add_count,
    )

    collect_word = main_collect_word
    collect_lemma = main_collect_lemma
    multiword = main_multiword
    multilemma = main_multilemma
    compile_words_by_lemma = main_compile_words_by_lemma
    add_count = main_add_count


@dataclass
class VarLangSemantics(LangSemantics):
    def __post_init__(self):
        self.var = self

    def other(self) -> "MainLangSemantics":
        assert self.main, "non-null value required by mypy"
        return self.main

    def is_variant(self) -> bool:
        return True

    def main_alt_lemmas(self, row: List[str], my_var: Source) -> List[str]:
        assert self.main, "non-null value required by mypy"
        return [row[l] for l in self.main.lemmas if row[l]]

    def build_keys(self, row: List[str]) -> List[str]:
        if present(row, self) and self.word != None and bool(row[self.word]):
            return [base_word(w) for w in self.multiword(row).values()]
        return [""]

    def __repr__(self):
        """main ignored to avoid recursion"""
        return f"VarLangSemantics(lang='{self.lang}',word={self.word},lemmas={self.lemmas})"

    from .semvar import (  # type: ignore
        collect_word as var_collect_word,
        collect_lemma as var_collect_lemma,
        multiword as var_multiword,
        multilemma as var_multilemma,
        compile_words_by_lemma as var_compile_words_by_lemma,
        add_count as var_add_count,
    )

    collect_word = var_collect_word
    collect_lemma = var_collect_lemma
    compile_words_by_lemma = var_compile_words_by_lemma
    multiword = var_multiword
    multilemma = var_multilemma
    add_count = var_add_count
