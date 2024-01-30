#!/usr/bin/env python3
"""List integrator for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  integrator.py [-v|--verbose|-s|--silent] <xlsx>...

Options:
  -h --help             This information
  -s --silent           Remove output other than warnings and errors, also does not pause after completion
  -v --verbose          Increase debug level
  --version             Print version

"""
__version__ = "1.3.12"  # used also by build.sh script

from cli import expand_names, init, wrapup


fnames = init("integrator", __doc__, __version__) if __name__ == "__main__" else []

import logging as log

logger = log.getLogger()

from sortedcontainers import SortedDict  # type: ignore

from config import FROM_LANG, TO_LANG
from semantics import TableSemantics
from setup import sl_sem, gr_sem
from importer import import_mapping
from util import ord_word, extract_letters
from merger import merge
from aggregator import aggregate
from exporter import export_docx

if __name__ == "__main__":
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

    expanded_fnames, to_clean = expand_names(fnames)

    for fname in expanded_fnames:
        log.info(f"Прочитане: {fname}")
        log.info("Импорт...")
        lines = import_mapping(fname, sem)
        log.info(f"{len(lines)} думи")

        # print("Раздуване на индекси...")
        # lines = expand_idx(lines)
        # print(f"{len(lines)} реда")

        log.info(f"Обзор на буквите в славянски...")
        letters = {}
        for c in sl_sem.lem1_cols():
            letters.update(extract_letters(lines, c))
        log.info(f"{len(letters)} символа: {letters}")

        log.info(f"Обзор на буквите в гръцки...")
        letters = {}
        for c in gr_sem.lem1_cols():
            letters.update(extract_letters(lines, c))
        log.info(f"{len(letters)} символа: {letters}")

        for p in pairs:
            log.info(f"Събиране на многоредови преводи {p.label}...")
            merged = merge(lines, p.orig, p.trans)
            log.info(f"{len(merged)} думи")

            log.info(f"Кондензиране {p.label}...")
            before = len(p.result)
            p.result = aggregate(merged, p.orig, p.trans, p.result)
            after = len(p.result)
            log.info(f"{after-before} леми")

    # TODO: Directories do not work well
    fname_prefix = ""
    if len(fnames) == 1:
        if fnames[0].lower().endswith(".xlsx"):
            fname_prefix = fnames[0][:-5] + "-"
        else:
            fname_prefix = fnames[0] + "-"

    log.info("Експорт славянски...")
    export_fname = f"{fname_prefix}list-sla.docx"
    export_docx(sla, FROM_LANG, export_fname)
    log.info(f"Записване: {export_fname}")

    log.info("Експорт гръцки...")
    export_fname = f"{fname_prefix}list-gre.docx"
    export_docx(gre, TO_LANG, export_fname)
    log.info(f"Записване: {export_fname}")

    wrapup(to_clean)
