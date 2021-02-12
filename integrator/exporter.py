from typing import Tuple, List

from sortedcontainers import SortedDict, SortedList  # type: ignore

from docx import Document  # type: ignore
from docx.shared import RGBColor, Pt  # type: ignore

from model import Index

html = """
<html>
<head>
</head>
<body>
%s
</body>
</html>
"""

fonts = {"gr": "Times New Roman", "sl": "CyrillicaOchrid10U"}
colors = {"gr": RGBColor(0x55, 0x00, 0x00), "sl": RGBColor(0x00, 0x00, 0x55)}


def docx_usage(par, key: Tuple[str, str], usage: List[Index], src_style: str) -> None:
    """
    key: (word,translation)
    usage: list of indices of usages also containing their styles
    """
    other_style = "gr" if src_style == "sl" else "sl"

    run = par.add_run()
    run.font.name = fonts[src_style]
    run.font.color.rgb = colors[src_style]
    run.add_text(key[0])

    run = par.add_run()
    run.add_text("/")

    run = par.add_run()
    run.font.name = fonts[other_style]
    run.font.color.rgb = colors[other_style]
    run.add_text(f"{key[1]} (")

    first = True
    for next in usage:
        if not first:
            run = par.add_run()
            run.add_text(", ")
        run = par.add_run()
        run.font.bold = next.bold
        run.font.italic = next.italic
        run.add_text(str(next))
        first = False
    run = par.add_run()
    run.add_text(")")


def _export_line(level: int, lang: str, d: SortedDict, doc: Document):
    """Builds the hierarchical entries of the dictionary. Recursion ensures that this works with variable depth.

    Args:
        level (int): 0-indexed depth, runs along with dict depth
        lang (str): original language
        d (SortedDict): level of dictionary to be exported
        doc (Document): export document
    """
    for li, next_d in d.items():
        if li:
            par = doc.add_paragraph()
            if level > 0:
                par.paragraph_format.first_line_indent = Pt(10)
            run = par.add_run()
            run.font.name = fonts[lang]
            run.font.size = Pt(18 if level == 0 else 14)
            prefix = "| " * level
            run.add_text(f"{prefix} {li}")
        any_child = next(iter(next_d.values()))
        any_of_any = next(iter(any_child.values()))
        if type(any_of_any) is SortedList:
            trans_lang = "gr" if lang == "sl" else "sl"
            for t, bottom_d in next_d.items():
                par = doc.add_paragraph()
                par.paragraph_format.left_indent = Pt(30)
                par.paragraph_format.first_line_indent = Pt(-10)
                run = par.add_run()
                run.font.name = fonts[trans_lang]
                run.add_text(t + ": ")
                first = True
                for key, usage in bottom_d.items():
                    if not first:
                        par.add_run().add_text("; ")
                    docx_usage(par, key, usage, lang)
                    first = False

        else:
            _export_line(level + 1, lang, next_d, doc)


def export_docx(d: SortedDict, lang: str, fname: str) -> None:
    doc = Document()
    _export_line(0, lang, d, doc)
    doc.save(fname)
