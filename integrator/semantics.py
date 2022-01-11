"""A collection of model classes, specific to the interpretation of the input spreadsheet"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from sortedcontainers import SortedDict, SortedSet  # type: ignore

import re

from const import EMPTY_CH, PATH_SEP, VAR_SEP, default_sources
from const import IDX_COL, EXAMPLE_COL, STYLE_COL

from util import base_word
from model import Index, Usage, Path


def present(row: List[str], sem: Optional["LangSemantics"]) -> bool:
    """Not present if not semantics specified or if row misses first lemma according to semantics"""
    return not not sem and bool(row[sem.lemmas[0]])


def _build_usage(
    row: List[str],
    osem: "LangSemantics",
    tsem: "LangSemantics",
    ovar: str,
    tvar: str,
    word: str,
):
    """ovar and tvar are a list of variant identifiers"""
    b = "bold" in row[STYLE_COL]
    i = "italic" in row[STYLE_COL]
    v = osem.is_variant()
    idx = Index.unpack(row[IDX_COL], b, i, v, word)
    (oaltm, oaltv) = osem.alternatives(row, ovar)
    (taltm, taltv) = tsem.alternatives(row, tvar)
    var = ovar + VAR_SEP + tvar if ovar and tvar else ovar + tvar
    return Usage(idx, osem.lang, var, oaltm, oaltv, taltm, taltv)


def _is_variant_lemma(
    row: List[str], sem: "LangSemantics", current_var: str, current_lemma: str
) -> bool:
    mlem = sem.multilemma(row)
    if not mlem:
        return False
    # print(mlem)
    if not sem.is_variant():
        assert not current_var
        assert len(mlem) == 1
        return current_lemma == mlem[""]
    # result = current_var not in mlem or current_lemma == mlem[current_var]
    result = current_var in mlem and current_lemma == mlem[current_var]
    # print(f"{current_var} in {current_lemma}: {result}")
    return result


def _add_usage(
    val: "Usage", nxt: Path, key: Tuple[str, str], d: SortedDict
) -> SortedDict:
    """*IN PLACE*"""
    path = str(nxt)
    if path in d:
        if key not in d[path]:
            d[path][key] = SortedSet()
        d[path][key].add(val)
    else:
        d[path] = {key: SortedSet([val])}
    return d


@dataclass
class LangSemantics:
    """Table column mapping for a language."""

    lang: str
    word: int
    lemmas: List[int]

    """Nullable just because recursive reference and setting up needs to happen post-init. Non-null during runtime"""
    var: Optional["VarLangSemantics"] = None
    main: Optional["MainLangSemantics"] = None

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
        """sublemmas (excluding first lemma)"""
        return self.lemmas[1:]

    def other(self) -> "LangSemantics":
        """For main returns variant, for variant returns main.
        Be careful not to enter in infinite recursion"""
        raise NotImplementedError("abstract method")

    def is_variant(self) -> bool:
        return False

    def alternatives(self, row: List[str], my_var: str) -> Tuple[str, Dict[str, str]]:
        """TODO: Also add functionality to get alternative words"""
        m = len(self.lemmas)
        for l in range(m - 1, 0, -1):  # does not reach 0
            if row[self.lemmas[l]].strip():
                lalt = self.level_alternatives(row, my_var, l)
                if not lalt[0] and not lalt[1]:
                    continue
                return lalt
        return self.level_alternatives(row, my_var)  # return with 0 if reach this line

    def level_alternatives(
        self, row: List[str], my_var: str, lidx: int = 0
    ) -> Tuple[str, Dict[str, str]]:
        """Get alternative lemmas
        Returns (main_alt, dict(var_name,var_alt))"""
        raise NotImplementedError("abstract method")

    def key(self, text: str) -> str:
        raise NotImplementedError("abstract method")

    def build_keys(self, row: List[str]) -> List[str]:
        raise NotImplementedError("abstract method")

    def multiword(self, row: List[str]) -> Dict[str, str]:
        raise NotImplementedError("abstract method")

    def multilemma(self, row: List[str], lidx: int = 0) -> Dict[str, str]:
        raise NotImplementedError("abstract method")

    def build_paths(self, row: List[str]) -> List[Path]:
        """Build the multipaths (due to multilemma) relevant to the current row"""
        # first lemma in variant could contain multilemma
        multilemmas = self.multilemma(row).values()
        if not multilemmas:
            return [Path()]
        paths = [Path([w.strip()]) for w in multilemmas]

        # other lemmas could contain annotations that share symbols with variant annotations
        for c in range(1, len(self.lemmas)):
            w = row[self.lemmas[c]].strip()
            if not w:
                continue
            for path in paths:
                path += w.strip()

        for path in paths:
            path.compile()

        return paths

    def compile_usages(
        self,
        trans: "LangSemantics",
        row: List[str],
        d: SortedDict,
        olemma: str,
        tlemma: str,
    ) -> SortedDict:
        # print(self.multiword(row))
        # print(trans.multiword(row))
        for ovar, oword in self.multiword(row).items():
            for tvar, tword in trans.multiword(row).items():
                # TODO: Variant to a lemma is the group of lemmas in the variant.
                val = _build_usage(row, self, trans, ovar, tvar, oword)
                for nxt in trans.build_paths(row):
                    orig_var_in_lemma = _is_variant_lemma(row, self, ovar, olemma)
                    # print(f"{ovar} in {olemma}: {orig_var_in_lemma}")
                    trans_var_in_lemma = _is_variant_lemma(row, trans, tvar, tlemma)
                    # print(f"{tvar} in {tlemma}: {trans_var_in_lemma}")
                    # TODO: what if nxt is gram. or other annotation?
                    # print(f"{tlemma} in {nxt}: {tlemma in nxt}")
                    if orig_var_in_lemma and trans_var_in_lemma and tlemma in nxt:
                        key = (oword, tword)
                        d = _add_usage(val, nxt, key, d)
        return d


@dataclass
class MainLangSemantics(LangSemantics):
    def __post_init__(self):
        """
        If there is variant, make sure add correct number of lemma columns.
        relevant, because different language/variant combinations have different number of lemma columns.
        """
        assert self.lang == self.var.lang
        self.main = self
        self.var.main = self

        if len(self.lemmas) == len(self.var.lemmas):
            return
        delta = len(self.lemmas) - len(self.var.lemmas)
        if delta > 0:
            self.var.lemmas += [STYLE_COL - 4 + i for i in range(delta)]
        else:
            self.lemmas += [STYLE_COL - 4 + i for i in range(-delta)]

    def word_cols(self) -> List[int]:
        assert self.var  # for mypy
        return super().word_cols() + [self.var.word]

    def lem1_cols(self) -> List[int]:
        assert self.var  # for mypy
        return super().lem1_cols() + [self.var.lemmas[0]]

    def lemn_cols(self) -> List[int]:
        assert self.var  # for mypy
        return super().lemn_cols() + self.var.lemmas[1:]

    def other(self) -> "VarLangSemantics":
        assert self.var  # for mypy
        return self.var

    def level_alternatives(
        self, row: List[str], my_var: str, lidx: int = 0
    ) -> Tuple[str, Dict[str, str]]:
        """Get alternative lemmas, ignoring variants that coincide with main
        Returns (main_alt, dict(var_name,var_alt))
        Main alternative to main is always empty/nonexistent"""
        assert self.var  # for mypy
        alt = {
            k: v
            for k, v in self.var.multilemma(row, lidx).items()
            if v != row[self.lemmas[lidx]]
        }
        return ("", alt)

    def key(self, text: str) -> str:
        return text

    def build_keys(self, row: List[str]) -> List[str]:
        if present(row, self) and self.word != None and not not row[self.word]:
            return [base_word(row[self.word])]
        return [""]

    def multiword(self, row: List[str]) -> Dict[str, str]:
        """Main variant does not have multiple words in a cell"""
        return {"": row[self.word].strip()}

    def multilemma(self, row: List[str], lidx: int = 0) -> Dict[str, str]:
        """Main variant does not have multiple words in a cell"""
        return {"": row[self.lemmas[lidx]].strip()}


@dataclass
class VarLangSemantics(LangSemantics):
    def __post_init__(self):
        self.var = self

    def word_cols(self) -> List[int]:
        assert self.main  # for mypy
        return super().word_cols() + [self.main.word]

    def lem1_cols(self) -> List[int]:
        assert self.main  # for mypy
        return super().lem1_cols() + [self.main.lemmas[0]]

    def lemn_cols(self) -> List[int]:
        assert self.main  # for mypy
        return super().lemn_cols() + self.main.lemmas[1:]

    def other(self) -> "MainLangSemantics":
        assert self.main  # for mypy
        return self.main

    def is_variant(self) -> bool:
        return True

    def level_alternatives(
        self, row: List[str], my_var: str, lidx: int = 0
    ) -> Tuple[str, Dict[str, str]]:
        """Get alternative lemmas, skipping main if coincides with my variant
        Returns (main_alt, dict(var_name,var_alt))"""
        main = ""
        multilemma = self.multilemma(row, lidx)
        if present(row, self.main):
            assert self.main  # for mypy
            if (
                my_var in multilemma
                and row[self.main.lemmas[lidx]] != multilemma[my_var]
            ):
                main = row[self.main.lemmas[lidx]]
        alt = {k: v for k, v in multilemma.items() if k != my_var}
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
        regex = r"^([^A-Z]+)(([A-Z][a-z]?)+)(.*)$"
        result = {}
        m = re.search(regex, row[self.word].strip())
        while m:
            result[m.group(2)] = m.group(1).strip()
            rest = m.group(4).strip()
            m = re.search(regex, rest)
        if not result:
            return {default_sources[self.lang]: row[self.word].strip()}
            # return {'': row[self.word].strip()}
        return result

    def multilemma(self, row: List[str], lidx: int = 0) -> Dict[str, str]:
        # TODO: accepting both & and / as separators is not neccessary
        regex = r"^([^A-Z\+]+)(\+\s\w+\.)?(([A-Z][a-z]?)+)?(\s*[\&\/])?(.*)$"
        # regex = r"^([^A-Z]+)(([A-Z][a-z]?)+)?(\s*[\&\/])?(.*)$"
        result = {}
        m = re.search(regex, row[self.lemmas[lidx]].strip())
        while m:
            v = m.group(1) if m.group(1) else ""
            v = v + m.group(2) if m.group(2) else v
            v = v.strip()

            k = m.group(3) if m.group(3) else ""
            result[k] = v
            rest = m.group(6) if len(m.groups()) == 6 else ""
            m = re.search(regex, rest.strip())

        # When lemma in variant does not have source, read source from word
        # When in some variants word is missing, get lemma for this variant from main
        if len(result) == 1 and next(iter(result.keys())) == "":
            updated = {}
            for k, v in self.multiword(row).items():
                if v != EMPTY_CH:
                    updated[k] = result[""]

            # words = {k: v for k, v in self.multiword(row).items() if v != EMPTY_CH}
            # assert len(words) == 1
            # return {next(iter(words.keys())): result[""]}
            return updated

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
