#!/usr/bin/env python3
"""Index integrator for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  integrator.py [-p] <xlsx>...
  integrator.py [--no-pause] <xlsx>...

Options:
  -h --help                This information
  -v --version             Print version
  -p --no-pause            Disable pause at end of execution

"""
__version__ = "1.2.1"  # used also by build.sh script

from docopt import docopt  # type: ignore
from sortedcontainers import SortedDict  # type: ignore

from config import FROM_LANG, TO_LANG
from semantics import TableSemantics
from setup import sl_sem, gr_sem
from importer import import_mapping
from util import ord_word, extract_letters
from merger import merge
from aggregator import aggregate
from exporter import export_docx

INCL_HILITED = True

if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)
    print(f"Integrator v{__version__}")
    # print(args)
    fnames = args["<xlsx>"]

    assert sl_sem.var  # for mypy
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

        for p in pairs:
            print(f"Събиране на многоредови преводи {p.label}...")
            merged = merge(lines, p.orig, p.trans, INCL_HILITED)
            print(f"{len(merged)} думи")

            print(f"Кондензиране {p.label}...")
            before = len(p.result)
            p.result = aggregate(merged, p.orig, p.trans, p.result)
            after = len(p.result)
            print(f"{after-before} леми")

    fname_prefix = ""
    if len(fnames) == 1:
        if fnames[0].lower().endswith(".xlsx"):
            fname_prefix = fnames[0][:-5] + "-"
        else:
            fname_prefix = fnames[0] + "-"

    print("Експорт слявянски...")
    export_fname = f"{fname_prefix}list-sla.docx"
    export_docx(sla, FROM_LANG, export_fname)
    print(f"Записване: {export_fname}")

    print("Експорт гръцки...")
    export_fname = f"{fname_prefix}list-gre.docx"
    export_docx(gre, TO_LANG, export_fname)
    print(f"Записване: {export_fname}")

    if not args["--no-pause"]:
        input("Натиснете Enter, за да приключите изпълнението.")
