#!/usr/bin/env python3

from typing import List, Tuple, Dict

from docx import Document  # type: ignore
from docx.table import _Cell  # type: ignore
from lxml import etree  # type: ignore

ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
tag_commentStart = (
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}commentRangeStart"
)
tag_commentEnd = (
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}commentRangeEnd"
)
tag_paragraph = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"
tag_run = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r"


def import_comments(doc: Document) -> Dict[int, str]:
    """Returns idx->content"""
    xml = None
    result: Dict[int, str] = {}
    for part in doc.part.package.parts:
        if part.partname == "/word/comments.xml":
            xml = part.blob
    if not xml:
        return result

    root = etree.fromstring(xml)
    for next in root.getchildren():
        # print(next.attrib)
        id = int(next.xpath("./@w:id", namespaces=ns)[0])
        text = "".join(next.xpath(".//w:t/text()", namespaces=ns))
        result[id] = text
    return result


def locate_comments(cell: _Cell) -> Dict[int, str]:
    id = None
    text = ""
    anchors = {}

    for par in cell._element:
        if par.tag != tag_paragraph:
            continue
        for child in par:
            if id is not None and child.tag == tag_run:
                # take only last line of marked text
                if "\n" in child.text:
                    text = child.text.split("\n")[-1]
                else:
                    text += child.text
            elif child.tag == tag_commentStart:
                id = int(child.xpath("./@w:id", namespaces=ns)[0])
                text = ""
            elif child.tag == tag_commentEnd:
                assert id == int(child.xpath("./@w:id", namespaces=ns)[0])
                anchors[id] = text
                id = None
                text = ""
    return anchors


def import_lines(fname: str = "sample.docx") -> Dict[str, Tuple[str, List[int]]]:
    """Returns line_num->line_text,line_comments"""
    print("File: %s" % fname)
    doc = Document(fname)
    book_prefix = int(fname.split("/")[-1].split("-")[0])
    print("Book: %s" % book_prefix)

    comments = import_comments(doc)
    comments_found: List[int] = []

    book_index = {}
    for page in doc.tables:
        page_name = page.cell(0, 0).text
        page_rows_nums = page.cell(1, 0).text.split("\n")
        cell = page.cell(1, 1)
        text = cell.text

        # print(cell._element.getchildren())
        anchors = locate_comments(cell)
        comments_found.extend(anchors.keys())

        # assertion: comment selections do not contain newline
        assert not [v for v in anchors.values() if v.find("\n") != -1]

        page_rows = text.split("\n")
        # if nums less then rows, extend nums counter
        if len(page_rows_nums) < len(page_rows):
            extension = [
                str(int(page_rows_nums[-1]) + i)
                for i in range(1, 1 + len(page_rows) - len(page_rows_nums))
            ]
            page_rows_nums.extend(extension)

        assert len(page_rows_nums) == len(page_rows)
        for i, n in enumerate(page_rows_nums):
            row_idx = "%d/%s%d" % (book_prefix, page_name, int(n))
            relevant_comments = [k for k, v in anchors.items() if v in page_rows[i]]
            book_index[row_idx] = (page_rows[i], relevant_comments)

    # print(comments_found)
    # print(list(comments.keys()))
    # not all comments are in text
    assert len(comments_found) <= len(comments.keys())
    return book_index


if __name__ == "__main__":
    # import_lines("../text/01-slovo1-tab.docx")
    # book_lines = import_lines("../text/00-Prolog-tab.docx")
    print(import_lines("../new/01-slovo1-tab.docx"))
    # print(import_comments(Document('../new/01-slovo1-tab.docx')))
    # print(locate_comments(Document('../new/01-slovo1-tab.docx').tables[0].cell(1,1)._element[1]))
