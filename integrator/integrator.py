#!/usr/bin/env python3
"""Index integrator for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  integrator.py [-p] <xlsx>
  integrator.py [--no-pause] <xlsx>

Options:
  -h --help                This information
  -v --version             Print version
  -p --no-pause            Disable pause at end of execution

"""
__version__ = "1.0.0"

from docopt import docopt  # type: ignore

from docx import Document  # type: ignore
from docx.opc.exceptions import OpcError  # type: ignore
from sortedcontainers import SortedSet  # type: ignore

from semantics import TableSemantics, MainLangSemantics, VarLangSemantics
from importer import import_mapping
from util import extract_letters
from merger import merge
from aggregator import aggregate
from exporter import export_docx, generate_docx


if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)
    print(f"Integrator v{__version__}")
    # print(args)
    fname = args["<xlsx>"]
    print(f"Прочитане: {fname}")

    if len(fname) < 6 or "." not in fname[2:]:
        fname += ".xlsx"
    elif not fname.lower().endswith(".xlsx"):
        print("Файлът трябва да е във формат .xlsx. Моля конвертирайте го")
        exit()

    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    assert sl_sem.var  # for mypy
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
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

    print("Събиране на многоредови преводи от гръцки...")
    lines_gr = merge(lines, gr_sem, sl_sem)
    print(f"{len(lines_gr)} думи")

    print(f"Обзор на буквите в славянски...")
    letters = {}
    for c in sl_sem.lem1_cols():
        letters.update(extract_letters(lines, c))
    print(f"{len(letters)} символа: {letters}")

    print(f"Обзор на буквите в гръцки...")
    letters = {}
    for c in gr_sem.lem1_cols():
        letters.update(extract_letters(lines, c))
    print(f"{len(letters)} символа: {letters}")

    print("Кондензиране славянски...")
    sla = aggregate(lines_sl, sl_sem, gr_sem)
    print(f"{len(sla)} леми")

    print("Кондензиране гръцки...")
    gre = aggregate(lines_gr, gr_sem, sl_sem)
    print(f"{len(gre)} леми")

    print("Експорт слявянски...")
    export_fname = fname[:-5] + "-sla.docx"
    export_docx(sla, "sl", export_fname)
    print(f"Записване: {export_fname}")

    print("Експорт гръцки...")
    export_fname = fname[:-5] + "-gre.docx"
    export_docx(gre, "gr", export_fname)
    print(f"Записване: {export_fname}")

    if not args["--no-pause"]:
        input("Натиснете Enter, за да приключите изпълнението.")
