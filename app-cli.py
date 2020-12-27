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

# from importer import import_lines, parse_comments
from importer import import_chapter
from processor import dehyphenate, condense, integrate_words
from exporter import export_sheet

if __name__ == "__main__":
    args = docopt(__doc__)
    fname = args["<docx>"]
    if len(fname) < 6 or "." not in fname[2:]:
        fname += ".docx"
    elif not fname.lower().endswith(".docx"):
        print("Файлът трябва да е във формат .docx. Моля конвертирайте го")
        exit()
    # fname = "../text/00-Prolog-tab.docx"
    # # fname = "../text/01-slovo1-tab.docx"
    # book_index = import_lines(fname)
    # print(book_index)
    # comments = parse_comments(Document(fname))
    # print(comments)
    # transformed = transform_clean(book_index)
    # print(transformed)
    # book_lines = split_rows(transformed, comments)
    # print(book_lines)

    print("Импорт...")
    lines = import_chapter(fname)
    print(f"{len(lines)} думи")

    # print(lines)
    # export_sheet(lines, fname + ".1.xlsx")

    print("Премахване на пренос...")
    lines = dehyphenate(lines)
    # export_sheet(lines, fname[:-5] + ".1.xlsx")
    print(f"{len(lines)} думи")

    print("Възстановяване на думи, разделени от коментари...")
    # print(lines)
    lines = integrate_words(lines)
    # export_sheet(lines, fname[:-5] + ".2.xlsx")
    # print(lines)
    print(f"{len(lines)} думи")

    # export_sheet(lines, fname + ".2.xlsx")

    print("Премахване на празни думи...")
    lines = condense(lines)
    # export_sheet(lines, fname[:-5] + ".3.xlsx")
    print(f"{len(lines)} думи")

    print("Експорт")
    export_sheet(lines, fname[:-5] + ".xlsx")
