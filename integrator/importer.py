#!/usr/bin/env python3

from typing import List, Dict, Tuple

from openpyxl import Workbook  # type: ignore
from openpyxl import load_workbook  # type: ignore


def import_mapping(fname: str) -> List[List[str]]:
    wb = load_workbook(fname, read_only=True, data_only=True)
    ws = wb.active

    return [list(row) for row in ws.iter_rows(max_col=16, values_only=True)]


if __name__ == "__main__":
    print(len(import_mapping("01-slovo1-lemat.xlsx")))
