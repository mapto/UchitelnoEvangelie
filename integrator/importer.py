#!/usr/bin/env python3

from typing import List, Dict, Optional

from openpyxl import Workbook  # type: ignore
from openpyxl import load_workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore

from const import IDX_COL, STYLE_COL

from semantics import TableSemantics, MainLangSemantics, VarLangSemantics


def _style2str(s: Font, bgs: Dict[str, Optional[str]]) -> str:
    """take font style from index and presence of background in selected named columns"""
    result = [k for k, v in bgs.items() if v]
    if s and s.bold:
        result.append("bold")
    if s and s.italic:
        result.append("italic")
    return "|".join(result)


def import_mapping(fname: str, sem: TableSemantics) -> List[List[str]]:
    wb = load_workbook(fname, read_only=True, data_only=True)
    ws = wb.active

    result = []
    for row in ws.iter_rows(max_col=STYLE_COL):
        line = [cell.value for cell in row]
        if not "".join([v for v in line if v]).strip():
            continue
        bgs = {f"hl{v:02d}": row[v].fill.patternType for v in sem.cols() if row[v].fill}
        line.append(_style2str(row[IDX_COL].font, bgs))
        result.append(line)

    return result


if __name__ == "__main__":
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )
    sem = TableSemantics(sl_sem, gr_sem)

    result = import_mapping("01-slovo1-lemat.xlsx", sem)

    print(result)
    print(len(result))
