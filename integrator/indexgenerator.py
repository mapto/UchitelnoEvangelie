#!/usr/bin/env python3
"""Index generator for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  indexgenerator.py [-v|--verbose|-s|--silent] <xlsx>...

Options:
  -h --help             This information
  -s --silent           Remove output other than warnings and errors, also does not pause after completion
  -v --verbose          Increase debug level
  --version             Print version

"""
__version__ = "0.3.5"  # used also by build.sh script

import sys
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
from util import ord_word
from merger import merge
from aggregator import aggregate
from generator import generate_docx

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
    log.info(f"IndexGenerator v{__version__}")
    log.debug(
        f"Detected binary path: {path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)}"
    )  # used in config.py
    log.debug(f"CLI arguments: {args}")
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

    log.info("Генериране славянски...")
    export_fname = f"{fname_prefix}index-sla.docx"
    generate_docx(sla, FROM_LANG, export_fname)
    log.info(f"Записване: {export_fname}")

    log.info("Генериране гръцки...")
    export_fname = f"{fname_prefix}index-gre.docx"
    generate_docx(gre, TO_LANG, export_fname)
    log.info(f"Записване: {export_fname}")

    for d in to_clean:
        shutil.rmtree(d)

    if logger.level < log.WARNING:
        input("Натиснете Enter, за да приключите изпълнението.")
