#!/usr/bin/env python3
"""Index generator for Uchenie evangelsko

Usage:
  indexer <docx_file>

"""

from importer import import_lines
from processor import clean_hyphens, split_rows
from exporter import export_sheet

from docopt import docopt

if __name__ == "__main__":
    args = docopt(__doc__)
    fname = args["<docx_file>"]
    # fname = "../text/00-Prolog-tab.docx"
    # # fname = "../text/01-slovo1-tab.docx"
    book_index = import_lines(fname)
    book_lines = split_rows(clean_hyphens(book_index))
    export_sheet(book_lines, fname + ".xlsx")
