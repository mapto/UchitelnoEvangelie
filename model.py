from typing import Optional, List
from dataclasses import dataclass, field

import re
from lxml.etree import _Element  # type: ignore

from schema import ns


@dataclass(init=True, repr=True)
class Comment:
    """
    :param: ref represents comment selection, split into lines
    :param: annotation (before +) and addition (after +) are extracted from comment contents
    """

    id: int
    ref: List[str] = field(default_factory=lambda: [])
    annotation: str = ""
    addition: str = ""

    @classmethod
    def fromXml(self, node: _Element):
        id = int(node.xpath("./@w:id", namespaces=ns)[0])
        content = "".join(node.xpath(".//w:t/text()", namespaces=ns))
        parts = re.split(r"\+", content)
        assert 1 <= len(parts) <= 2
        addition = parts[1] if len(parts) == 2 else ""
        return Comment(id, annotation=parts[0], addition=addition)


@dataclass(init=True, repr=True)
class Word:
    ch: int
    page: str
    row: int
    word: str = ""
    line_context: str = ""
    variant: str = ""
    prev: Optional["Word"] = field(init=False, repr=False, default=None)
    next: Optional["Word"] = field(init=False, repr=False, default=None)

    def index(self):
        return f"{self.ch:02d}/{self.page}{self.row:02d}"

    def __str__(self):
        return f"{self.index()}: {self.word}, '{self.variant}'"
