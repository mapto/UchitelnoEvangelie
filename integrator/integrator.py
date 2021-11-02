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
__version__ = "1.0.3"

from docopt import docopt  # type: ignore
from sortedcontainers import SortedDict  # type: ignore

from semantics import TableSemantics, MainLangSemantics, VarLangSemantics
from importer import import_mapping
from util import ord_word, extract_letters
from merger import merge
from aggregator import aggregate
from exporter import export_docx


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

    # print("Раздуване на индекси...")
    # lines = expand_idx(lines)
    # print(f"{len(lines)} реда")

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
