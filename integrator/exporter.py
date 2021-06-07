from typing import Tuple, List, Optional, Union

from sortedcontainers import SortedDict, SortedSet  # type: ignore

from docx import Document  # type: ignore
from docx.shared import RGBColor, Pt, Cm  # type: ignore

from model import Index, Usage

GENERIC_FONT = "Times New Roman"

fonts = {"gr": GENERIC_FONT, "sl": "CyrillicaOchrid10U"}
colors = {"gr": RGBColor(0x55, 0x00, 0x00), "sl": RGBColor(0x00, 0x00, 0x55)}


def _generate_text(
    par,
    text: str,
    font: str = "",
    color: str = "",
    size: Optional[Pt] = None,
    bold: bool = False,
    italic: bool = False,
    indent: Optional[Cm] = None,
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
    run.add_text(text)


def docx_usage(par, key: Tuple[str, str], usage: List[Usage], src_style: str) -> None:
    """
    key: (word,translation)
    usage: list of indices of usages also containing their styles
    """
    other_style = "gr" if src_style == "sl" else "sl"

    _generate_text(par, key[0], fonts[src_style], colors[src_style])

    run = par.add_run()
    run.add_text("/")

    _generate_text(par, key[1], fonts[other_style], colors[other_style])

    run = par.add_run()
    run.add_text(" (")

    first = True
    for next in usage:
        if not first:
            run = par.add_run()
            run.add_text(", ")
        run = par.add_run()
        run.font.bold = next.idx.bold
        run.font.italic = next.idx.italic
        run.add_text(str(next.idx))
        first = False
    run = par.add_run()
    run.add_text(")")


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
    run = par.add_run()
    run.add_text(str(idx))
    if idx.var:
        run = par.add_run()
        run.font.superscript = True
        run.add_text(idx.var)


def docx_result(par, key: Tuple[str, str], usage: List[Usage], src_style: str) -> None:
    """
    key: (word,translation)
    usage: list of indices of usages also containing their styles
    """
    other_style = "gr" if src_style == "sl" else "sl"

    run = par.add_run()
    first = True
    for next in usage:
        if not first:
            run = par.add_run()
            run.add_text("; ")
        run = par.add_run()
        run.font.bold = next.idx.bold
        run.font.italic = next.idx.italic
        run.add_text(str(next.idx))
        if next.var:
            run = par.add_run()
            run.font.superscript = True
            run.add_text(next.var)
            run = par.add_run()
        run.add_text(next.suffix())
        first = False


def _get_set_counts(s: SortedSet) -> Tuple[int, int]:
    """
    >>> i = [Index(ch=1, alt=True, page=168, col='c', row=7), Index(ch=1, alt=True, page=169, col='c', row=7)]
    >>> s = SortedSet([Usage(n, "sl") for n in i])
    >>> _get_set_counts(s)
    (2, 0)

    >>> i = [Index(ch=1, alt=True, page=168, col='c', row=7, var=True), Index(ch=1, alt=True, page=168, col='c', row=7)]
    >>> s = SortedSet([Usage(n, "sl") for n in i])
    >>> _get_set_counts(s)
    (1, 1)
    """
    r = (0, 0)
    for next in s:
        r = (r[0], r[1] + 1) if next.idx.var else (r[0] + 1, r[1])
    return r


def _get_dict_counts(d: Union[SortedDict, dict]) -> Tuple[int, int]:
    """
    >>> u = Usage(Index(ch=1, alt=False, page=5, col='a', row=5), "sl")
    >>> d = SortedDict({'pass. >> ἀγνοέω': {('не бѣ ꙗвленъ•', 'ἠγνοεῖτο'): SortedSet([u])}})
    >>> _get_dict_counts(d)
    (1, 0)

    >>> u1 = Usage(Index(ch=1, alt=False, page=8, col='a', row=3), "sl")
    >>> u2 = Usage(Index(ch=1, alt=False, page=6, col='b', row=7), "sl")
    >>> d = SortedDict({'': SortedDict({'': SortedDict({'τοσоῦτος': {('тол\ue205ко•', 'τοσοῦτοι'): SortedSet([u1]), ('тол\ue205ка', 'τοσαῦτα'): SortedSet([u2])}})})})
    >>> _get_dict_counts(d)
    (2, 0)
    """
    r = (0, 0)
    any = next(iter(d.values()))
    if type(any) is SortedSet:
        for n in d.values():
            a = _get_set_counts(n)
            r = (r[0] + a[0], r[1] + a[1])
    else:  # type(any) is SortedDict or type(any) is dict:
        for n in d.values():
            a = _get_dict_counts(n)
            r = (r[0] + a[0], r[1] + a[1])
    return r


def _generate_counts(par, d: Union[SortedDict, dict]) -> None:
    c = _get_dict_counts(d)
    assert c[0] or c[1]
    run = par.add_run()
    run.add_text(" (")
    if c[0]:
        run.add_text(str(c[0]))
        if c[1]:
            run.add_text(" + ")
    if c[1]:
        run.add_text(str(c[1]))
        run = par.add_run()
        run.font.superscript = True
        run.add_text("var")


def _generate_line(level: int, lang: str, d: SortedDict, doc: Document):
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

            _generate_counts(par, next_d)
            run = par.add_run()
            run.add_text(")")
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
                _generate_counts(par, bottom_d)

                run = par.add_run()
                run.font.name = GENERIC_FONT
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
