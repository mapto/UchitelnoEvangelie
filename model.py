from typing import Optional, List
from dataclasses import dataclass, field

import re
from lxml.etree import _Element  # type: ignore

from schema import ns


@dataclass(init=True, repr=True)
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


@dataclass(init=True, repr=True)
class Index:
    ch: int
    page: str
    row: int

    def __str__(self):
        return f"{self.ch:02d}/{self.page}{self.row:02d}"


@dataclass(init=True, repr=True)
class Word:
    """Annotated words"""

    _index: Index
    word: str = ""
    line_context: str = ""
    variant: str = ""
    prev: Optional["Word"] = field(init=False, repr=False, default=None)
    next: Optional["Word"] = field(init=False, repr=False, default=None)

    def appendTo(self, other: "Word") -> None:
        self.prev = other
        other.next = self

    def prependTo(self, other: "Word") -> None:
        self.next = other
        other.prev = self

    def insertBetween(self, before: "Word", after: "Word") -> None:
        assert before.next == after
        assert after.prev == before

        self.prependTo(before)
        self.appendTo(after)

    def index(self):
        return self._index.__str__()

    def __str__(self):
        prev = self.prev.word if self.prev else None
        next = self.next.word if self.next else None
        return f"{self.index()}: {self.word},\t'{self.variant}'\t[{prev},{next}]"
