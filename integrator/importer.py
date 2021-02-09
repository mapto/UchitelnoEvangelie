#!/usr/bin/env python3

from typing import List, Dict, Tuple

from openpyxl import Workbook  # type: ignore
from openpyxl import load_workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore


def style2str(s: Font) -> str:
    if not s:
        return ""
    result = []
    if s.bold:
        result.append("bold")
    if s.italic:
        result.append("italic")
    return "|".join(result)


def import_mapping(fname: str) -> List[List[str]]:
    wb = load_workbook(fname, read_only=True, data_only=True)
    ws = wb.active

    result = []
    for row in ws.iter_rows(max_col=16):
        line = [cell.value for cell in row]
        line.append(style2str(row[3].font))
        result.append(line)

    # return [list(row) for row in ws.iter_rows(max_col=16, values_only=True)]
    return result


if __name__ == "__main__":
    result = import_mapping("01-slovo1-lemat.xlsx")

    print(result)
    print(len(result))
