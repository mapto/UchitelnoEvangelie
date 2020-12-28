#!/usr/bin/env python3

from typing import List, Tuple

from openpyxl import Workbook  # type: ignore
from openpyxl.cell import WriteOnlyCell  # type: ignore
from openpyxl.styles import Font  # type: ignore

from model import Word


def export_sheet(data: List[Word], fname: str) -> None:
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    for next in data:
        row = [next.variant, "", "", next.index(), next.word, next.line_context]
        line = []
        for v in row:
            cell = WriteOnlyCell(ws, value=v)
            cell.font = Font("CyrillicaOchrid10U")
            line.append(cell)
        ws.append(line)

    # col = ws.column_dimensions["B"]
    # col.font = font

    # Save the file
    wb.save(fname)


"""
def read(fname: str = "4slovo-Bg-LT.docx"):
    doc = handler.DocxHandler(fname)
    doc.clean_hyphens()

    export_sheet([[l, w, r] for l, w, r in doc.extract_words()], fname + ".xlsx")
"""

if __name__ == "__main__":
    # read()
    pass
