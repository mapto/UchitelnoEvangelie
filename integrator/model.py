from typing import Optional, List, Set
from dataclasses import dataclass, field

import re


@dataclass(init=True, repr=True, order=True)
class Index:
    ch: int
    page: str
    row: int
    bold: bool = False
    italic: bool = False

    @staticmethod
    def unpack(value: str) -> "Index":
        m = re.search(r"(\d{1,2})/((\d{1,2}|W?\d{3})[abcd])(\d{1,2})", value)
        assert m
        # print(m.groups())
        ch = int(m.group(1))
        page = m.group(2)
        row = int(m.group(4))
        return Index(ch, page, row)

    def __str__(self):
        return f"{self.ch}/{self.page}{self.row}"

    def longstr(self):
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
