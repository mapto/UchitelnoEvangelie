"""A collection of model classes, specific to the interpretation of the input spreadsheet"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from sortedcontainers import SortedDict, SortedSet  # type: ignore

import re

from const import EMPTY_CH, H_LEMMA_SEP, PATH_SEP, VAR_SEP, default_sources
from const import IDX_COL, EXAMPLE_COL, STYLE_COL

from util import base_word
from model import Index, Usage


def present(row: List[str], sem: Optional["LangSemantics"]) -> bool:
    """Not present if not semantics specified or if row misses first lemma according to semantics"""
    return not not sem and not not row[sem.lemmas[0]]


def _add_usage(
    val: "Usage", nxt: str, key: Tuple[str, str], d: SortedDict
) -> SortedDict:
    """*IN PLACE*"""
    if nxt in d:
        if key not in d[nxt]:
            d[nxt][key] = SortedSet()
        d[nxt][key].add(val)
    else:
        d[nxt] = {key: SortedSet([val])}
    return d


@dataclass
class LangSemantics:
    """Table column mapping for a language."""

    lang: str
    word: int
    lemmas: List[int]

    '''
    def __post_init__(self):
        """
        If there is variant, make sure add correct number of lemma columns.
        relevant, because different language/variant combinations have different number of lemma columns.
        """
        if not self.var or len(self.lemmas) == len(self.var.lemmas):
            return
        delta = len(self.lemmas) - len(self.var.lemmas)
        if delta > 0:
            self.var.lemmas += [STYLE_COL - 4 + i for i in range(delta)]
        else:
            self.lemmas += [STYLE_COL - 4 + i for i in range(-delta)]
    '''

    def cols(self) -> List[int]:
        c = []
        c += self.word_cols()
        c += self.lem1_cols()
        c += self.lemn_cols()
        return c

    def word_cols(self) -> List[int]:
        return [self.word]

    def lem1_cols(self) -> List[int]:
        return [self.lemmas[0]]

    def lemn_cols(self) -> List[int]:
        return self.lemmas[1:]

    def get_variant(self, row: List[str]) -> str:
        return "".join([k for k in self.multiword(row).keys()])

    def alternatives(self, row: List[str], var: str) -> Tuple[str, Dict[str, str]]:
        """Returns (main_alt, dict(var_name,var_alt))"""
        raise NotImplementedError("abstract method")

    def key(self, text: str) -> str:
        raise NotImplementedError("abstract method")

    def build_keys(self, row: List[str]) -> List[str]:
        raise NotImplementedError("abstract method")

    def multiword(self, row: List[str]) -> Dict[str, str]:
        raise NotImplementedError("abstract method")

    def multilemma(self, row: List[str], lemma: int = 0) -> Dict[str, str]:
        raise NotImplementedError("abstract method")

    def build_paths(self, row: List[str]) -> List[str]:
        paths: List[List[str]] = [[]]
        for c in range(len(self.lemmas)):
            new_paths = []
            # print(f"{c} {self.lemmas[c]} {row[self.lemmas[c]]}")
            for w in self.multilemma(row, c).values():
                # print(f"{w} {w.strip()}")
                for path in paths:
                    n = path.copy()
                    n.append(w)
                    new_paths.append(n)
            paths = new_paths

        result: List[str] = []
        for cols in paths:
            extract = None
            cols.reverse()
            empty = True
            while empty:
                if not cols:
                    empty = False
                elif not cols[0]:
                    cols.pop(0)
                    empty = len(cols) > 0
                elif re.match(r"^[a-zA-z\.]+$", cols[0]):
                    extract = cols.pop(0)
                else:
                    empty = False
            construct = PATH_SEP.join(cols)
            if extract:
                construct += f" {extract}"
            result.append(construct)

        return result

    def build_usages(
        self, trans: "LangSemantics", row: List[str], d: SortedDict, lemma: str
    ) -> SortedDict:
        """
        TODO: test, esp. combined variants
        """
        for ovar, oword in self.multiword(row).items():
            for tvar, tword in trans.multiword(row).items():
                key = (oword, tword)
                b = "bold" in row[STYLE_COL]
                i = "italic" in row[STYLE_COL]
                idx = Index.unpack(row[IDX_COL], b, i)
                (oaltm, oaltv) = self.alternatives(row, ovar)
                (taltm, taltv) = trans.alternatives(row, tvar)
                var = ovar + VAR_SEP + tvar if ovar and tvar else ovar + tvar
                val = Usage(idx, self.lang, var, oaltm, oaltv, taltm, taltv)
                for nxt in trans.build_paths(row):
                    ml = self.multilemma(row)
                    if ovar not in ml or lemma == ml[ovar]:
                        d = _add_usage(val, nxt, key, d)
        return d


@dataclass
class MainLangSemantics(LangSemantics):
    var: "VarLangSemantics"

    def __post_init__(self):
        """
        If there is variant, make sure add correct number of lemma columns.
        relevant, because different language/variant combinations have different number of lemma columns.
        """
        assert self.lang == self.var.lang
        self.var.main = self

        if len(self.lemmas) == len(self.var.lemmas):
            return
        delta = len(self.lemmas) - len(self.var.lemmas)
        if delta > 0:
            self.var.lemmas += [STYLE_COL - 4 + i for i in range(delta)]
        else:
            self.lemmas += [STYLE_COL - 4 + i for i in range(-delta)]

    def word_cols(self) -> List[int]:
        return super().word_cols() + [self.var.word]

    def lem1_cols(self) -> List[int]:
        return super().lem1_cols() + [self.var.lemmas[0]]

    def lemn_cols(self) -> List[int]:
        return super().lemn_cols() + self.var.lemmas[1:]

    def alternatives(self, row: List[str], var: str) -> Tuple[str, Dict[str, str]]:
        """Returns (main_alt, dict(var_name,var_alt))
        Main alternative to main is always empty/nonexistent"""
        alt = self.var.multilemma(row)
        return ("", alt)

    def key(self, text: str) -> str:
        return text

    def build_keys(self, row: List[str]) -> List[str]:
        if present(row, self) and self.word != None and not not row[self.word]:
            return [base_word(row[self.word])]
        return [""]

    def multiword(self, row: List[str]) -> Dict[str, str]:
        """Main variant does not have multiple words in a cell"""
        return {"": row[self.word]}

    def multilemma(self, row: List[str], lemma: int = 0) -> Dict[str, str]:
        """Main variant does not have multiple words in a cell"""
        return {"": row[self.lemmas[lemma]]}


@dataclass
class VarLangSemantics(LangSemantics):
    """main is nullable just because it's a recursive reference and setting up needs to happen post-init"""

    main: Optional["MainLangSemantics"] = None

    def alternatives(self, row: List[str], var: str) -> Tuple[str, Dict[str, str]]:
        """Returns (main_alt, dict(var_name,var_alt))"""
        main = ""
        if present(row, self.main):
            assert self.main  # for mypy
            main = row[self.main.lemmas[0]]
        alt = {k: v for k, v in self.multilemma(row).items() if k != var}
        return (main, alt)

    def key(self, text: str) -> str:
        m = re.search(r"^([^A-Z]+)([A-Z]+)$", text.strip())
        if m:
            text = m.group(1).strip()
        return f" {{{text}}}"

    def build_keys(self, row: List[str]) -> List[str]:
        if present(row, self) and self.word != None and not not row[self.word]:
            return [base_word(w) for w in self.multiword(row).values()]
        return [""]

    def multiword(self, row: List[str]) -> Dict[str, str]:
        result = {}
        m = re.search(r"^([^A-Z]+)([A-Z]+)(.*)$", row[self.word].strip())
        while m:
            result[m.group(2)] = m.group(1).strip()
            rest = m.group(3).strip()
            m = re.search(r"^([^A-Z]+)([A-Z]+)(.*)$", rest)
        if not result:
            return {default_sources[self.lang]: row[self.word].strip()}
            # return {'': row[self.word].strip()}
        return result

    def multilemma(self, row: List[str], lemma: int = 0) -> Dict[str, str]:
        result = {}
        # TODO: accepting both & and / as separators is not neccessary
        m = re.search(
            r"^([^A-Z]+)([A-Z]+)?(\s*[\&\/])?(.*)$", row[self.lemmas[lemma]].strip()
        )
        while m:
            v = m.group(1).strip() if m.group(1) else ""
            k = m.group(2) if m.group(2) else ""
            result[k] = v
            rest = m.group(4) if len(m.groups()) == 4 else ""
            m = re.search(r"^([^A-Z]+)([A-Z]+)(.*)$", rest.strip())

        # When lemma in variant does not have source, read it from word
        if len(result) == 1 and next(iter(result.keys())) == "":
            words = {k: v for k, v in self.multiword(row).items() if v != EMPTY_CH}
            assert len(words) == 1
            return {next(iter(words.keys())): result[""]}

        return result

    def __repr__(self):
        """main ignored to avoid recursion"""
        return (
            f"VarLangSemantics(lang={self.lang},word={self.word},lemmas={self.lemmas})"
        )


@dataclass
class TableSemantics:
    """Overall table column mapping"""

    sl: "MainLangSemantics"
    gr: "MainLangSemantics"
    idx: int = IDX_COL
    example: int = EXAMPLE_COL
    style: int = STYLE_COL

    def cols(self) -> List[int]:
        """extract word and lemma columns"""
        c = []
        c += self.sl.cols()
        c += self.gr.cols()
        return c

    def word_cols(self) -> List[int]:
        """extract word columns"""
        c = []
        c += self.sl.word_cols()
        c += self.gr.word_cols()
        return c

    def lem1_cols(self) -> List[int]:
        """extract first lemma columns"""
        c = []
        c += self.sl.lem1_cols()
        c += self.gr.lem1_cols()
        return c

    def lemn_cols(self) -> List[int]:
        """extract word and lemma columns"""
        c = []
        c += self.sl.lemn_cols()
        c += self.gr.lemn_cols()
        return c
