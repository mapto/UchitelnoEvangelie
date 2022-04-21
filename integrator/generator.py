"""The exporter specific to the indexgenerator"""
from typing import Dict, Union

from sortedcontainers import SortedDict, SortedSet  # type: ignore

from docx import Document  # type: ignore
from docx.shared import Pt, Cm  # type: ignore

from config import FROM_LANG, TO_LANG
from config import VAR_GR, VAR_SL
from const import SPECIAL_CHARS
from const import CF_SEP
from const import BRACE_OPEN, BRACE_CLOSE
from util import main_source, subscript
from address import Index
from model import Alternative, Usage, Counter, Source

from wordproc import _generate_text, any_grandchild
from wordproc import GENERIC_FONT, other_lang, fonts

BULLET_STYLE = "List Bullet"
LEVEL_OFFSET = 0.4


def _generate_usage_alt_vars(par, lang: str, alt_var: Alternative) -> None:
    first = True
    _generate_text(par, f" {BRACE_OPEN[lang]}")
    for lsrc, lemma in alt_var.var_lemmas.items():
        args = [
            # tpl[1] for wsrc, tpl in alt_var.var_words.items() if wsrc and tpl[0] and wsrc.inside([lsrc])
            tpl[1]
            for wsrc, tpl in alt_var.var_words.items()
            if wsrc.inside([lsrc])
        ]
        cnt = max(args) if args else 1
        if first:
            first = False
        else:
            _generate_text(par, ", ")
        _generate_text(par, lemma, fonts[lang])
        if lsrc:
            _generate_text(par, str(lsrc._sort_vars()), superscript=True)
        if cnt > 1:
            _generate_text(par, subscript(cnt, lang), subscript=True)
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


def _generate_usage(par, u: Usage) -> None:
    _generate_index(par, u)
    if not u.orig_alt and not u.trans_alt:
        return

    _generate_text(par, f" {CF_SEP}")
    if u.orig_alt.main_lemma:
        _generate_text(par, " ")
        _generate_text(par, u.orig_alt.main_lemma, fonts[u.lang])
        _generate_text(par, f" {main_source(u.lang, u.idx.alt)}")
        if u.orig_alt.main_cnt > 1:
            _generate_text(par, subscript(u.orig_alt.main_cnt, u.lang), subscript=True)

    if u.orig_alt.var_lemmas:
        _generate_usage_alt_vars(par, u.lang, u.orig_alt)

    if u.trans_alt.main_lemma:
        _generate_text(par, " ")
        _generate_text(par, u.trans_alt.main_lemma, fonts[other_lang[u.lang]])
        _generate_text(par, f" {main_source(other_lang[u.lang], u.idx.alt)}")
        if u.trans_alt.main_cnt > 1:
            _generate_text(
                par, subscript(u.trans_alt.main_cnt, other_lang[u.lang]), subscript=True
            )

    if u.trans_alt.var_lemmas:
        _generate_usage_alt_vars(par, other_lang[u.lang], u.trans_alt)


def docx_result(par, usage: SortedSet, src_style: str) -> None:
    """
    usage: list of indices of usages also containing their styles
    """
    first = True
    for next in usage:
        if first:
            first = False
        else:
            _generate_text(par, "; ")
        try:
            _generate_usage(par, next)
        except Exception as e:
            print(
                f"ГРЕШКА: При генериране възникна проблем в ред {next.idx} или групата му"
            )
            print(e)
            break


def _get_set_counts(s: SortedSet) -> Counter:
    """
    >>> i = [Index(ch=1, alt=True, page=168, col='c', row=7), Index(ch=1, alt=True, page=169, col='c', row=7)]
    >>> s = SortedSet([Usage(n, FROM_LANG) for n in i])
    >>> c = _get_set_counts(s)
    >>> c.get_counts(True)
    (2, 0)
    >>> c.get_counts(False)
    (2, 0)

    >>> i = [Index(ch=1, alt=True, page=168, col='c', row=7), Index(ch=1, alt=True, page=168, col='c', row=7, ocnt=2)]
    >>> s = SortedSet([Usage(n, FROM_LANG, "W" if x == 0 else "") for x, n in enumerate(i)])
    >>> c = _get_set_counts(s)
    >>> c.get_counts(False)
    (1, 1)
    >>> c.get_counts(True)
    (2, 0)
    """
    lang = next(iter(s)).lang
    orig_var = VAR_SL if lang == FROM_LANG else VAR_GR
    trans_var = VAR_GR if lang == FROM_LANG else VAR_SL
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
    >> c = _get_dict_counts({})
    >> c.get_counts(True)
    (0, 0)
    >> c.get_counts(False)
    (0, 0)

    >>> u = Usage(Index(ch=1, alt=False, page=5, col='a', row=5), FROM_LANG)
    >>> d = SortedDict({'pass. >> ἀγνοέω': {('не бѣ ꙗвленъ•', 'ἠγνοεῖτο'): SortedSet([u])}})
    >>> c = _get_dict_counts(d)
    >>> c.get_counts(True)
    (1, 0)
    >>> c.get_counts(False)
    (1, 0)

    >>> u1 = Usage(Index(ch=1, alt=False, page=8, col='a', row=3), FROM_LANG)
    >>> u2 = Usage(Index(ch=1, alt=False, page=6, col='b', row=7), FROM_LANG)
    >>> d = SortedDict({'lem2': SortedDict({'lem1': SortedDict({'τοσоῦτος': {('тол\ue205ко•', 'τοσοῦτοι'): SortedSet([u1]), ('тол\ue205ка', 'τοσαῦτα'): SortedSet([u2])}})})})
    >>> c = _get_dict_counts(d)
    >>> c.get_counts(True)
    (2, 0)
    >>> c.get_counts(False)
    (2, 0)
    """
    # print(dict(d))
    r = Counter()
    # if not d:
    #    return r
    any = next(iter(d.values()))
    if type(any) is SortedSet:
        for n in d.values():
            r += _get_set_counts(n)
    else:  # type(any) is SortedDict or type(any) is dict:
        for k, n in d.items():
            try:
                r += _get_dict_counts(n)
            except StopIteration as si:
                print(f"ГРЕШКА: При генериране неуспешно преброяване на {k}")
                raise si
    return r


def _generate_counts(par, d: Union[SortedDict, dict], trans: bool = False) -> None:
    try:
        c = _get_dict_counts(d).get_counts(trans)
    except StopIteration as si:
        keys = []
        key = next(iter(d))
        if key:
            keys += [key]
        while key and key in d and bool(d[key]):
            d = d[key]
            key = next(iter(d))
            if key:
                keys += [key]
        # TODO: Better reporting
        if keys:
            print(f"ГРЕШКА: При генериране възникна проблем с {'|'.join(keys)}")
        else:
            print(f"ГРЕШКА: При генериране възникна неидентифициран проблем")
        print(f"ГРЕШКА: При генериране неуспешно преброяване в {d}")
        return
    run = par.add_run()
    run.add_text(" (")
    if c[0]:
        run.add_text(str(c[0]))
        if c[1]:
            run.add_text(" + ")
    if c[1]:
        run.add_text(str(c[1]))
        _generate_text(par, "var", superscript=True)


def _generate_usage_line(lang: str, d: SortedDict, doc: Document) -> None:
    """Merges together all occurences for the purposes of ordering, because usage pairs are not shown"""
    trans_lang = TO_LANG if lang == FROM_LANG else FROM_LANG
    for t, bottom_d in d.items():
        # c = _get_dict_counts(d).get_counts(True)
        # if not c[0] and not c[1]:
        #    return

        par = doc.add_paragraph()
        par.style = doc.styles[BULLET_STYLE]
        par.style.font.name = GENERIC_FONT
        par.paragraph_format.space_before = Cm(0)
        par.paragraph_format.space_after = Cm(0)
        par.paragraph_format.left_indent = Cm(LEVEL_OFFSET * 4)

        _generate_text(par, t, fonts[trans_lang])
        _generate_counts(par, bottom_d, True)

        run = par.add_run()
        # run.font.name = GENERIC_FONT
        run.add_text("): ")
        total = SortedSet()
        for nxt in bottom_d.values():
            total.update(nxt)
        docx_result(par, total, lang)


def _generate_line(level: int, lang: str, d: SortedDict, doc: Document) -> None:
    """Builds the hierarchical entries of the dictionary.
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
        # c = _get_dict_counts(d).get_counts(False)
        # if not c[0] and not c[1]:
        #    return
        if li:
            par = doc.add_paragraph()
            par.style.font.name = GENERIC_FONT
            par.paragraph_format.space_before = Cm(0)
            par.paragraph_format.space_after = Cm(0)
            if level > 0:
                par.paragraph_format.first_line_indent = Cm(LEVEL_OFFSET * level)

            prefix = "" if li[0] in SPECIAL_CHARS else "| " * level
            _generate_text(
                par,
                f"{prefix}{li}",
                fonts[lang],
                size=Pt(14 if level == 0 else 12),
                bold=level == 0,
                indent=Cm(LEVEL_OFFSET * level),
            )

            _generate_counts(par, next_d, False)
            _generate_text(par, ")")

        try:
            any_of_any = any_grandchild(next_d)
        except AssertionError as ae:
            print(
                f"ГРЕШКА: При генериране възникна проблем с една от {len(next_d)} употреби на {li}"
            )
            raise ae
        if type(any_of_any) is SortedSet:  # bottom of structure
            _generate_usage_line(lang, next_d, doc)
        else:
            try:
                _generate_line(level + 1, lang, next_d, doc)
            except AssertionError as ae:
                print(
                    f"ГРЕШКА: При генериране възникна проблем с една от {len(next_d)} употреби на {li}"
                )


def generate_docx(d: SortedDict, lang: str, fname: str) -> None:
    doc = Document()
    doc.styles["Normal"].font.name = GENERIC_FONT
    _generate_line(0, lang, d, doc)

    doc.save(fname)
