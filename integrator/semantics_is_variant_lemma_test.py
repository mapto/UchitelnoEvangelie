from sortedcontainers.sorteddict import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL
from model import Source
from semantics import _is_variant_lemma
from setup import sl_sem, gr_sem


def test_ipercliso():
    row = (
        [""] * 4
        + [
            "1/W168c17",
            "прѣ\ue205сто\ue20dе",
            "всѣмь прѣ\ue205сто\ue20dе\ue201• \ue205 по \ue205сто\ue20dен\ue205\ue205",
            "прѣ\ue205сто\ue20d\ue205т\ue205",
        ]
        + [""] * 3
        + ["ὑπερκλύζων", "ὑπερκλύζω"]
        + [""] * 3
        + ["ὑπερβλύζων Cs", "ὑπερβλύω"]
        + [""] * 9
    )
    exception = False
    try:
        _is_variant_lemma(row, gr_sem, Source("Cs"), "ὑπερκλύζω")
    except AssertionError:
        exception = True
    assert exception

    assert _is_variant_lemma(row, gr_sem, Source(""), "ὑπερκλύζω")
    assert _is_variant_lemma(row, gr_sem.var, Source("Cs"), "ὑπερβλύω")

    assert not _is_variant_lemma(row, gr_sem.var, Source("M"), "ὑπερβλύω")


def test_monogenes():
    row = (
        ["\ue201д\ue205но\ue20dеды WH Ø G", "\ue201д\ue205но\ue20dѧдъ"]
        + [""] * 2
        + [
            "1/5a4",
            "\ue205но\ue20dадꙑ\ue205",
            "нъ ꙗко б\ue010ъ• а \ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενὴς", "μονογενής"]
        + [""] * 14
    )
    assert _is_variant_lemma(row, sl_sem.var, Source("HW"), "\ue201д\ue205но\ue20dѧдъ")
    assert not _is_variant_lemma(
        row, sl_sem.var, Source("G"), "\ue201д\ue205но\ue20dѧдъ"
    )
    assert not _is_variant_lemma(row, sl_sem.var, Source("G"), "\ue205но\ue20dѧдъ")
    assert _is_variant_lemma(row, sl_sem, Source(""), "\ue205но\ue20dѧдъ")
    assert _is_variant_lemma(row, gr_sem, Source(""), "μονογενής")
    assert not _is_variant_lemma(row, gr_sem.var, Source(""), "μονογενής")


def test_bozhii():
    row = (
        ["б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H", "бож\ue205\ue205"]
        + [""] * 2
        + ["1/7a4", "боꙁѣ", "о боꙁѣ словес\ue205•", "богъ", "Dat."]
        + [""] * 2
        + ["Θεοῦ", "θεός", "Gen."]
        + [""] * 13
    )
    assert _is_variant_lemma(row, sl_sem.var, Source("W"), "бож\ue205\ue205")
