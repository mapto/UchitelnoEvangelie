from typing import List, Optional
from dataclasses import dataclass, field

import re
from lxml.etree import _Element  # type: ignore

from schema import ns


@dataclass
class Comment:
    """The structure of comments, relating to the text they relate to

    :param: ref represents comment selection, split into lines
    :param: annotation (before +) and addition (after +) are extracted from comment contents
    """

    id: int
    ref: List[str] = field(default_factory=lambda: [])
    annotation: str = ""
    addition: List[str] = field(default_factory=lambda: [])

    @classmethod
    def fromXml(self, node: _Element):
        id = int(node.xpath("./@w:id", namespaces=ns)[0])
        content = "".join(node.xpath(".//w:t/text()", namespaces=ns))
        parts = re.split(r"\+", content)
        assert 1 <= len(parts)
        annotation = content if len(parts) == 2 and not parts[1] else parts[0]
        addition = parts[1:] if len(parts) > 1 else []
        return Comment(id, annotation=annotation, addition=addition)


@dataclass
class Index:
    """
    >>> Index(0, "", 0) == Index(0, "", 0)
    True
    """

    ch: int
    page: str
    row: int

    def __str__(self):
        return f"{self.ch:02d}/{self.page}{self.row:02d}"

    def __eq__(self, other):
        return not not other and self.__repr__() == other.__repr__()


@dataclass
class Word:
    """Annotated words
    >>> Word(_index=Index(ch=1, page='4b', row=10), word='ѿ', line_context='ѿ оана⁘', variant='') == Word(_index=Index(ch=1, page='4b', row=10), word='ѿ', line_context='ѿ оана⁘', variant='')
    True
    """

    _index: Index
    word: str = ""
    line_context: str = ""
    variant: str = ""
    prev: Optional["Word"] = field(init=False, repr=False, default=None)
    next: Optional["Word"] = field(init=False, repr=False, default=None)

    def appendTo(self, other: Optional["Word"]) -> None:
        self.prev = other
        if other:
            other.next = self

    def prependTo(self, other: Optional["Word"]) -> None:
        self.next = other
        if other:
            other.prev = self

    def insertBetween(self, before: "Word", after: "Word") -> None:
        assert before.next == after
        assert after.prev == before

        self.prependTo(before)
        self.appendTo(after)

    def index(self) -> str:
        return str(self._index)

    def __str__(self) -> str:
        prev = self.prev.word if self.prev else None
        next = self.next.word if self.next else None
        return f"{self.index()}: {self.word},\t'{self.variant}'\t[{prev},{next}]"

    def __eq__(self, other) -> bool:
        if not other:
            return False
        if self._index != other._index:
            return False
        if (
            self.word != other.word
            or self.line_context != other.line_context
            or self.variant != other.variant
        ):
            return False
        return True
