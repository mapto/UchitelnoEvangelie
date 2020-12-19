from typing import List
from dataclasses import dataclass, field

import re
from lxml.etree import _Element  # type: ignore

from schema import ns


@dataclass(init=True, repr=True)
class Comment:
    id: int
    ref: List[str] = field(default_factory=lambda: [])
    annotation: str = ""
    addition: str = ""

    @classmethod
    def fromXml(self, node: _Element):
        id = int(node.xpath("./@w:id", namespaces=ns)[0])
        content = "".join(node.xpath(".//w:t/text()", namespaces=ns))
        if content.find("+") == -1:
            annotation = content
            addition = ""
        else:
            parts = re.split(r"\+", content)
            assert len(parts) == 2
            annotation = parts[0]
            addition = parts[1]
        return Comment(id, annotation=annotation, addition=addition)
