from typing import Optional, List, Set
from dataclasses import dataclass, field

import re


@dataclass(init=True, repr=True, order=True)
class Index:
    ch: int
    page: str
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
        >>> str(Index.unpack("1/6c4-6d4"))
        '1/6c4-6d4'
        >>> str(Index.unpack("1/6c4-7d4"))
        '1/6c4-7d4'
        >>> str(Index.unpack("1/6c4-2/6d4"))
        '1/6c4-2/6d4'

        Regex using: https://pythex.org/
        """
        m = re.search(
            r"(\d{1,2})/((\d{1,2}|W?\d{3})[abcd])(\d{1,2})(-(((\d{1,2})/)?((\d{1,2}|W?\d{3})[abcd]))?(\d{1,2}))?",
            value,
        )
        assert m
        # print(m.groups())
        ch = int(m.group(1))
        page = m.group(2)
        row = int(m.group(4))

        end = None
        if m.group(11):
            if m.group(9):
                if m.group(8):
                    end = Index(int(m.group(8)), m.group(9), int(m.group(11)))
                else:
                    end = Index(ch, m.group(9), int(m.group(11)))
            else:
                end = Index(ch, page, int(m.group(11)))

        return Index(ch, page, row, end)

    def __str__(self):
        """
        >>> str(Index(1, "6c", 4, Index(1, "6d", 4)))
        '1/6c4-6d4'
        >>> str(Index(1, "6c", 4, Index(1, "6c", 11)))
        '1/6c4-11'
        """
        if self.end:
            if self.end.ch != self.ch:
                return f"{self.ch}/{self.page}{self.row}-{str(self.end)}"
            if self.end.page != self.page:
                return f"{self.ch}/{self.page}{self.row}-{self.end.page}{self.end.row}"
            if self.end.row != self.row:
                return f"{self.ch}/{self.page}{self.row}-{self.end.row}"
        return f"{self.ch}/{self.page}{self.row}"

    def longstr(self):
        """
        >>> Index(1, "6c", 4, Index(2, "6c", 4)).longstr()
        '01/6c04-02/6c04'
        """
        if self.end:
            if self.end.ch != self.ch:
                return f"{self.ch:02d}/{self.page}{self.row:02d}-{self.end.longstr()}"
            if self.end.page != self.page:
                return f"{self.ch:02d}/{self.page}{self.row:02d}-{self.end.page}{self.end.row:02d}"
            if self.end.row != self.row:
                return f"{self.ch:02d}/{self.page}{self.row:02d}-{self.end.row:02d}"
        return f"{self.ch:02d}/{self.page}{self.row:02d}"


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
