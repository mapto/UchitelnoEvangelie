"""The exporter specific to the integrator"""

from const import VAR_GR, VAR_SL
from typing import Dict, List, Tuple

from sortedcontainers import SortedDict, SortedSet  # type: ignore

from docx import Document  # type: ignore
from docx.shared import RGBColor, Pt  # type: ignore

from const import CF_SEP, main_source, var_sources
from model import Index, Usage

from wordproc import _generate_text

GENERIC_FONT = "Times New Roman"

other_lang = {"gr": "sl", "sl": "gr"}
fonts = {"gr": GENERIC_FONT, "sl": "CyrillicaOchrid10U"}
colors = {"gr": RGBColor(0x55, 0x00, 0x00), "sl": RGBColor(0x00, 0x00, 0x55)}
brace_open = {"sl": "[", "gr": "{"}
brace_close = {"sl": "]", "gr": "}"}


def docx_usage(par, key: Tuple[str, str], usage: List[Usage], src_style: str) -> None:
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
        _generate_text(par, str(next.idx), bold=next.idx.bold, italic=next.idx.italic)
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

        any_child = next(iter(next_d.values()))
        any_of_any = next(iter(any_child.values()))
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
                pairs = dict(bottom_d.items())
                for key in sorted(pairs, key=pairs.__getitem__):
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
    _generate_text(par, str(idx))
    if idx.var:
        _generate_text(par, "var", superscript=True)


def _generate_usage_alt_vars(par, lang: str, alt_var: Dict[str, str]) -> None:
    first = True
    _generate_text(par, f" {brace_open[lang]}")
    for var, word in alt_var.items():
        if first:
            first = False
        else:
            _generate_text(par, ", ")
        _generate_text(par, word, fonts[lang])
        _generate_text(par, var, superscript=True)
    _generate_text(par, brace_close[lang])


def _generate_usage(par, u: Usage) -> None:
    if (
        not u.orig_alt
        and not u.orig_alt_var
        and not u.trans_alt
        and not u.trans_alt_var
    ):
        return
    _generate_text(par, f" {CF_SEP}")
    if u.orig_alt:
        _generate_text(par, " ")
        _generate_text(par, u.orig_alt, fonts[u.lang])
        _generate_text(par, f" {main_source[u.lang]}")

    if u.orig_alt_var:
        _generate_usage_alt_vars(par, u.lang, u.orig_alt_var)

    # previous addition certainly finished with GENERIC_FONT
    if u.trans_alt:
        _generate_text(par, " ")
        _generate_text(par, u.trans_alt, fonts[other_lang[u.lang]])
        _generate_text(par, f" {main_source[other_lang[u.lang]]}")

    if u.trans_alt_var:
        _generate_usage_alt_vars(par, other_lang[u.lang], u.trans_alt_var)


def docx_result(par, key: Tuple[str, str], usage: List[Usage], src_style: str) -> None:
    """
    key: (word,translation)
    usage: list of indices of usages also containing their styles
    """
    other_style = other_lang[src_style]

    first = True
    for next in usage:
        if not first:
            _generate_text(par, "; ")
        _generate_text(par, str(next.idx), bold=next.idx.bold, italic=next.idx.italic)
        if next.var:
            _generate_text(par, next.var, superscript=True)
        _generate_usage(par, next)
        first = False
