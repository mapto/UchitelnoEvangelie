from typing import Optional, List, Set
from dataclasses import dataclass, field

import re


@dataclass(init=True, repr=True, order=True)
class Index:
    ch: int
    alt: bool
    page: int
    col: str
    row: int
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
        >>> str(Index.unpack("1/6c4-8"))
        '1/6c4-8'
        >>> str(Index.unpack("1/6c4-d4"))
        '1/6c4-d4'
        >>> str(Index.unpack("1/6c4-6d4"))
        '1/6c4-d4'
        >>> str(Index.unpack("1/6c4-7d4"))
        '1/6c4-7d4'
        >>> str(Index.unpack("1/6c4-2/6d4"))
        '1/6c4-2/6d4'

        >>> Index.unpack("1/6a8") < Index.unpack("1/6a17")
        True
        >>> Index.unpack("1/6a8") < Index.unpack("1/W167c4")
        True
        >>> Index.unpack("2/6a8") < Index.unpack("2/W167c4")
        False

        Regex using: https://pythex.org/
        """
        m = re.search(
            # r"(\d{1,2})/(W)?(\d{1,3})([abcd])(\d{1,2})(-(((\d{1,2})/)?((\d{1,3}|W?\d{3})[abcd]))?(\d{1,2}))?",
            r"(\d{1,2})/(W)?(\d{1,3})([abcd])(\d{1,2})(-((((\d{1,2})/)?(W)?(\d{1,3}))?([abcd]))?(\d{1,2}))?",
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

        end = None
        if m.group(14):
            if m.group(13):
                if m.group(12):
                    if m.group(10):
                        e_ch = int(m.group(10))
                        e_alt = not not m.group(11) if e_ch % 2 else not m.group(11)
                        end = Index(
                            e_ch, e_alt, int(m.group(12)), m.group(13), int(m.group(14))
                        )
                    else:
                        e_alt = not not m.group(11) if ch % 2 else not m.group(11)
                        end = Index(
                            ch, e_alt, int(m.group(12)), m.group(13), int(m.group(14))
                        )
                else:
                    end = Index(ch, alt, page, m.group(13), int(m.group(14)))
            else:
                end = Index(ch, alt, page, col, int(m.group(14)))

        return Index(ch, alt, page, col, row, end)

    def __str__(self):
        """
        >>> str(Index(1, False, 6, "c", 4, Index(1, False, 6, "d", 4)))
        '1/6c4-d4'
        >>> str(Index(1, False, 6, "c", 4, Index(1, False, 6, "c", 11)))
        '1/6c4-11'
        >>> str(Index(1, True, 6, "c", 4))
        '1/W6c4'
        >>> str(Index(2, False, 6, "c", 4))
        '2/W6c4'
        """
        w = "W" if not not self.ch % 2 == self.alt else ""
        if self.end:
            if self.end.ch != self.ch:
                return f"{self.ch}/{w}{self.page}{self.col}{self.row}-{str(self.end)}"
            if self.end.alt != self.alt:
                ew = "W" if self.end.alt and self.end.ch % 2 else ""
                return (
                    f"{self.ch}/{w}{self.page}{self.col}{self.row}-"
                    f"{ew}{self.end.page}{self.end.col}{self.end.row}"
                )
            if self.end.page != self.page:
                return (
                    f"{self.ch}/{w}{self.page}{self.col}{self.row}-"
                    f"{self.end.page}{self.end.col}{self.end.row}"
                )
            if self.end.col != self.col:
                return (
                    f"{self.ch}/{w}{self.page}{self.col}{self.row}-"
                    f"{self.end.col}{self.end.row}"
                )
            if self.end.row != self.row:
                return f"{self.ch}/{w}{self.page}{self.col}{self.row}-{self.end.row}"
        return f"{self.ch}/{w}{self.page}{self.col}{self.row}"

    def longstr(self):
        """
        >>> Index(1, False, 6, "c", 4, Index(2, True, 6, "c", 4)).longstr()
        '01/006c04-02/006c04'
        """
        w = "W" if not not self.ch % 2 == self.alt else ""
        if self.end:
            if self.end.ch != self.ch:
                return f"{self.ch:02d}/{w}{self.page:03d}{self.col}{self.row:02d}-{self.end.longstr()}"
            if self.end.alt != self.alt:
                ew = "W" if self.end.alt and self.end.ch % 2 else ""
                return (
                    f"{self.ch:02d}/{w}{self.page:03d}{self.col}{self.row:02d}-"
                    f"{ew}{self.end.page:03d}{self.end.col}{self.end.row:02d}"
                )
            if self.end.page != self.page:
                return (
                    f"{self.ch:02d}/{w}{self.page:03d}{self.col}{self.row:02d}-"
                    f"{self.end.page:03d}{self.end.col}{self.end.row:02d}"
                )
            if self.end.col != self.col:
                return (
                    f"{self.ch:02d}/{w}{self.page:03d}{self.col}{self.row:02d}-"
                    f"{self.end.col}{self.end.row:02d}"
                )
            if self.end.row != self.row:
                return f"{self.ch:02d}/{w}{self.page:03d}{self.col}{self.row:02d}-{self.end.row:02d}"
        return f"{self.ch:02d}/{w}{self.page:03d}{self.col}{self.row:02d}"


@dataclass(init=True, repr=True)
class LangSemantics:
    lang: str
    word: int
    lemmas: List[int]


@dataclass(init=True, repr=True)
class TableSemantics:
    sl: "LangSemantics"
    gr: "LangSemantics"
    idx: int = 3
    example: int = 5
    style: int = 16
