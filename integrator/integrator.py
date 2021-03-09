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
from processor import merge, aggregate, extract_letters, expand_idx, join
from exporter import export_docx

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

    sl_sem = LangSemantics("sl", 4, [6, 7, 8, 9], LangSemantics("sl_var", 0, [1, 2]))
    assert sl_sem.var  # for mypy
    gr_sem = LangSemantics(
        "gr", 10, [11, 12, 13], LangSemantics("gr_var", 15, [16, 17])
    )
    assert gr_sem.var  # for mypy
    sem = TableSemantics(sl_sem, gr_sem)

    print("Импорт...")
    lines = import_mapping(fname, sem)
    print(f"{len(lines)} думи")

    # print("Раздуване на индекси...")
    # lines = expand_idx(lines)
    # print(f"{len(lines)} реда")

    print("Събиране на многоредови преводи от славянски...")
    lines_sl = merge(lines, sl_sem, gr_sem)
    print(f"{len(lines_sl)} думи")

    print("Събиране на многоредови преводи от славянски варианти...")
    lines_sl_var = merge(lines, sl_sem.var, gr_sem)
    print(f"{len(lines_sl_var)} думи")

    print("Събиране на многоредови преводи от гръцки...")
    lines_gr = merge(lines, gr_sem, sl_sem)
    print(f"{len(lines_gr)} думи")

    print("Събиране на многоредови преводи от гръцки варианти...")
    lines_gr_var = merge(lines, gr_sem.var, sl_sem)
    print(f"{len(lines_gr_var)} думи")

    for c in sem.lem1_cols():
        print(f"Обзор на буквите в колона {chr(ord('A') + c)}...")
        letters = extract_letters(lines, c)
        print(f"{len(letters)} символа")

    print("Кондензиране славянски...")
    sla = aggregate(lines_sl, sl_sem, gr_sem)
    print(f"{len(sla)} леми")

    print("Кондензиране славянски варианти...")
    sla_var = aggregate(lines_sl_var, sl_sem.var, gr_sem)
    print(f"{len(sla_var)} леми")

    print("Включване на славянски варианти в обща структура...")
    sla = join(sla, sla_var)
    print(f"{len(sla)} леми")

    print("Кондензиране гръцки...")
    gre = aggregate(lines_gr, gr_sem, sl_sem)
    print(f"{len(gre)} леми")

    print("Кондензиране гръцки варианти...")
    gre_var = aggregate(lines_gr_var, gr_sem.var, sl_sem)
    print(f"{len(gre_var)} леми")

    print("Включване на гръцки варианти в обща структура...")
    gre = join(gre, gre_var)
    print(f"{len(gre)} леми")

    print("Експорт слявянски...")
    export_fname = fname[:-5] + "-sla.docx"
    export_docx(sla, "sl", export_fname)
    print(f"Записване: {export_fname}")

    print("Експорт гръцки...")
    export_fname = fname[:-5] + "-gre.docx"
    export_docx(gre, "gr", export_fname)
    print(f"Записване: {export_fname}")

    # if not args["--no-pause"]:
    input("Натиснете Enter, за да приключите изпълнението.")
