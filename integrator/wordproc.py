"""Shared utilities for the word processor export"""

from typing import Optional

from docx.shared import Pt, Cm  # type: ignore


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
    run.add_text(text)
