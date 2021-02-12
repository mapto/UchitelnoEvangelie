#!/usr/bin/env python3
"""Index integrator for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  integrator.py <xlsx>

"""
__version__ = "0.0.1"

from docopt import docopt  # type: ignore

from docx import Document  # type: ignore
from docx.opc.exceptions import OpcError  # type: ignore

from model import TableSemantics, LangSemantics
from importer import import_mapping
from processor import merge, aggregate, extract_letters, expand_idx
from exporter import export_html, export_docx

if __name__ == "__main__":
    args = docopt(__doc__)
    # print(args)
    fname = args["<xlsx>"]
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

    print("Раздуване на индекси...")
    lines = expand_idx(lines)
    print(f"{len(lines)} реда")

    sl_sem = LangSemantics("sl", 4, [6, 7, 8, 9])
    gr_sem = LangSemantics("gr", 10, [11, 12, 13])

    print("Събиране на многоредови преводи от славянски...")
    lines_sl = merge(lines, sl_sem, gr_sem)
    print(f"{len(lines_sl)} думи")

    print("Събиране на многоредови преводи от гръцки...")
    lines_gr = merge(lines, gr_sem, sl_sem)
    print(f"{len(lines_gr)} думи")

    for c in [sl_sem.lemmas[0], gr_sem.lemmas[0]]:
        print(f"Обзор на буквите в колона {chr(ord('A') + c)}...")
        letters = extract_letters(lines, c)
        print(f"{len(letters)} символа")

    print("Кондензиране славянски...")
    sla = aggregate(lines_sl, sl_sem, gr_sem)
    print(f"{len(sla)} леми")

    print("Кондензиране гръцки...")
    gre = aggregate(lines_gr, gr_sem, sl_sem)
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

    # if not args["--no-pause"]:
    input("Натиснете Enter, за да приключите изпълнението.")
