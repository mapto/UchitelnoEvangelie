#!/usr/bin/env python3
"""Vocabulary extractor for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  extractor.py [-dIcp] <docx>
  extractor.py [--no-dehyphenate] [--integrate] [--no-condense] [--no-pause] <docx>

Options:
  -h --help                This information
  -v --version             Print version
  -d --no-dehyphenate   Disable removal of hyphens and word merging
  -I --integrate        Put together words that have been separated by comment selection
  -c --no-condense      Disable removal of words that are blank and have no annotation
  -p --no-pause         Disable pause at end of execution

"""
__version__ = "1.0.2"

from docopt import docopt  # type: ignore

from docx import Document  # type: ignore
from docx.opc.exceptions import OpcError  # type: ignore

# from importer import import_lines, parse_comments
from importer import import_chapter
from processor import dehyphenate, condense, integrate_words
from exporter import export_sheet

if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)
    # print(args)
    fname = args["<docx>"]
    print(f"Прочитане: {fname}")

    if len(fname) < 6 or "." not in fname[2:]:
        fname += ".docx"
    elif not fname.lower().endswith(".docx"):
        print("Файлът трябва да е във формат .docx. Моля конвертирайте го")
        exit()

    try:
        doc = Document(fname)
    except OpcError:
        print(
            "Файлът трябва да е във формат .docx. Посоченият файл изглежда развален. Моля регенерирайте го"
        )
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

    if not args["--no-dehyphenate"]:
        print("Премахване на пренос...")
        lines = dehyphenate(lines)
        # export_sheet(lines, fname[:-5] + ".d.xlsx")
        print(f"{len(lines)} думи")
    else:
        print("Оставяне на пренос.")

    if args["--integrate"]:
        print("Възстановяване на думи, разделени от коментари...")
        # print(lines)
        lines = integrate_words(lines)
        # export_sheet(lines, fname[:-5] + ".i.xlsx")
        # print(lines)
        print(f"{len(lines)} думи")
    else:
        print("Оставяне на думи, разделени от коментари.")

    # export_sheet(lines, fname + ".2.xlsx")

    if not args["--no-condense"]:
        print("Премахване на празни думи...")
        lines = condense(lines)
        # export_sheet(lines, fname[:-5] + ".c.xlsx")
        print(f"{len(lines)} думи")
    else:
        print("Оставяне на празни думи.")

    print("Експорт...")
    export_fname = fname[:-5] + ".xlsx"
    export_sheet(lines, export_fname)
    print(f"Записване: {export_fname}")

    if not args["--no-pause"]:
        input("Натиснете Enter, за да приключите изпълнението.")
