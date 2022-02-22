"""The exporter specific to the integrator"""

from const import SPECIAL_CHARS
from typing import Dict, Tuple

from sortedcontainers import SortedDict, SortedSet  # type: ignore

from docx import Document  # type: ignore
from docx.shared import Pt  # type: ignore

from const import CF_SEP
from const import BRACE_OPEN, BRACE_CLOSE

from util import main_source, subscript
from model import Usage, Source

from wordproc import _generate_text, any_grandchild
from wordproc import GENERIC_FONT, other_lang, fonts, colors


def _generate_usage_alt_vars(
    par, lang: str, alt_var: Dict[Source, Tuple[str, int]]
) -> None:
    first = True
    _generate_text(par, f" {BRACE_OPEN[lang]}")
    for word, cnt in alt_var.values():
        if first:
            first = False
        else:
            _generate_text(par, ", ")
        _generate_text(par, word, fonts[lang])
        subs = subscript(cnt, lang)
        if subs:
            _generate_text(par, subs, subscript=True)
    _generate_text(par, BRACE_CLOSE[lang])


def _generate_index(par, u: Usage) -> None:
    s = str(u.idx)
    if u.idx.ocnt != 1:
        s = s[:-3]
    if u.idx.tcnt != 1:
        s = s[:-3]
    _generate_text(par, s, bold=u.idx.bold, italic=u.idx.italic)

    sl_cnt = u.idx.ocnt if u.lang == "sl" else u.idx.tcnt
    gr_cnt = u.idx.tcnt if u.lang == "sl" else u.idx.ocnt

    other_before_own = False
    if u.var and u.var.has_lang("sl"):
        if not u.var.has_lang("gr"):
            if gr_cnt > 1:
                _generate_text(par, subscript(gr_cnt, "gr"), subscript=True)
            other_before_own = True
        _generate_text(par, str(u.var.by_lang("sl")), superscript=True)
    if sl_cnt > 1:
        _generate_text(par, subscript(sl_cnt, "sl"), subscript=True)
    elif u.var and u.var.has_lang("sl") and u.var.has_lang("gr"):
        _generate_text(par, "-", superscript=True)
    if not other_before_own:
        if u.var and u.var.has_lang("gr"):
            _generate_text(par, str(u.var.by_lang("gr")), superscript=True)
        if gr_cnt > 1:
            _generate_text(par, subscript(gr_cnt, "gr"), subscript=True)


def _generate_usage(par, u: Usage) -> None:
    _generate_index(par, u)
    if not u.orig_alt and not u.trans_alt:
        return

    _generate_text(par, f" {CF_SEP}")
    if u.orig_alt.main_word:
        _generate_text(par, " ")
        _generate_text(par, u.orig_alt.main_word, fonts[u.lang])
        _generate_text(par, f" {main_source(u.lang, u.idx.alt)}")
        if u.orig_alt.main_cnt > 1:
            _generate_text(par, subscript(u.orig_alt.main_cnt, u.lang), subscript=True)

    if u.orig_alt.var_words:
        _generate_usage_alt_vars(par, u.lang, u.orig_alt.var_words)

    # previous addition certainly finished with GENERIC_FONT
    if u.trans_alt.main_word:
        _generate_text(par, " ")
        _generate_text(par, u.trans_alt.main_word, fonts[other_lang[u.lang]])
        _generate_text(par, f" {main_source(other_lang[u.lang], u.idx.alt)}")
        if u.trans_alt.main_cnt > 1:
            _generate_text(
                par, subscript(u.trans_alt.main_cnt, other_lang[u.lang]), subscript=True
            )

    if u.trans_alt.var_words:
        _generate_usage_alt_vars(par, other_lang[u.lang], u.trans_alt.var_words)


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
        _generate_usage(par, next)
    _generate_text(par, ")")


def _generate_usage_line(lang: str, d: SortedDict, doc: Document) -> None:
    """Lists ordered occurences for each word usage pair"""
    trans_lang = "gr" if lang == "sl" else "sl"
    for t, bottom_d in d.items():
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

            prefix = "" if li[0] in SPECIAL_CHARS else "| " * level
            _generate_text(
                par, f"{prefix} {li}", fonts[lang], size=Pt(14 if level == 0 else 12)
            )

        any_of_any = any_grandchild(next_d)
        if type(any_of_any) is SortedSet:  # bottom of structure
            _generate_usage_line(lang, next_d, doc)
        else:
            _export_line(level + 1, lang, next_d, doc)


def export_docx(d: SortedDict, lang: str, fname: str) -> None:
    doc = Document()
    doc.styles["Normal"].font.name = GENERIC_FONT
    _export_line(0, lang, d, doc)
    doc.save(fname)
