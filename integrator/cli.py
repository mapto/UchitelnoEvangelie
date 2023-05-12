from typing import List, Tuple

import os
import sys
from glob import glob
import shutil
import tempfile
import logging
from docopt import docopt  # type: ignore

logger = logging.getLogger()


def init(name: str, doc: str, version: str) -> List[str]:
    args = docopt(doc, version=version)

    logfile = f"{name}-log.txt"
    logger.setLevel(logging.DEBUG)

    logformat = "%(asctime)s:%(name)s:%(levelname)s: %(message)s"
    logFormatter = logging.Formatter(logformat)
    fileHandler = logging.FileHandler(logfile, mode="w", encoding='utf-8')
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.set_name("file")  # type: ignore
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    if "--verbose" in args and args["--verbose"]:
        consoleHandler.setLevel(logging.DEBUG)
    elif "--silent" in args and args["--silent"]:
        consoleHandler.setLevel(logging.WARNING)
    else:
        consoleHandler.setLevel(logging.INFO)
    consoleHandler.set_name("console")  # type: ignore
    logger.addHandler(consoleHandler)

    logging.info(f"{name} v{version}")
    logging.debug(f"CLI arguments: {args}")
    return args["<xlsx>"]


def expand_names(fnames) -> Tuple[List[str], List[str]]:
    expanded_fnames = []
    to_clean = []
    for fname in fnames:
        logging.info(f"Преглеждане: {fname}")

        if os.path.isdir(fname):
            expanded_fnames += glob(os.path.join(fname, "*.xlsx"))
        elif len(fname) < 6 or "." not in fname[2:]:
            expanded_fnames += [fname + ".xlsx"]
        elif not fname.lower().endswith(".xlsx"):
            dest_dir = os.path.join(tempfile.gettempdir(), fname)
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            try:
                shutil.unpack_archive(fname, dest_dir)
                to_clean += [dest_dir]
            except ValueError as ve:
                logging.critical(
                    f"Файлът {fname} трябва да е във формат .xlsx. Като алтернатива, може да е директория или архив. Моля конвертирайте го"
                )
                exit()
            expanded_fnames += glob(os.path.join(dest_dir, "*.xlsx"))
        else:
            expanded_fnames += [fname]
    expanded_fnames.sort()
    return expanded_fnames, to_clean


def wrapup(to_clean: List[str]):
    for d in to_clean:
        shutil.rmtree(d)

    consoleHandler = next(h for h in logger.handlers if h.name == "console")
    if consoleHandler.level < logging.WARNING:
        input("Натиснете Enter, за да приключите изпълнението.")
