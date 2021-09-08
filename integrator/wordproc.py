"""Shared utilities for the word processor export"""

from typing import Optional, Union

from sortedcontainers import SortedDict, SortedSet  # type: ignore

from docx.shared import RGBColor, Pt, Cm  # type: ignore

GENERIC_FONT = "Times New Roman"

other_lang = {"gr": "sl", "sl": "gr"}
fonts = {"gr": GENERIC_FONT, "sl": "CyrillicaOchrid10U"}
colors = {"gr": RGBColor(0x55, 0x00, 0x00), "sl": RGBColor(0x00, 0x00, 0x55)}
brace_open = {"sl": "[", "gr": "{"}
brace_close = {"sl": "]", "gr": "}"}


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


def any_grandchild(d: SortedDict) -> Union[SortedDict, SortedSet]:
    """Returns the first grandchild. Also handles the case if some child collections are empty"""
    for child in d.values():
        for grandchild in child.values():
            return grandchild
    print(d)
    raise NotImplementedError("Completely empty collections tree not allowed")
