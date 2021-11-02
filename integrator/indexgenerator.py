#!/usr/bin/env python3
"""Index generator for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  indexgenerator.py [-p] <xlsx>
  indexgenerator.py [--no-pause] <xlsx>

Options:
  -h --help                This information
  -v --version             Print version
  -p --no-pause            Disable pause at end of execution

"""
__version__ = "0.0.4"

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
    fname = args["<xlsx>"]
    print(f"Прочитане: {fname}")

    if len(fname) < 6 or "." not in fname[2:]:
        fname += ".xlsx"
    elif not fname.lower().endswith(".xlsx"):
        print("Файлът трябва да е във формат .xlsx. Моля конвертирайте го")
        exit()

    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    assert sl_sem.var  # for mypy
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )
    assert gr_sem.var  # for mypy
    sem = TableSemantics(sl_sem, gr_sem)

    print("Импорт...")
    lines = import_mapping(fname, sem)
    print(f"{len(lines)} думи")

    sla = SortedDict(ord_word)
    gre = SortedDict(ord_word)
    pairs = [
        {
            "orig": sl_sem,
            "trans": gr_sem,
            "label": "от славянски основен към гръцки",
            "agg": sla,
        },
        {
            "orig": sl_sem.var,
            "trans": gr_sem,
            "label": "от славянски вариант към гръцки",
            "agg": sla,
        },
        {
            "orig": gr_sem.var,
            "trans": sl_sem,
            "label": "от гръцки вариант към славянски",
            "agg": gre,
        },
        {
            "orig": gr_sem,
            "trans": sl_sem,
            "label": "от гръцки основен към славянски",
            "agg": gre,
        },
    ]

    for p in pairs:
        print(f"Събиране на многоредови преводи {p['label']}...")
        merged = merge(lines, p["orig"], p["trans"])
        print(f"{len(merged)} думи")

        print(f"Кондензиране {p['label']}...")
        before = len(p["agg"])
        p["agg"] = aggregate(merged, p["orig"], p["trans"], p["agg"])
        after = len(p["agg"])
        print(f"{after-before} леми")

    print("Генериране слявянски...")
    export_fname = fname[:-5] + "-result-sla.docx"
    generate_docx(sla, "sl", export_fname)
    print(f"Записване: {export_fname}")

    print("Генериране гръцки...")
    export_fname = fname[:-5] + "-result-gre.docx"
    generate_docx(gre, "gr", export_fname)
    print(f"Записване: {export_fname}")

    if not args["--no-pause"]:
        input("Натиснете Enter, за да приключите изпълнението.")
