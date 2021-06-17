from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from sortedcontainers import SortedDict, SortedSet  # type: ignore

import re

from const import CF_SEP
from const import IDX_COL, EXAMPLE_COL, STYLE_COL
from const import DEFAULT_SL, DEFAULT_GR

from util import base_word, build_paths


def _present(row: List[str], sem: Optional["LangSemantics"]) -> bool:
    return not not sem and not not row[sem.lemmas[0]]


def _compile_usage(
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


def _get_variant(row, orig: "LangSemantics") -> str:
    return "".join([k for k in orig.multiword(row).keys()])


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
    orig_alt_var: List[str] = field(default_factory=lambda: [])
    trans_alt: str = ""
    trans_alt_var: List[str] = field(default_factory=lambda: [])

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

    def alternatives(self, row: List[str]) -> Tuple[str, List[str]]:
        raise NotImplementedError("abstract method")

    def key(self, text: str) -> str:
        raise NotImplementedError("abstract method")

    def build_key(self, row: List[str]) -> str:
        raise NotImplementedError("abstract method")

    def multiword(self, row: List[str]) -> Dict[str, str]:
        raise NotImplementedError("abstract method")

    def multilemma(self, row: List[str]) -> Dict[str, str]:
        raise NotImplementedError("abstract method")

    def build_usages(
        self, trans: "LangSemantics", row: List[str], d: SortedDict
    ) -> SortedDict:
        raise NotImplementedError("abstract method")


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

    def alternatives(self, row: List[str]) -> Tuple[str, List[str]]:
        alt = list(self.var.multilemma(row).values())
        return ("", alt)

    def key(self, text: str) -> str:
        return text

    def build_key(self, row: List[str]) -> str:
        result = ""
        if _present(row, self) and self.word != None and not not row[self.word]:
            result += self.key(f"{base_word(row[self.word])}")
        if (
            _present(row, self.var)
            and self.var.word != None
            and not not row[self.var.word]
        ):
            result += self.var.key(f"{base_word(row[self.var.word])}")
        return result

    def multiword(self, row: List[str]) -> Dict[str, str]:
        """Main variant does not have multiple words in a cell"""
        return {}

    def multilemma(self, row: List[str]) -> Dict[str, str]:
        """Main variant does not have multiple words in a cell"""
        return {}

    def build_usages(
        self, trans: "LangSemantics", row: List[str], d: SortedDict
    ) -> SortedDict:
        orig_key = self.build_key(row)
        trans_key = trans.build_key(row)
        key = (orig_key, trans_key)

        b = "bold" in row[STYLE_COL]
        i = "italic" in row[STYLE_COL]
        idx = Index.unpack(row[IDX_COL], b, i)
        var = _get_variant(row, self) + _get_variant(row, trans)
        oalt = self.alternatives(row)
        talt = trans.alternatives(row)
        val = Usage(idx, self.lang, var, oalt[0], oalt[1], talt[0], talt[1])
        for nxt in build_paths(row, trans.lemmas):
            d = _compile_usage(val, nxt, key, d)
        return d


@dataclass
class VarLangSemantics(LangSemantics):
    """ main is nullable just because it's a recursive reference and setting up needs to happen post-init"""

    main: Optional["MainLangSemantics"] = None

    def alternatives(self, row: List[str]) -> Tuple[str, List[str]]:
        main = ""
        if self.main and row[self.main.lemmas[0]]:
            main = row[self.main.lemmas[0]]
        alt = list(self.multilemma(row).values())
        return (main, alt)

    def key(self, text: str) -> str:
        m = re.search(r"^([^A-Z]+)([A-Z]+)$", text.strip())
        if m:
            text = m.group(1).strip()
        return f" {{{text}}}"

    def build_key(self, row: List[str]) -> str:
        result = ""
        assert self.main
        if (
            _present(row, self.main)
            and self.main.word != None
            and not not row[self.main.word]
        ):
            result += self.main.key(f"{base_word(row[self.main.word])}")
        if _present(row, self) and self.word != None and not not row[self.word]:
            result += self.key(f"{base_word(row[self.word])}")
        return result

    def multiword(self, row: List[str]) -> Dict[str, str]:
        result = {}
        m = re.search(r"^([^A-Z]+)([A-Z]+)(.*)$", row[self.word].strip())
        while m:
            result[m.group(2)] = m.group(1).strip()
            rest = m.group(3).strip()
            m = re.search(r"^([^A-Z]+)([A-Z]+)(.*)$", rest)
        if not result:
            default = DEFAULT_SL if self.lang == "sl" else DEFAULT_GR
            return {default: row[self.word].strip()}
        return result

    def multilemma(self, row: List[str]) -> Dict[str, str]:
        result = {}
        m = re.search(
            r"^([^A-Z]+)([A-Z]+)(\s*\&\s*)?(.*)$", row[self.lemmas[0]].strip()
        )
        while m:
            result[m.group(2)] = m.group(1).strip() if m.group(1) else ""
            rest = m.group(4).strip() if len(m.groups()) == 4 else ""
            m = re.search(r"^([^A-Z]+)([A-Z]+)(.*)$", rest)
        return result

    def build_usages(
        self, trans: "LangSemantics", row: List[str], d: SortedDict
    ) -> SortedDict:
        orig_key = self.build_key(row)
        trans_key = trans.build_key(row)
        key = (orig_key, trans_key)

        b = "bold" in row[STYLE_COL]
        i = "italic" in row[STYLE_COL]
        idx = Index.unpack(row[IDX_COL], b, i)
        var = _get_variant(row, self) + _get_variant(row, trans)
        oalt = self.alternatives(row)
        talt = trans.alternatives(row)
        val = Usage(idx, self.lang, var, oalt[0], oalt[1], talt[0], talt[1])
        for nxt in build_paths(row, trans.lemmas):
            d = _compile_usage(val, nxt, key, d)
        return d


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
