#!/usr/bin/env python3
"""App-cli.

Usage:
  app-cli.py <docx>
"""
"""Създаване на индекс за Учително евангелие - изпълнение чрез команден интерфейс.
Запишете файла в директорията където 

Usage:
Употреба:
  app-cli.py <docx>
"""
from docopt import docopt  # type: ignore

from docx import Document  # type: ignore

from importer import import_lines, import_comments
from processor import transform_clean, split_rows
from exporter import export_sheet

if __name__ == "__main__":
    args = docopt(__doc__)
    fname = args["<docx>"]
    # fname = "../text/00-Prolog-tab.docx"
    # # fname = "../text/01-slovo1-tab.docx"
    book_index = import_lines(fname)
    # print(book_index)
    comments = import_comments(Document(fname))
    # print(comments)
    transformed = transform_clean(book_index)
    # print(transformed)
    book_lines = split_rows(transformed, comments)
    # print(book_lines)
    export_sheet(book_lines, fname + ".xlsx")
