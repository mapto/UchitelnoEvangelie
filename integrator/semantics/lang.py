"""A collection of model classes, specific to the interpretation of the input spreadsheet"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from sortedcontainers import SortedDict, SortedSet  # type: ignore

import re

from const import H_LEMMA_SEP, IDX_COL, NON_COUNTABLE, NON_LEMMAS, STYLE_COL
from const import EMPTY_CH, MISSING_CH
from const import ERR_SUBLEMMA, SPECIAL_CHARS
from const import DEFAULT_SOURCES

from regex import multiword_regex, multilemma_regex
from .util import collect, remove_repetitions, regroup, _add_usage
from util import base_word
from model import Alternative, Index, Path, Source, Alignment, Usage

LAST_LEMMA = -1
UNSPECIFIED = -1


def present(row: List[str], sem: Optional["LangSemantics"]) -> bool:
    """Not present if not semantics specified or if row misses first lemma according to semantics"""
    return not not sem and bool(row[sem.lemmas[0]])


def _build_content(
    row: List[str], sem: "LangSemantics", var: Source, word: str, cnt: int
) -> Usage:
    oalt = sem.alternatives(row, var)
    lemmas = []
    for lvl in range(0, len(sem.lemmas)):
        found = False
        ml = sem.multilemma(row, lvl)
        for k, v in ml.items():
            if not k or var in k:
                lemmas += [v]
                found = True
                break
        if not found:
            lemmas += [""]
    while lemmas and not lemmas[-1]:
        lemmas.pop()
    return Usage(sem.lang, var, oalt, word, lemmas, cnt)


def _is_variant_lemma(
    row: List[str], sem: "LangSemantics", current_var: Source, current_lemma: str
) -> bool:
    mlem = sem.multilemma(row)
    if not mlem:
        return False
    if not sem.is_variant():
        assert not current_var
        assert len(mlem) == 1
        return current_lemma in mlem[Source()]
    loc = current_var.inside(mlem)
    result = loc is not None and current_lemma in mlem[loc]
    return result


@dataclass
class LangSemantics:
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

    def collect_word(self, group: List[List[str]]) -> str:
        raise NotImplementedError("abstract method")

    def collect_lemma(
        self, group: List[List[str]], cidx: int, separator: str = ""
    ) -> str:
        raise NotImplementedError("abstract method")

    def alternatives(self, row: List[str], my_var: Source) -> Alternative:
        m = len(self.lemmas) - 1
        alt_main = ("", "", 1)
        alt_var: Tuple[Dict[Source, str], Dict[Source, Tuple[str, int]]] = ({}, {})
        for l in range(m, -1, -1):
            if not alt_main[0]:
                alt_main = self.level_main_alternatives(row, my_var, l)
                if alt_main[0] in NON_LEMMAS:
                    alt_main = ("", "", 1)
            if not alt_var[0]:
                alt_var = self.level_var_alternatives(row, my_var, l)
                for v in alt_var[0].values():
                    if v in NON_LEMMAS:
                        alt_var = ({}, {})
        return Alternative(
            alt_main[0], alt_var[0], alt_main[1], alt_var[1], alt_main[2]
        )

    def level_main_alternatives(
        self, row: List[str], my_var: Source, lidx: int = 0
    ) -> Tuple[str, str, int]:
        """Get alternative lemmas in main.
        First return value is lemma, second word"""
        raise NotImplementedError("abstract method")

    def level_var_alternatives(
        self, row: List[str], my_var: Source, lidx: int = 0
    ) -> Tuple[Dict[Source, str], Dict[Source, Tuple[str, int]]]:
        """Get alternative lemmas in variant.
        First return value is lemma, second word"""
        raise NotImplementedError("abstract method")

    def build_keys(self, row: List[str]) -> List[str]:
        raise NotImplementedError("abstract method")

    def multiword(self, row: List[str]) -> Dict[Source, str]:
        raise NotImplementedError("abstract method")

    def multilemma(self, row: List[str], lidx: int = 0) -> Dict[Source, str]:
        raise NotImplementedError("abstract method")

    def build_paths(self, row: List[str]) -> List[Path]:
        """Build the multipaths (due to multilemma) relevant to the current row"""
        # first lemma in variant could contain multilemma
        multilemmas = self.multilemma(row)
        if not multilemmas:
            return [Path()]
        paths = {k: Path([v.strip()]) for k, v in multilemmas.items()}
        if self.is_variant() and len(paths) == 1 and next(iter(paths.keys())) == "":
            keys = Source(DEFAULT_SOURCES[self.lang])
            paths = {keys: next(iter(paths.values()))}

        # other lemmas could contain multilemmas with less sources
        for c in range(1, len(self.lemmas)):
            w = row[self.lemmas[c]].strip()
            if not w:
                continue
            multilemmas = self.multilemma(row, c)
            if (
                self.is_variant()
                and len(multilemmas) == 1
                and next(iter(multilemmas.keys())) == ""
            ):
                s = {str(k) for k in paths.keys()}
                keys = Source(remove_repetitions("".join(s)))
                multilemmas = {keys: next(iter(multilemmas.values()))}

            for k, v in multilemmas.items():
                for pk, path in paths.items():
                    if pk.inside([k]) is not None:
                        path += v.strip()

        for k, path in paths.items():
            path.compile()

        return list(paths.values())

    def compile_words_by_lemma(
        self, row: List[str], var: Source
    ) -> Tuple[str, str, int]:
        raise NotImplementedError("abstract method")

    def compile_usages(
        self,
        trans: "LangSemantics",
        row: List[str],
        d: SortedDict,
        rolemma: str,
        rtlemma: str,
        rolv: Source = Source(),
    ) -> SortedDict:
        for tvar in trans.multilemma(row).keys():
            for nxt in trans.build_paths(row):
                tvl = _is_variant_lemma(row, trans, tvar, rtlemma)
                if not tvl or rtlemma not in nxt:
                    continue
                (oword, olemma, ocnt) = self.compile_words_by_lemma(row, rolv)
                (tword, tlemma, tcnt) = trans.compile_words_by_lemma(row, tvar)
                idx = Index(row[IDX_COL])
                ocontent = _build_content(row, self, rolv, oword, ocnt)
                tcontent = _build_content(row, trans, tvar, tword, tcnt)
                b = "bold" in row[STYLE_COL]
                i = "italic" in row[STYLE_COL]
                val = Alignment(idx, ocontent, tcontent, b, i)
                key = (oword, tword)
                d = _add_usage(val, nxt, key, d)
        return d

    def add_count(self, row: List[str], row_counts: Dict[str, int]) -> Dict[str, int]:
        raise NotImplementedError("abstract method")


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

    def collect_word(self, group: List[List[str]]) -> str:
        return " ".join(collect(group, self.word))

    def collect_lemma(
        self, group: List[List[str]], cidx: int, separator: str = ""
    ) -> str:
        g = [e for e in collect(group, cidx) if e.strip() != MISSING_CH]
        if separator:
            return f" {separator} ".join(g)
        return f" ".join(g)

    def level_main_alternatives(
        self, row: List[str], my_var: Source, lidx: int = 0
    ) -> Tuple[str, str, int]:
        return "", "", 1

    def level_var_alternatives(
        self, row: List[str], my_var: Source, lidx: int = 0
    ) -> Tuple[Dict[Source, str], Dict[Source, Tuple[str, int]]]:
        """Get alternative lemmas, ignoring variants that coincide with main"""
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
        alt_words = {l: (v[0], v[2]) for l, v in aw.items()}
        if Source() in alt_lemmas:
            alt_lemmas[Source("".join(str(s) for s in alt_words.keys()))] = alt_lemmas[
                Source()
            ]
            alt_lemmas.pop(Source())
            alt_words.pop(Source())
        return alt_lemmas, alt_words

    def build_keys(self, row: List[str]) -> List[str]:
        if present(row, self) and self.word != None and bool(row[self.word]):
            return [base_word(row[self.word])]
        return [""]

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
    ) -> Tuple[str, str, int]:
        return (row[self.word], row[self.lemmas[0]], int(row[self.cnt_col]))

    def add_count(self, row: List[str], row_counts: Dict[str, int]) -> Dict[str, int]:
        """based on word (in column) expand it with counter
        *IN PLACE*
        Updates both row and row_counts"""
        if not self.cnt_col:
            self.cnt_col = len(row)
        while len(row) < self.cnt_col + 1:
            row += ["1"]

        if not row[self.word] or row[self.word] in NON_COUNTABLE:
            return row_counts
        if row[self.word] in row_counts:
            row_counts[row[self.word]] += 1
            row[self.cnt_col] = str(row_counts[row[self.word]])
        else:
            row_counts[row[self.word]] = 1
            # fallback to default value for cnt in Index
        return row_counts


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

    def collect_word(self, group: List[List[str]]) -> str:
        """Collects the content of the multiwords for a variant in a group into a single string.
        The output is conformant with the multiword syntax.
        Yet it might contain redundancies, due to the normalisation process (split of equal variants)"""
        collected: Dict[Source, List[str]] = SortedDict()
        for row in group:
            for k, v in self.multiword(row).items():
                if not v.strip():
                    continue
                if k not in collected:
                    collected[k] = []
                collected[k] += [v.strip()]
        result = regroup(
            {k: " ".join(collected[k]) for k in collected if any(collected[k])}
        )
        return " ".join([f"{v} {k}" if k else v for k, v in result.items() if v])

    def collect_lemma(
        self, group: List[List[str]], cidx: int = UNSPECIFIED, separator: str = ""
    ) -> str:
        if cidx == UNSPECIFIED:
            cidx = self.lemmas[0]
        multis = [self.multilemma(r, self.lemmas.index(cidx)) for r in group]
        collected: Dict[Source, List[str]] = SortedDict()
        for m in multis:
            for k, v in m.items():
                if k not in collected:
                    collected[k] = []
                collected[k] += [v]
        glue = f" {separator} " if separator else " "
        result = regroup({k: glue.join(collected[k]).strip() for k in collected}, glue)
        g = [f"{v} {k}" if k else v for k, v in result.items() if v]
        return f" {H_LEMMA_SEP} ".join(g)

    def level_main_alternatives(
        self, row: List[str], my_var: Source, lidx: int = 0
    ) -> Tuple[str, str, int]:
        """Get alternative lemmas in main"""
        main_lemma = ""
        main_word = ""
        multilemma = self.multilemma(row, lidx)
        if present(row, self.main):
            assert self.main  # for mypy
            loc = my_var.inside(multilemma)
            if loc and row[self.main.lemmas[lidx]] != multilemma[loc]:
                main_lemma = row[self.main.lemmas[lidx]]
                main_word = row[self.main.word]
                # Get interpretative annotation from sublemma if any
                if lidx == 0 and len(self.main.lemmas) > 1:
                    for prefix in SPECIAL_CHARS + [ERR_SUBLEMMA]:
                        if row[self.main.lemmas[1]].startswith(prefix):
                            main_lemma = f"{prefix} {main_lemma}"
                            break

        return main_lemma, main_word, int(row[self.other().cnt_col])

    def level_var_alternatives(
        self, row: List[str], my_var: Source, lidx: int = 0
    ) -> Tuple[Dict[Source, str], Dict[Source, Tuple[str, int]]]:
        """Get alternative lemmas in variant"""
        multilemma = self.multilemma(row, lidx)
        alt_lemmas = {k: v for k, v in multilemma.items() if my_var not in k}
        # Get interpretative annotation from sublemma if any
        if lidx == 0 and len(self.lemmas) > 1:
            l2 = self.multilemma(row, 1)
            for k2, v2 in l2.items():
                for prefix in SPECIAL_CHARS + [ERR_SUBLEMMA]:
                    if v2.startswith(prefix):
                        for k1 in alt_lemmas.keys():
                            if k1.inside(k2):
                                alt_lemmas[k1] = f"{prefix} {alt_lemmas[k1]}"
                        break

        aw = {
            k: self.compile_words_by_lemma(row, k)
            for k, v in self.multiword(row).items()
            if k.inside(alt_lemmas)
        }
        alt_words = {k: (v[0], v[2]) for k, v in aw.items()}

        return alt_lemmas, alt_words

    def build_keys(self, row: List[str]) -> List[str]:
        if present(row, self) and self.word != None and bool(row[self.word]):
            return [base_word(w) for w in self.multiword(row).values()]
        return [""]

    def multiword(self, row: List[str]) -> Dict[Source, str]:
        result: Dict[Source, str] = SortedDict()
        m = re.search(multiword_regex, row[self.word].strip())
        while m:
            s = Source(m.group(2))
            v = m.group(1).strip()
            result[s] = " ".join([result[s], v]) if s in result else v
            rest = m.group(4).strip()
            m = re.search(multiword_regex, rest)
        if not result:
            return {Source(DEFAULT_SOURCES[self.lang]): row[self.word].strip()}
            # return {'': row[self.word].strip()}
        return regroup(result)

    def multilemma(self, row: List[str], lidx: int = 0) -> Dict[Source, str]:
        if lidx == LAST_LEMMA:
            lidx = len(self.lemmas) - 1
            while lidx > 0 and not row[self.lemmas[lidx]]:
                lidx -= 1
            return self.multilemma(row, lidx)
        result = SortedDict()
        m = re.search(multilemma_regex, row[self.lemmas[lidx]].strip())
        while m:
            v = m.group(1) if m.group(1) else ""
            v = v + m.group(2) if m.group(2) else v
            v = v.strip()

            k = m.group(3) if m.group(3) else ""
            result[Source(k)] = v
            rest = m.group(6) if len(m.groups()) == 6 else ""
            m = re.search(multilemma_regex, rest.strip())

        # When lemma in variant does not have source, read source from word or previous lemma
        # When in some variants word is missing, get lemma for this variant from main
        # When different variants have same lemma, unite. Case present only when deduced from different multiwords
        if len(result) == 1 and next(iter(result.keys())) == "":
            previdx = lidx - 1
            while not row[self.lemmas[previdx]] and previdx >= 0:
                previdx -= 1
            prev_multi = (
                self.multilemma(row, previdx) if previdx >= 0 else self.multiword(row)
            )
            s = {str(k) for k, v in prev_multi.items() if v != EMPTY_CH}
            keys = Source(remove_repetitions("".join(s)))
            # keys = ""
            # for k, v in self.multiword(row).items():
            #     if v != EMPTY_CH:
            #         keys += k

            # words = {k: v for k, v in self.multiword(row).items() if v != EMPTY_CH}
            # assert len(words) == 1
            # return {next(iter(words.keys())): result[""]}
            if not result[Source()]:
                return {}
            return {keys: result[Source()]}

        return result

    def compile_words_by_lemma(
        self, row: List[str], var: Source
    ) -> Tuple[str, str, int]:
        """returns:
        1. concatenated pairs (word, variant)
        2. lemmas without variants
        3. repetition index in row
        TODO: Consider introducing a new data class
        """
        vars = SortedSet()
        lemmas = SortedSet()
        multiword = self.multiword(row)
        multilemma = self.multilemma(row)
        for v in var:
            for kw in multiword.keys():
                if not kw and v in Source(DEFAULT_SOURCES[self.lang]):
                    vars.add(f"{multiword[Source()]} {kw}")
                    lemmas.add(multilemma[Source()])
                elif v in kw and kw in multiword:
                    vars.add(f"{multiword[kw]} {kw}")
                    for m in multilemma.keys():
                        if kw in m:
                            lemmas.add(multilemma[m])
                            break
        # TODO: multiword counts need to distinguish between variants
        return (" ".join(vars), " ".join(lemmas), int(row[self.cnt_col]))

    def __repr__(self):
        """main ignored to avoid recursion"""
        return (
            f"VarLangSemantics(lang={self.lang},word={self.word},lemmas={self.lemmas})"
        )

    def add_count(self, row: List[str], row_counts: Dict[str, int]) -> Dict[str, int]:
        """based on word (in column) expand it with counter
        *IN PLACE*
        Updates both row and row_counts"""
        # TODO: multiword counts need to distinguish between variants
        if not self.cnt_col:
            self.cnt_col = len(row)
        while len(row) < self.cnt_col + 1:
            row += ["1"]

        col = self.word
        # Counts should be ignored, as they clearly don't exist before coming here
        if not row[self.word]:
            return row_counts
        multiword = self.multiword(row)
        for k, v in multiword.items():
            if v in NON_COUNTABLE:
                continue
            if v in row_counts:
                row_counts[v] += 1
                row[self.cnt_col] = str(row_counts[v])
            else:
                row_counts[v] = 1
                # result += [f"{v[0]}{' ' if k else ''}{k}"]
                # fallback to default value for cnt in Index
        # row[self.word] = " ".join(result)
        return row_counts
