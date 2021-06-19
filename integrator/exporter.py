from const import VAR_GR, VAR_SL
from typing import Dict, List, Optional, Tuple, Union

from sortedcontainers import SortedDict, SortedSet  # type: ignore

from docx import Document  # type: ignore
from docx.shared import RGBColor, Pt, Cm  # type: ignore

from const import CF_SEP, main_source, var_sources
from model import Index, Usage, Counter

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


def _get_set_counts(s: SortedSet) -> Counter:
    """
    >>> i = [Index(ch=1, alt=True, page=168, col='c', row=7), Index(ch=1, alt=True, page=169, col='c', row=7)]
    >>> s = SortedSet([Usage(n, "sl") for n in i])
    >>> c = _get_set_counts(s)
    >>> c.get_counts(True)
    (2, 0)
    >>> c.get_counts(False)
    (2, 0)

    >>> i = [Index(ch=1, alt=True, page=168, col='c', row=7, var=True), Index(ch=1, alt=True, page=168, col='c', row=7)]
    >>> s = SortedSet([Usage(n, "sl", "W" if n.var else "") for n in i])
    >>> c = _get_set_counts(s)
    >>> c.get_counts(False)
    (1, 1)
    >>> c.get_counts(True)
    (2, 0)
    """
    lang = next(iter(s)).lang
    orig_var = VAR_SL if lang == "sl" else VAR_GR
    trans_var = VAR_GR if lang == "sl" else VAR_SL
    r = Counter()
    for nxt in s:
        assert nxt.lang == lang

        found = False
        for v in orig_var:
            if v in nxt.var:
                r.orig_var.add(nxt.idx)
                found = True
                break
        if not found:
            r.orig_main.add(nxt.idx)

        found = False
        for v in trans_var:
            if v in nxt.var:
                r.trans_var.add(nxt.idx)
                found = True
                break
        if not found:
            r.trans_main.add(nxt.idx)

    return r


def _get_dict_counts(d: Union[SortedDict, dict]) -> Counter:
    """
    >>> u = Usage(Index(ch=1, alt=False, page=5, col='a', row=5), "sl")
    >>> d = SortedDict({'pass. >> ἀγνοέω': {('не бѣ ꙗвленъ•', 'ἠγνοεῖτο'): SortedSet([u])}})
    >>> c = _get_dict_counts(d)
    >>> c.get_counts(True)
    (1, 0)
    >>> c.get_counts(False)
    (1, 0)

    >>> u1 = Usage(Index(ch=1, alt=False, page=8, col='a', row=3), "sl")
    >>> u2 = Usage(Index(ch=1, alt=False, page=6, col='b', row=7), "sl")
    >>> d = SortedDict({'lem2': SortedDict({'lem1': SortedDict({'τοσоῦτος': {('тол\ue205ко•', 'τοσοῦτοι'): SortedSet([u1]), ('тол\ue205ка', 'τοσαῦτα'): SortedSet([u2])}})})})
    >>> c = _get_dict_counts(d)
    >>> c.get_counts(True)
    (2, 0)
    >>> c.get_counts(False)
    (2, 0)
    """
    r = Counter()
    any = next(iter(d.values()))
    if type(any) is SortedSet:
        for n in d.values():
            r += _get_set_counts(n)
    else:  # type(any) is SortedDict or type(any) is dict:
        for n in d.values():
            r += _get_dict_counts(n)
    return r


def _generate_counts(par, d: Union[SortedDict, dict], trans: bool = False) -> None:
    c = _get_dict_counts(d).get_counts(trans)
    run = par.add_run()
    run.add_text(" (")
    if c[0]:
        run.add_text(str(c[0]))
        if c[1]:
            run.add_text(" + ")
    if c[1]:
        run.add_text(str(c[1]))
        _generate_text(par, "var", superscript=True)


def _generate_line(level: int, lang: str, d: SortedDict, doc: Document) -> None:
    """Builds the hierarchical entries of the dictionary. Recursion ensures that this works with variable depth.

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
            par.paragraph_format.space_before = Pt(0)
            par.paragraph_format.space_after = Pt(0)
            if level > 0:
                par.paragraph_format.first_line_indent = Pt(10)

            _generate_text(
                par,
                li,
                fonts[lang],
                size=Pt(14 if level == 0 else 12),
                bold=level == 0,
                indent=Cm(0.25 * level),
            )

            _generate_counts(par, next_d, False)
            _generate_text(par, ")")
        any_child = next(iter(next_d.values()))
        any_of_any = next(iter(any_child.values()))
        if type(any_of_any) is SortedSet:  # bottom of structure
            trans_lang = "gr" if lang == "sl" else "sl"
            for t, bottom_d in next_d.items():
                par = doc.add_paragraph()
                par.style.font.name = GENERIC_FONT
                par.paragraph_format.space_before = Pt(0)
                par.paragraph_format.space_after = Pt(0)
                par.paragraph_format.left_indent = Cm(1)

                _generate_text(par, t, fonts[trans_lang])
                _generate_counts(par, bottom_d, True)

                run = par.add_run()
                # run.font.name = GENERIC_FONT
                run.add_text("): ")
                first = True
                pairs = dict(bottom_d.items())
                for key in sorted(pairs, key=pairs.__getitem__):
                    usage = bottom_d[key]
                    if not first:
                        par.add_run().add_text("; ")
                    docx_result(par, key, usage, lang)
                    first = False

        else:
            _generate_line(level + 1, lang, next_d, doc)


def generate_docx(d: SortedDict, lang: str, fname: str) -> None:
    doc = Document()
    doc.styles["Normal"].font.name = GENERIC_FONT
    _generate_line(0, lang, d, doc)
    doc.save(fname)
