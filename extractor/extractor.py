#!/usr/bin/env python3
"""Vocabulary extractor for Uchitelno Evangelie.
Licensed under MIT License, detailed here: https://mit-license.org/

Usage:
  extractor.py [-d|--no-dehyphenate] [-I|--integrate] [-c|--no-condense] [-v|--verbose|-s|--silent] <docx>

Options:
  -h --help                This information
  --version             Print version
  -d --no-dehyphenate   Disable removal of hyphens and word merging
  -I --integrate        Put together words that have been separated by comment selection
  -c --no-condense      Disable removal of words that are blank and have no annotation
  -s --silent           Remove output other than warnings and errors, also does not pause after completion
  -v --verbose          Increase debug level

"""
__version__ = "1.1.1"  # used also by build.sh script

from docopt import docopt  # type: ignore

from docx import Document  # type: ignore
from docx.opc.exceptions import OpcError  # type: ignore

# from importer import import_lines, parse_comments
from importer import import_chapter
from processor import dehyphenate, condense, integrate_words
from exporter import export_sheet

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
    log.info(f"Extractor v{__version__}")
    log.debug(args)
    fname = args["<docx>"]
    log.info(f"Прочитане: {fname}")

    if len(fname) < 6 or "." not in fname[2:]:
        fname += ".docx"
    elif not fname.lower().endswith(".docx"):
        log.critical("Файлът трябва да е във формат .docx. Моля конвертирайте го")
        exit()

    try:
        doc = Document(fname)
    except OpcError as oe:
        log.critical(
            "Файлът трябва да е във формат .docx. Посоченият файл изглежда развален. Моля регенерирайте го"
        )
        log.critical(oe)
        exit()

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

    log.info("Импорт...")
    lines = import_chapter(fname)
    log.info(f"{len(lines)} думи")

    log.debug(lines)
    # export_sheet(lines, fname + ".1.xlsx")

    if not args["--no-dehyphenate"]:
        log.info("Премахване на пренос...")
        lines = dehyphenate(lines)
        # export_sheet(lines, fname[:-5] + ".d.xlsx")
        log.info(f"{len(lines)} думи")
    else:
        log.info("Оставяне на пренос.")

    if args["--integrate"]:
        log.info("Възстановяване на думи, разделени от коментари...")
        log.debug(lines)
        lines = integrate_words(lines)
        # export_sheet(lines, fname[:-5] + ".i.xlsx")
        log.debug(lines)
        log.info(f"{len(lines)} думи")
    else:
        log.info("Оставяне на думи, разделени от коментари.")

    # export_sheet(lines, fname + ".2.xlsx")

    if not args["--no-condense"]:
        log.info("Премахване на празни думи...")
        lines = condense(lines)
        # export_sheet(lines, fname[:-5] + ".c.xlsx")
        log.info(f"{len(lines)} думи")
    else:
        log.info("Оставяне на празни думи.")

    log.info("Експорт...")
    export_fname = fname[:-5] + ".xlsx"
    export_sheet(lines, export_fname)
    log.info(f"Записване: {export_fname}")

    if logger.level < log.WARNING:
        input("Натиснете Enter, за да приключите изпълнението.")
