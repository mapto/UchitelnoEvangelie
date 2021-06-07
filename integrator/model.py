from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

import re

from const import IDX_COL, EXAMPLE_COL, STYLE_COL


@dataclass(order=True, frozen=True)
class Index:
    ch: int
    alt: bool  # means alternative indexing
    page: int
    col: str
    row: int
    var: str = ""
    end: Optional["Index"] = None
    bold: bool = False
    italic: bool = False

    @staticmethod
    def unpack(value: str, b: bool = False, i: bool = False, var: str = "") -> "Index":
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
        >>> str(Index(1, False, 6, "c", 4, "", Index(1, False, 6, "d", 4)))
        '1/6c4-d4'
        >>> str(Index(1, False, 6, "c", 4, "", Index(1, False, 6, "c", 11)))
        '1/6c4-11'

        Variants are not shown:
        >>> str(Index(1, False, 6, "c", 4, "WH", Index(1, False, 6, "d", 4, "WH")))
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
        >>> Index(1, False, 6, "c", 4, "", Index(2, True, 6, "c", 4)).longstr()
        '01/006c04-02/006c04'

        >> Index(1, False, 6, "c", 4, "WH", Index(2, True, 6, "c", 4)).longstr()
        '01/006c04WH-02/006c04'
        >> Index(1, False, 6, "c", 4, "", Index(2, True, 6, "c", 4, "WH")).longstr()
        '01/006c04-02/006c04WH'
        """
        w = "W" if not not self.ch % 2 == self.alt else ""
        v = self.var
        start = f"{self.ch:02d}/{w}{self.page:03d}{self.col}{self.row:02d}{v}"
        if self.end:
            if self.end.ch != self.ch:
                return f"{start}-{self.end.longstr()}"
            ev = self.end.var
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
    """Here alt means other other transcriptions (main or var)"""

    idx: Index
    lang: str
    orig_alt: str = ""
    orig_alt_var: List[str] = field(default_factory=lambda: [])
    trans_alt: str = ""
    trans_alt_var: List[str] = field(default_factory=lambda: [])

    def __hash__(self):
        return hash((self.idx, self.lang, self.orig_alt, self.trans_alt))

    def suffix(self):
        """
        >>> idx = Index.unpack("1/1a1")
        >>> Usage(idx, "sl").suffix()
        ''
        >>> Usage(idx, "sl",  "дноѧдъ", ["ноѧдъ"]).suffix()
        ' cf. \ue201д\ue205но\ue20dѧдъ, [\ue205но\ue20dѧдъ]'
        >>> Usage(idx, "sl",  "", [], "ὑπερκλύζω").suffix()
        ' cf. ὑπερκλύζω'
        >>> Usage(idx, "sl",  "", [], "", ["ὑπερβλύω"]).suffix()
        ' cf. {ὑπερβλύω}'
        >>> Usage(idx, "gr",  "ὑπερκλύζω").suffix()
        ' cf. ὑπερκλύζω'
        >>> Usage(idx, "gr",  "", ["ὑπερβλύω"]).suffix()
        ' cf. {ὑπερβλύω}'
        """
        if (
            not self.orig_alt
            and not self.orig_alt_var
            and not self.trans_alt
            and not self.trans_alt_var
        ):
            return ""
        result = []
        if self.orig_alt:
            result.append(self.orig_alt)
        if self.orig_alt_var:
            if self.lang == "sl":
                result.append(f"[{', '.join(self.orig_alt_var)}]")
            else:
                result.append(f"{{{', '.join(self.orig_alt_var)}}}")
        if self.trans_alt:
            result.append(self.trans_alt)
        if self.trans_alt_var:
            if self.lang == "sl":
                result.append(f"{{{', '.join(self.trans_alt_var)}}}")
            else:
                result.append(f"[{', '.join(self.trans_alt_var)}]")
        return f" cf. {', '.join(result)}"


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


@dataclass
class MainLangSemantics(LangSemantics):
    var: "VarLangSemantics"

    def __post_init__(self):
        """
        If there is variant, make sure add correct number of lemma columns.
        relevant, because different language/variant combinations have different number of lemma columns.
        """
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
        if not self.var or not row[self.var.lemmas[0]]:
            return ("", [])
        return ("", [row[self.var.lemmas[0]]])


@dataclass
class VarLangSemantics(LangSemantics):
    """ main is nullable just because it's a recursive reference and setting up needs to happen post-init"""

    main: Optional["MainLangSemantics"] = None

    def alternatives(self, row: List[str]) -> Tuple[str, List[str]]:
        if not self.main or not row[self.main.lemmas[0]]:
            return ("", [])
        return (row[self.main.lemmas[0]], [])


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
