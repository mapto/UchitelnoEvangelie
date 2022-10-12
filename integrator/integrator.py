#!/usr/bin/env python3
"""Index integrator for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  integrator.py [-v|--verbose|-s|--silent] <xlsx>...

Options:
  -h --help             This information
  -s --silent           Remove output other than warnings and errors, also does not pause after completion
  -v --verbose          Increase debug level
  --version             Print version

"""
__version__ = "1.3.1"  # used also by build.sh script

from os import path
from glob import glob
import shutil
import tempfile

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

import logging as log

logger = log.getLogger()

if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)
    if "--verbose" in args and args["--verbose"]:
        log.basicConfig(level=log.DEBUG)
    elif "--silent" in args and args["--silent"]:
        log.basicConfig(level=log.WARNING)
    else:
        log.basicConfig(level=log.INFO)
    log.info(f"Integrator v{__version__}")
    log.debug(args)
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

    expanded_fnames = []
    to_clean = []
    for fname in fnames:
        log.info(f"Преглеждане: {fname}")

        if path.isdir(fname):
            expanded_fnames += glob(path.join(fname, "*.xlsx"))
        elif len(fname) < 6 or "." not in fname[2:]:
            expanded_fnames += [fname + ".xlsx"]
        elif not fname.lower().endswith(".xlsx"):
            dest_dir = path.join(tempfile.gettempdir(), fname)
            if path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            try:
                shutil.unpack_archive(fname, dest_dir)
                to_clean += [dest_dir]
            except ValueError as ve:
                log.critical(
                    f"Файлът {fname} трябва да е във формат .xlsx. Като алтернатива, може да е директория или архив. Моля конвертирайте го"
                )
                exit()
            expanded_fnames += glob(path.join(dest_dir, "*.xlsx"))
        else:
            expanded_fnames += [fname]
    expanded_fnames.sort()

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

    for d in to_clean:
        shutil.rmtree(d)

    if logger.level < log.WARNING:
        input("Натиснете Enter, за да приключите изпълнението.")
