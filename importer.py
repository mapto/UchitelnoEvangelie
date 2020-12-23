#!/usr/bin/env python3

from typing import List, Tuple, Dict

import re

from docx import Document  # type: ignore
from docx.table import _Cell  # type: ignore
from lxml import etree, html  # type: ignore

from schema import ns
from schema import (
    tag_paragraph,
    tag_run,
    tag_commentStart,
    tag_commentEnd,
    tag_text,
    tag_br,
)
from model import Comment, Word


def parse_comments(doc: Document) -> Dict[int, Comment]:
    xml = None
    result: Dict[int, Comment] = {}
    for part in doc.part.package.parts:
        if part.partname == "/word/comments.xml":
            xml = part.blob
    if not xml:
        return result

    root = etree.fromstring(xml)
    for next in root.getchildren():
        c = Comment.fromXml(next)
        result[c.id] = c

    return result


def compile_words(ch: int, page: str, row: int, line: str, comment: str) -> List[Word]:
    result: List[Word] = []
    words = re.split(r"\s", line)
    for w in words:
        new_word = Word(ch, page, row, w, line, variant=comment)
        if result:
            result[-1].next = new_word
            new_word.prev = result[-1]
        result.append(new_word)
    return result


def parse_page(
    ch: int, page: str, rows: List[int], cell: _Cell, comments: Dict[int, Comment]
) -> List[Word]:
    result: List[Word] = []
    open_comments: List[int] = []
    # anchors: Dict[int, str] = {}
    line = ""
    row = rows.pop(0)
    for par in cell._element:
        if par.tag != tag_paragraph:
            continue
        for sec in par:
            if sec.tag == tag_run:
                for content in sec:
                    if content.tag == tag_text:
                        line += content.text
                    elif content.tag == tag_br:
                        comment = ",".join(
                            [comments[c].annotation for c in open_comments]
                        )
                        compiled = compile_words(ch, page, row, line, comment)
                        if result:
                            result[-1].next = compiled[0]
                            compiled[0].prev = result[-1]
                        result.extend(compiled)
                        line = ""
                        row = rows.pop(0)
                        if not rows:
                            rows.append(row + 1)
            elif sec.tag == tag_commentStart:
                comment = ",".join([comments[c].annotation for c in open_comments])
                compiled = compile_words(ch, page, row, line, comment)
                if result:
                    result[-1].next = compiled[0]
                    compiled[0].prev = result[-1]
                result.extend(compiled)
                line = ""

                id = int(sec.xpath("./@w:id", namespaces=ns)[0])
                open_comments.append(id)
            elif sec.tag == tag_commentEnd:
                # print(open_comments)
                # print(comments)
                comment = ",".join([comments[c].annotation for c in open_comments])
                compiled = compile_words(ch, page, row, line, comment)
                if result:
                    result[-1].next = compiled[0]
                    compiled[0].prev = result[-1]
                result.extend(compiled)
                line = ""

                comment = ",".join([comments[c].addition for c in open_comments])
                if comment:
                    new_word = Word(ch, page, row, variant=comment)
                    result[-1].next = new_word
                    new_word.prev = result[-1]
                    result.append(new_word)

                id = int(sec.xpath("./@w:id", namespaces=ns)[0])
                open_comments.remove(id)

    # at end all comment starts should be matched by comment ends
    assert not open_comments

    return result


def parse_document(ch: int, doc: Document, comments: Dict[int, Comment]) -> List[Word]:
    words: List[Word] = []
    for page in doc.tables:
        page_name = page.cell(0, 0).text
        page_rows_nums = [int(r) for r in page.cell(1, 0).text.split("\n") if r]
        cell = page.cell(1, 1)
        page_words = parse_page(ch, page_name, page_rows_nums, cell, comments)
        if words:
            words[-1].next = page_words[0].prev
            page_words[0].prev = words[-1].next
        words.extend(page_words)
    return words


def import_chapter(fname: str) -> List[Word]:
    """Import a preformatted chapter of a manuscript
    """
    doc = Document(fname)
    book_prefix = int(fname.split("/")[-1].split("-")[0])
    comments = parse_comments(doc)
    # print(comments)
    return parse_document(book_prefix, doc, comments)


if __name__ == "__main__":
    # import_lines("../text/01-slovo1-tab.docx")
    # book_lines = import_lines("../text/00-Prolog-tab.docx")
    # print(import_lines("../new/01-slovo1-tab.docx"))
    # print(import_comments(Document('../new/01-slovo1-tab.docx')))
    # print(locate_comments(Document('../new/01-slovo1-tab.docx').tables[0].cell(1,1)._element[1]))
    import_chapter("test/01-slovo1-4b.docx")
