from typing import Optional, List, Set
from dataclasses import dataclass, field


@dataclass(init=True, repr=True, order=True)
class Index:
    value: str
    bold: bool
    italic: bool


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
