"""Shared utilities for the word processor export"""

from typing import Optional, Union
import logging as log
from sortedcontainers import SortedDict, SortedSet  # type: ignore

from docx.shared import RGBColor, Pt, Cm  # type: ignore

from config import FROM_LANG, TO_LANG

GENERIC_FONT = "Times New Roman"

fonts = {TO_LANG: GENERIC_FONT, FROM_LANG: "CyrillicaOchrid10U"}
colors = {TO_LANG: RGBColor(0x55, 0x00, 0x00), FROM_LANG: RGBColor(0x00, 0x00, 0x55)}


def _generate_text(
    par,
    text: str,
    font: str = "",
    color: str = "",
    size: Optional[Pt] = None,
    bold: bool = False,
    italic: bool = False,
    indent: Optional[Cm] = None,
    superscript: bool = False,
    subscript: bool = False,
):
    run = par.add_run()
    if font:
        run.font.name = font
    if color:
        run.font.color.rgb = color
    if size:
        run.font.size = size
    if bold:
        run.font.bold = bold
    if italic:
        run.font.italic = italic
    if indent:
        par.paragraph_format.first_line_indent = indent
    if superscript:
        run.font.superscript = True
    if subscript:
        run.font.subscript = True
    run.add_text(text)


def any_grandchild(d: SortedDict) -> Union[SortedDict, SortedSet]:
    """Returns the first grandchild. Also handles the case if some child collections are empty"""
    for child in d.values():
        for grandchild in child.values():
            return grandchild
    log.error(d)
    raise AssertionError("Collections tree should not be empty")
