from typing import Optional, List, Dict
from dataclasses import dataclass, field

import re

from const import IDX_COL, EXAMPLE_COL, STYLE_COL


@dataclass(init=True, repr=True, order=True)
class Index:
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
    def unpack(value: str) -> "Index":
        """
        >>> Index.unpack("1/W167c4").longstr()
        '01/W167c04'
        >>> str(Index.unpack("1/6c4"))
        '1/6c4'
        >>> str(Index.unpack("1/6c4var"))
        '1/6c4var'
        >>> str(Index.unpack("1/6c4-8"))
        '1/6c4-8'
        >>> str(Index.unpack("1/6c4-8var"))
        '1/6c4-8var'
        >>> str(Index.unpack("1/6c4-d4"))
        '1/6c4-d4'
        >>> str(Index.unpack("1/6c4-6d4"))
        '1/6c4-d4'
        >>> str(Index.unpack("1/6c4-7d4"))
        '1/6c4-7d4'
        >>> str(Index.unpack("1/6c4-2/6d4"))
        '1/6c4-2/6d4'
        >>> str(Index.unpack("1/6c4var-2/6d4var"))
        '1/6c4var-2/6d4var'

        >>> Index.unpack("1/6a8") < Index.unpack("1/6a17")
        True
        >>> Index.unpack("1/6a8") < Index.unpack("1/W167c4")
        True
        >>> Index.unpack("2/6a8") < Index.unpack("2/W167c4")
        False

        Regex using: https://pythex.org/
        """
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
        var = not not m.group(6)

        end = None
        if m.group(15):
            e_ch = ch
            e_alt = alt
            e_page = page
            e_col = col
            e_row = int(m.group(15))
            e_var = not not m.group(16)
            if m.group(14):
                e_col = m.group(14)
                if m.group(13):
                    e_page = int(m.group(13))
                    if m.group(11):
                        e_ch = int(m.group(11))
                    e_alt = not not m.group(12) if e_ch % 2 else not m.group(12)
            end = Index(e_ch, e_alt, e_page, e_col, e_row, e_var)

        return Index(ch, alt, page, col, row, var, end)

    def __str__(self):
        """
        >>> str(Index(1, False, 6, "c", 4, False, Index(1, False, 6, "d", 4)))
        '1/6c4-d4'
        >>> str(Index(1, False, 6, "c", 4, False, Index(1, False, 6, "c", 11)))
        '1/6c4-11'
        >>> str(Index(1, False, 6, "c", 4, True, Index(1, False, 6, "d", 4, True)))
        '1/6c4var-d4var'
        >>> str(Index(1, True, 6, "c", 4))
        '1/W6c4'
        >>> str(Index(2, False, 6, "c", 4))
        '2/W6c4'
        """
        w = "W" if not not self.ch % 2 == self.alt else ""
        v = "var" if self.var else ""
        start = f"{self.ch}/{w}{self.page}{self.col}{self.row}{v}"
        if self.end:
            if self.end.ch != self.ch:
                return f"{start}-{str(self.end)}"
            ev = "var" if self.end.var else ""
            if self.end.alt != self.alt:
                ew = "W" if self.end.alt and self.end.ch % 2 else ""
                return f"{start}-{ew}{self.end.page}{self.end.col}{self.end.row}{ev}"
            if self.end.page != self.page:
                return f"{start}-{self.end.page}{self.end.col}{self.end.row}{ev}"
            if self.end.col != self.col:
                return f"{start}-{self.end.col}{self.end.row}{ev}"
            if self.end.row != self.row:
                return f"{start}-{self.end.row}{ev}"
        return start

    def longstr(self):
        """
        >>> Index(1, False, 6, "c", 4, False, Index(2, True, 6, "c", 4)).longstr()
        '01/006c04-02/006c04'
        >>> Index(1, False, 6, "c", 4, True, Index(2, True, 6, "c", 4)).longstr()
        '01/006c04var-02/006c04'
        >>> Index(1, False, 6, "c", 4, False, Index(2, True, 6, "c", 4, True)).longstr()
        '01/006c04-02/006c04var'
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


@dataclass(init=True, repr=True)
class LangSemantics:
    lang: str
    word: int
    lemmas: List[int]
    var: Optional["LangSemantics"] = None


@dataclass(init=True, repr=True)
class TableSemantics:
    sl: "LangSemantics"
    gr: "LangSemantics"
    idx: int = IDX_COL
    example: int = EXAMPLE_COL
    style: int = STYLE_COL

    def word_cols(self) -> Dict[str, int]:
        """extract named columns"""
        r = {"slgroup": self.sl.word, "grgroup": self.gr.word}
        if self.sl.var:
            r["slvargroup"] = self.sl.var.word
        if self.gr.var:
            r["grvargroup"] = self.gr.var.word
        return r
