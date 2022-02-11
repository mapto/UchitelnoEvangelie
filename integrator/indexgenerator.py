#!/usr/bin/env python3
"""Index generator for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  indexgenerator.py [-p] <xlsx>...
  indexgenerator.py [--no-pause] <xlsx>...

Options:
  -h --help                This information
  -v --version             Print version
  -p --no-pause            Disable pause at end of execution

"""
__version__ = "0.0.5"

from docopt import docopt  # type: ignore
from sortedcontainers import SortedDict  # type: ignore

from semantics import TableSemantics, MainLangSemantics, VarLangSemantics
from importer import import_mapping
from util import ord_word
from merger import merge
from aggregator import aggregate
from generator import generate_docx


if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)
    print(f"IndexGenerator v{__version__}")
    # print(args)
    fnames = args["<xlsx>"]

    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    assert sl_sem.var  # for mypy
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )
    assert gr_sem.var  # for mypy

    sla = SortedDict(ord_word)
    gre = SortedDict(ord_word)

    pairs = [
        TableSemantics(
            sl_sem, gr_sem, label="от славянски основен към гръцки", result=sla
        ),
        TableSemantics(
            sl_sem.var, gr_sem, label="от славянски вариант към гръцки", result=sla
        ),
        TableSemantics(
            gr_sem, sl_sem, label="от гръцки основен към славянски", result=gre
        ),
        TableSemantics(
            gr_sem.var, sl_sem, label="от гръцки вариант към славянски", result=gre
        ),
    ]
    sem = pairs[0]

    for fname in fnames:
        print(f"Прочитане: {fname}")

        if len(fname) < 6 or "." not in fname[2:]:
            fname += ".xlsx"
        elif not fname.lower().endswith(".xlsx"):
            print("Файлът трябва да е във формат .xlsx. Моля конвертирайте го")
            exit()

        print("Импорт...")
        lines = import_mapping(fname, sem)
        print(f"{len(lines)} думи")

        for p in pairs:
            print(f"Събиране на многоредови преводи {p.label}...")
            merged = merge(lines, p.orig, p.trans)
            print(f"{len(merged)} думи")

            print(f"Кондензиране {p.label}...")
            before = len(p.result)
            p.result = aggregate(merged, p.orig, p.trans, p.result)
            after = len(p.result)
            print(f"{after-before} леми")

    print("Генериране слявянски...")
    export_fname = "index-sla.docx"
    if len(fnames) == 1:
        export_fname = f"{fnames[0][:-5]}-{export_fname}"
    generate_docx(sla, "sl", export_fname)
    print(f"Записване: {export_fname}")

    print("Генериране гръцки...")
    export_fname = "index-gre.docx"
    if len(fnames) == 1:
        export_fname = f"{fnames[0][:-5]}-{export_fname}"
    generate_docx(gre, "gr", export_fname)
    print(f"Записване: {export_fname}")

    if not args["--no-pause"]:
        input("Натиснете Enter, за да приключите изпълнението.")
