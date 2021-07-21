from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from sortedcontainers import SortedDict, SortedSet  # type: ignore

import re

from const import EMPTY_CH, H_LEMMA_SEP, PATH_SEP, default_sources
from const import IDX_COL, EXAMPLE_COL, STYLE_COL

from util import base_word


def _present(row: List[str], sem: Optional["LangSemantics"]) -> bool:
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


@dataclass(order=True, frozen=True)
class Index:
    """Index only indicates if it is from a variant.
    Alternative variable (alt) means alternative indexing.
     Contrast these to Usage."""

    ch: int
    alt: bool
    page: int
    col: str
    row: int
    var: bool = False
    end: Optional["Index"] = None
    bold: bool = False
    italic: bool = False

    @staticmethod
    def unpack(
        value: str, b: bool = False, i: bool = False, var: bool = False
    ) -> "Index":
        """
        >>> Index.unpack("1/W167c4").longstr()
        '01/W167c04'
        >>> str(Index.unpack("1/6c4"))
        '1/6c4'

        >> str(Index.unpack("1/6c4var"))
        '1/6c4var'
        >>> str(Index.unpack("1/6c4-8"))
        '1/6c4-8'

        >> str(Index.unpack("1/6c4-8var"))
        '1/6c4-8var'
        >>> str(Index.unpack("1/6c4-d4"))
        '1/6c4-d4'
        >>> str(Index.unpack("1/6c4-6d4"))
        '1/6c4-d4'
        >>> str(Index.unpack("1/6c4-7d4"))
        '1/6c4-7d4'
        >>> str(Index.unpack("1/6c4-2/6d4"))
        '1/6c4-2/6d4'

        >> str(Index.unpack("1/6c4var-2/6d4var"))
        '1/6c4var-2/6d4var'

        >>> Index.unpack("1/6a8") < Index.unpack("1/6a17")
        True
        >>> Index.unpack("1/6a8") < Index.unpack("1/W167c4")
        True
        >>> Index.unpack("2/6a8") < Index.unpack("2/W167c4")
        False

        Regex using: https://pythex.org/
        """
        # TODO: var from regex (shift indices)
        m = re.search(
            r"(\d{1,2})/(W)?(\d{1,3})([abcd])(\d{1,2})(var)?"
            + r"(-((((\d{1,2})/)?(W)?(\d{1,3}))?([abcd]))?(\d{1,2})(var)?)?",
            value,
        )
        assert m
        # print(m.groups())
        ch = int(m.group(1))
        # alt puts W at end of ch1 and at start of ch2
        alt = not not m.group(2) if ch % 2 else not m.group(2)
        page = int(m.group(3))
        col = m.group(4)
        row = int(m.group(5))
        # v = m.group(6)

        end = None
        if m.group(15):
            e_ch = ch
            e_alt = alt
            e_page = page
            e_col = col
            e_row = int(m.group(15))
            # e_var = m.group(16)
            if m.group(14):
                e_col = m.group(14)
                if m.group(13):
                    e_page = int(m.group(13))
                    if m.group(11):
                        e_ch = int(m.group(11))
                    e_alt = not not m.group(12) if e_ch % 2 else not m.group(12)
            end = Index(e_ch, e_alt, e_page, e_col, e_row, var)

        return Index(ch, alt, page, col, row, var, end, b, i)

    def __str__(self):
        """
        >>> str(Index(1, False, 6, "c", 4, end=Index(1, False, 6, "d", 4)))
        '1/6c4-d4'
        >>> str(Index(1, False, 6, "c", 4, end=Index(1, False, 6, "c", 11)))
        '1/6c4-11'

        Variants are not shown:
        >>> str(Index(1, False, 6, "c", 4, True, Index(1, False, 6, "d", 4, True)))
        '1/6c4-d4'

        >>> str(Index(1, True, 6, "c", 4))
        '1/W6c4'
        >>> str(Index(2, False, 6, "c", 4))
        '2/W6c4'
        """
        w = "W" if not not self.ch % 2 == self.alt else ""
        start = f"{self.ch}/{w}{self.page}{self.col}{self.row}"
        if self.end:
            if self.end.ch != self.ch:
                return f"{start}-{str(self.end)}"
            if self.end.alt != self.alt:
                ew = "W" if self.end.alt and self.end.ch % 2 else ""
                return f"{start}-{ew}{self.end.page}{self.end.col}{self.end.row}"
            if self.end.page != self.page:
                return f"{start}-{self.end.page}{self.end.col}{self.end.row}"
            if self.end.col != self.col:
                return f"{start}-{self.end.col}{self.end.row}"
            if self.end.row != self.row:
                return f"{start}-{self.end.row}"
        return start

    def longstr(self):
        """
        >>> Index(1, False, 6, "c", 4, end=Index(2, True, 6, "c", 4)).longstr()
        '01/006c04-02/006c04'

        >> Index(1, False, 6, "c", 4, True, Index(2, True, 6, "c", 4)).longstr()
        '01/006c04WH-02/006c04'
        >> Index(1, False, 6, "c", 4, end=Index(2, True, 6, "c", 4, True)).longstr()
        '01/006c04-02/006c04WH'
        """
        w = "W" if not not self.ch % 2 == self.alt else ""
        v = "var" if self.var else ""
        start = f"{self.ch:02d}/{w}{self.page:03d}{self.col}{self.row:02d}{v}"
        if self.end:
            if self.end.ch != self.ch:
                return f"{start}-{self.end.longstr()}"
            ev = "var" if self.end.var else ""
            if self.end.alt != self.alt:
                ew = "W" if self.end.alt and self.end.ch % 2 else ""
                return f"{start}-{ew}{self.end.page:03d}{self.end.col}{self.end.row:02d}{ev}"
            if self.end.page != self.page:
                return (
                    f"{start}-{self.end.page:03d}{self.end.col}{self.end.row:02d}{ev}"
                )
            if self.end.col != self.col:
                return f"{start}-" f"{self.end.col}{self.end.row:02d}{ev}"
            if self.end.row != self.row:
                return f"{start}-{self.end.row:02d}{ev}"
        return start


@dataclass(order=True, frozen=True)
class Usage:
    """Variant is not only indicative, but also nominative - which variant.
    Here alt means other other transcriptions (main or var).
    Contrast these to Index"""

    idx: Index
    lang: str
    var: str = ""
    orig_alt: str = ""
    orig_alt_var: Dict[str, str] = field(default_factory=lambda: {})
    trans_alt: str = ""
    trans_alt_var: Dict[str, str] = field(default_factory=lambda: {})

    def __hash__(self):
        return hash((self.idx, self.lang, self.orig_alt, self.trans_alt))


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
            print(f"{c} {self.lemmas[c]} {row[self.lemmas[c]]}")
            for w in self.multilemma(row, c).values():
                print(f"{w} {w.strip()}")
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
        for ovar, oword in self.multiword(row).items():
            for tvar, tword in trans.multiword(row).items():
                key = (oword, tword)
                b = "bold" in row[STYLE_COL]
                i = "italic" in row[STYLE_COL]
                idx = Index.unpack(row[IDX_COL], b, i)
                oalt = self.alternatives(row, ovar)
                talt = trans.alternatives(row, tvar)
                var = ovar + tvar
                val = Usage(idx, self.lang, var, oalt[0], oalt[1], talt[0], talt[1])
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
        alt = self.var.multilemma(row)
        return ("", alt)

    def key(self, text: str) -> str:
        return text

    def build_keys(self, row: List[str]) -> List[str]:
        if _present(row, self) and self.word != None and not not row[self.word]:
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
        main = ""
        if self.main and row[self.main.lemmas[0]]:
            main = row[self.main.lemmas[0]]
        alt = {k: v for k, v in self.multilemma(row).items() if k != var}
        return (main, alt)

    def key(self, text: str) -> str:
        m = re.search(r"^([^A-Z]+)([A-Z]+)$", text.strip())
        if m:
            text = m.group(1).strip()
        return f" {{{text}}}"

    def build_keys(self, row: List[str]) -> List[str]:
        if _present(row, self) and self.word != None and not not row[self.word]:
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


@dataclass
class Counter:
    orig_main: Set[Index] = field(default_factory=lambda: set())
    orig_var: Set[Index] = field(default_factory=lambda: set())
    trans_main: Set[Index] = field(default_factory=lambda: set())
    trans_var: Set[Index] = field(default_factory=lambda: set())

    def __iadd__(self, other: "Counter") -> "Counter":
        self.orig_main = self.orig_main.union(other.orig_main)
        self.orig_var = self.orig_var.union(other.orig_var)
        self.trans_main = self.trans_main.union(other.trans_main)
        self.trans_var = self.trans_var.union(other.trans_var)
        return self

    def get_counts(self, trans: bool = False) -> Tuple[int, int]:
        if trans:
            return (len(self.trans_main), len(self.trans_var))
        return (len(self.orig_main), len(self.orig_var))
