"""The exporter specific to the integrator"""

from const import INDENT_CH, SPECIAL_CHARS
from typing import Dict, Tuple

from sortedcontainers import SortedDict, SortedSet  # type: ignore

from docx import Document  # type: ignore
from docx.shared import Pt  # type: ignore

from config import FROM_LANG, TO_LANG
from const import CF_SEP
from const import BRACE_OPEN, BRACE_CLOSE

from util import main_source, subscript
from model import Alternative, Usage, Source

from wordproc import _generate_text, any_grandchild
from wordproc import GENERIC_FONT, other_lang, fonts, colors


def _generate_usage_alt_vars(
    par, u: Usage, lang: str, alt_var: Dict[Source, Tuple[str, int]]
) -> None:
    # Word is stored in Index only for orig.
    # Thus the check u.lang == lang
    if u.lang == lang and not any(v[0] not in u.idx.word for v in alt_var.values()):
        return

    first = True
    _generate_text(par, f" {BRACE_OPEN[lang]}")
    for word, cnt in alt_var.values():
        if u.lang == lang and word in u.idx.word:
            continue
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

    sl_cnt = u.idx.ocnt if u.lang == FROM_LANG else u.idx.tcnt
    gr_cnt = u.idx.tcnt if u.lang == FROM_LANG else u.idx.ocnt

    other_before_own = False
    if u.var and u.var.has_lang(FROM_LANG):
        if not u.var.has_lang(TO_LANG):
            if gr_cnt > 1:
                _generate_text(par, subscript(gr_cnt, TO_LANG), subscript=True)
            other_before_own = True
        _generate_text(par, str(u.var.by_lang(FROM_LANG)), superscript=True)
    if sl_cnt > 1:
        _generate_text(par, subscript(sl_cnt, FROM_LANG), subscript=True)
    elif u.var and u.var.has_lang(FROM_LANG) and u.var.has_lang(TO_LANG):
        _generate_text(par, "-", superscript=True)
    if not other_before_own:
        if u.var and u.var.has_lang(TO_LANG):
            _generate_text(par, str(u.var.by_lang(TO_LANG)), superscript=True)
        if gr_cnt > 1:
            _generate_text(par, subscript(gr_cnt, TO_LANG), subscript=True)


def _is_orig_alt(u: Usage) -> bool:
    """
    >>> from model import Index
    >>> i = Index.unpack("5/28d18", word="шьств\ue205ꙗ пꙋт\ue205 H шьст\ue205ꙗ пꙋт\ue205 G", lemma="пѫть")

    >>> vl0 = {Source("H"): "шьств\ue205\ue201 пѫт\ue205", Source("G"): "other"}
    >>> vw0 = {Source("G"): ("other", 1), Source("H"): ("шьств\ue205ꙗ пꙋт\ue205 H", 1)}
    >>> oa0 = Alternative(var_lemmas=vl0, var_words=vw0)
    >>> u0 = Usage(i, "sl", Source("GH"), oa0)
    >>> _is_orig_alt(u0)
    True

    >>> vl = {Source("H"): "шьств\ue205\ue201 пѫт\ue205", Source("G"): "шьст\ue205\ue201 пѫт\ue205"}
    >>> vw = {Source("G"): ("шьст\ue205ꙗ пꙋт\ue205 G", 1), Source("H"): ("шьств\ue205ꙗ пꙋт\ue205 H", 1)}
    >>> oa1 = Alternative("пѫтошьств\ue205\ue201", vl, "поутошьств\ue205ꙗ", vw)
    >>> u1 = Usage(i, "sl", Source("GH"), oa1)
    >>> _is_orig_alt(u1)
    True

    >>> oa2 = Alternative(var_lemmas=vl, var_words=vw)
    >>> u2 = Usage(i, "sl", Source("GH"), oa2)
    >>> _is_orig_alt(u2)
    False
    """
    alt = u.orig_alt
    word = u.idx.word
    return bool(alt) and (
        alt.main_word
        and alt.main_word not in word
        or bool(u.orig_alt.var_words)
        and any(v[0] not in word for v in alt.var_words.values())
    )


def _generate_usage(par, u: Usage) -> None:
    _generate_index(par, u)
    if not _is_orig_alt(u) and not u.trans_alt:
        # if not u.orig_alt and not u.trans_alt:
        return

    _generate_text(par, f" {CF_SEP}")
    if u.orig_alt.main_word and u.orig_alt.main_word not in u.idx.word:
        _generate_text(par, " ")
        _generate_text(par, u.orig_alt.main_word, fonts[u.lang])
        _generate_text(par, f" {main_source(u.lang, u.idx.alt)}")
        if u.orig_alt.main_cnt > 1:
            _generate_text(par, subscript(u.orig_alt.main_cnt, u.lang), subscript=True)

    if u.orig_alt.var_words:
        _generate_usage_alt_vars(par, u, u.lang, u.orig_alt.var_words)

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
        _generate_usage_alt_vars(par, u, other_lang[u.lang], u.trans_alt.var_words)


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
    trans_lang = TO_LANG if lang == FROM_LANG else FROM_LANG
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
            try:
                docx_usage(par, key, usage, lang)
            except Exception as e:
                print(
                    f"ГРЕШКА: При експортиране възникна проблем в ред {usage.idx} ({key}) или групата му"
                )
                print(e)
                break
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

            prefix = "" if li[0] in SPECIAL_CHARS else f"{INDENT_CH} " * level
            _generate_text(
                par, f"{prefix} {li}", fonts[lang], size=Pt(14 if level == 0 else 12)
            )

        try:
            any_of_any = any_grandchild(next_d)
        except AssertionError as ae:
            print(
                f"ГРЕШКА: При експортиране възникна проблем с една от {len(next_d)} употреби на {li}"
            )
            raise ae
        if type(any_of_any) is SortedSet:  # bottom of structure
            _generate_usage_line(lang, next_d, doc)
        else:
            try:
                _export_line(level + 1, lang, next_d, doc)
            except AssertionError as ae:
                print(
                    f"ГРЕШКА: При експортиране възникна проблем с една от {len(next_d)} употреби на {li}"
                )


def export_docx(d: SortedDict, lang: str, fname: str) -> None:
    doc = Document()
    doc.styles["Normal"].font.name = GENERIC_FONT
    _export_line(0, lang, d, doc)

    doc.save(fname)
