"""The exporter specific to the integrator"""

from const import VAR_GR, VAR_SL
from typing import Dict, List, Tuple

from sortedcontainers import SortedDict, SortedSet  # type: ignore

from docx import Document  # type: ignore
from docx.shared import Pt  # type: ignore

from const import CF_SEP, main_source
from model import Index, Usage

from wordproc import _generate_text, any_grandchild
from wordproc import GENERIC_FONT, other_lang, fonts, colors, brace_open, brace_close


def docx_usage(par, key: Tuple[str, str], usage: SortedSet, src_style: str) -> None:
    """
    key: (word,translation)
    usage: list of indices of usages also containing their styles
    """
    other_style = other_lang[src_style]

    _generate_text(par, key[0], fonts[src_style], colors[src_style])
    _generate_text(par, "/")
    _generate_text(par, key[1], fonts[other_style], colors[other_style])
    _generate_text(par, " (")

    first = True
    for next in usage:
        if first:
            first = False
        else:
            _generate_text(par, ", ")
        generate_index(par, next.idx)
    _generate_text(par, ")")


def _export_line(level: int, lang: str, d: SortedDict, doc: Document):
    """Builds the hierarchical entries for detailed comparison.
    Recursion ensures that this works with variable depth.

    Args:
        level (int): 0-indexed depth, runs along with dict depth
        lang (str): original language
        d (SortedDict): level of dictionary to be exported
        doc (Document): export document
    """
    for li, next_d in d.items():
        if level == 0 and not li:
            continue
        if li:
            par = doc.add_paragraph()
            par.style.font.name = GENERIC_FONT
            if level > 0:
                par.paragraph_format.first_line_indent = Pt(10)

            prefix = "| " * level
            _generate_text(
                par, f"{prefix} {li}", fonts[lang], size=Pt(18 if level == 0 else 14)
            )

        any_of_any = any_grandchild(next_d)
        if type(any_of_any) is SortedSet:  # bottom of structure
            trans_lang = "gr" if lang == "sl" else "sl"
            for t, bottom_d in next_d.items():
                par = doc.add_paragraph()
                par.style.font.name = GENERIC_FONT
                par.paragraph_format.left_indent = Pt(30)
                par.paragraph_format.first_line_indent = Pt(-10)

                _generate_text(par, t, fonts[trans_lang])

                run = par.add_run()
                run.add_text(": ")
                first = True
                pairs = SortedDict(bottom_d.items())
                for key in pairs:
                    usage = bottom_d[key]
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


def generate_index(par, idx: Index) -> None:
    _generate_text(par, str(idx), bold=idx.bold, italic=idx.italic)
    if idx.var:
        _generate_text(par, "var", superscript=True, bold=idx.bold, italic=idx.italic)
