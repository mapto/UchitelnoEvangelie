from dataclasses import dataclass, field
from lxml.etree import _Element  # type: ignore

from schema import ns


@dataclass(init=True, repr=True)
class Comment:
    id: int
    ref: str = ""
    content: str = ""

    @classmethod
    def fromXml(self, node: _Element):
        id = int(node.xpath("./@w:id", namespaces=ns)[0])
        content = "".join(node.xpath(".//w:t/text()", namespaces=ns))
        return Comment(id, content=content)
