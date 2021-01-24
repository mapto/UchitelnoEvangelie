#!/usr/bin/env python3
"""Vocabulary extractor for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  extractor.py [-dIcp] <docx>
  extractor.py [--no-dehyphenate] [--integrate] [--no-condense] [--no-pause] <docx>

Options:
  --help                This information
  -d --no-dehyphenate   Disable removal of hyphens and word merging
  -I --integrate        Put together words that have been separated by comment selection
  -c --no-condense      Disable removal of words that are blank and have no annotation
  -p --no-pause         Disable pause at end of execution

"""
__version__ = "0.0.1"

from docopt import docopt  # type: ignore

from docx import Document  # type: ignore
from docx.opc.exceptions import OpcError  # type: ignore

from importer import import_mapping

from processor import aggregate

from exporter import export_html, export_docx

if __name__ == "__main__":
    args = docopt(__doc__)
    # print(args)
    fname = args["<docx>"]
    print(f"Прочитане: {fname}")

    if len(fname) < 6 or "." not in fname[2:]:
        fname += ".xlsx"
    elif not fname.lower().endswith(".xlsx"):
        print("Файлът трябва да е във формат .xlsx. Моля конвертирайте го")
        exit()

    # try:
    #     doc = Document(fname)
    # except OpcError:
    #     print(
    #         "Файлът трябва да е във формат .xlsx. Посоченият файл изглежда развален. Моля регенерирайте го"
    #     )
    #     exit()

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
    lines = import_mapping(fname)
    print(f"{len(lines)} думи")

    print("Кондензиране славянски...")
    sla = aggregate(lines, 4, 10, 6, 11)
    print(f"{len(sla)} леми")

    print("Кондензиране гръцки...")
    gre = aggregate(lines, 10, 4, 11, 6)
    print(f"{len(gre)} леми")

    # print(lines)
    # export_sheet(lines, fname + ".1.xlsx")

    # if not args["--no-dehyphenate"]:
    #     print("Премахване на пренос...")
    #     lines = dehyphenate(lines)
    #     # export_sheet(lines, fname[:-5] + ".d.xlsx")
    #     print(f"{len(lines)} думи")
    # else:
    #     print("Оставяне на пренос.")

    # if args["--integrate"]:
    #     print("Възстановяване на думи, разделени от коментари...")
    #     # print(lines)
    #     lines = integrate_words(lines)
    #     # export_sheet(lines, fname[:-5] + ".i.xlsx")
    #     # print(lines)
    #     print(f"{len(lines)} думи")
    # else:
    #     print("Оставяне на думи, разделени от коментари.")

    # export_sheet(lines, fname + ".2.xlsx")

    # if not args["--no-condense"]:
    #     print("Премахване на празни думи...")
    #     lines = condense(lines)
    #     # export_sheet(lines, fname[:-5] + ".c.xlsx")
    #     print(f"{len(lines)} думи")
    # else:
    #     print("Оставяне на празни думи.")

    print("Експорт слявянски...")
    # export_fname = fname[:-5] + "-sla.html"
    # export_html(sla, "sl", export_fname)
    export_fname = fname[:-5] + "-sla.docx"
    export_docx(sla, "sl", export_fname)
    print(f"Записване: {export_fname}")

    print("Експорт гръцки...")
    export_fname = fname[:-5] + "-gre.docx"
    export_docx(gre, "gr", export_fname)
    print(f"Записване: {export_fname}")

    if not args["--no-pause"]:
        input("Натиснете Enter, за да приключите изпълнението.")
