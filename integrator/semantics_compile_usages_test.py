"""Tests of LangSemantics.compile_usages"""

from sortedcontainers.sorteddict import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL
from model import Index, Usage, Source, Alternative
from semantics import MainLangSemantics, VarLangSemantics


def test_para():
    sl_sem = MainLangSemantics(
        FROM_LANG,
        5,
        [7, 8, 9, 10],
        VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        TO_LANG,
        11,
        [12, 13, 14],
        VarLangSemantics(TO_LANG, 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

    row = (
        [""] * 4
        + ["1/W168a19"]
        + ["Instr.", ""] * 2
        + [""] * 2
        + ["παρὰ", "παρά", "παρά + Dat."]
        + [""] * 13
        + ["1"] * 4
    )

    d2 = SortedDict()
    d2 = gr_sem.compile_usages(sl_sem, row, d2, "παρά", "Instr.")
    # print(d2)
    assert d2 == {
        "Instr.": {
            ("παρὰ", "Instr."): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="a",
                            row=19,
                            word="παρὰ",
                        ),
                        lang=TO_LANG,
                    )
                ]
            )
        }
    }

    row = (
        ["вь WGH", "въ", "въ + Loc.", "", "1/7d1", "оу", "оу насъ", "ѹ"]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["παρ’ C", "παρά", "παρά + Acc."]
        + [""] * 8
        + ["1"] * 4
    )
    d3 = SortedDict()
    d3 = gr_sem.var.compile_usages(sl_sem, row, d3, "παρά", "ѹ")
    assert d3 == {
        "ѹ": {
            ("παρ’ C", "оу"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=False,
                            page=7,
                            col="d",
                            row=1,
                            word="παρ’ C",
                        ),
                        lang=TO_LANG,
                        var=Source("C"),
                        trans_alt=Alternative(
                            var_lemmas={Source("WGH"): "въ"},
                            var_words={Source("WGH"): ("вь WGH", 1)},
                        ),
                    )
                ]
            )
        }
    }


def test_ipercliso():
    sl_sem = MainLangSemantics(
        FROM_LANG,
        5,
        [7, 8, 9, 10],
        VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        TO_LANG,
        11,
        [12, 13, 14],
        VarLangSemantics(TO_LANG, 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

    rows = [
        [""] * 4
        + [
            "1/W168c17",
            "\ue205сто\ue20dен\ue205\ue205",
            "всѣмь прѣ\ue205сто\ue20dе\ue201• \ue205 по \ue205сто\ue20dен\ue205\ue205",
            "\ue205сто\ue20dен\ue205\ue201",
        ]
        + [""] * 3
        + ["ὑπερκλύσαι", "ὑπερκλύζω", "inf."]
        + [""] * 2
        + ["ὑπερβλύσαι C", "ὑπερβλύω", "inf."]
        + [""] * 8
        + ["1"] * 4,
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
        + ["ὑπερβλύζων C", "ὑπερβλύω"]
        + [""] * 9
        + ["1"] * 4,
    ]

    d2 = SortedDict()
    d2 = gr_sem.var.compile_usages(
        sl_sem, rows[0], d2, "ὑπερβλύω", "\ue205сто\ue20dен\ue205\ue201"
    )
    d2 = gr_sem.var.compile_usages(
        sl_sem, rows[1], d2, "ὑπερβλύω", "прѣ\ue205сто\ue20d\ue205т\ue205"
    )
    assert d2 == {
        "прѣ\ue205сто\ue20d\ue205т\ue205": {
            ("ὑπερβλύζων C", "прѣ\ue205сто\ue20dе"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="c",
                            row=17,
                            word="ὑπερβλύζων C",
                        ),
                        lang=TO_LANG,
                        var=Source("C"),
                        orig_alt=Alternative(
                            main_lemma="ὑπερκλύζω",
                            main_word="ὑπερκλύζων",
                        ),
                    )
                ]
            )
        },
        "\ue205сто\ue20dен\ue205\ue201": {
            ("ὑπερβλύσαι C", "\ue205сто\ue20dен\ue205\ue205"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="c",
                            row=17,
                            word="ὑπερβλύσαι C",
                        ),
                        lang=TO_LANG,
                        var=Source("C"),
                        orig_alt=Alternative(
                            main_lemma="ὑπερκλύζω",
                            main_word="ὑπερκλύσαι",
                        ),
                    )
                ]
            )
        },
    }


def test_verovat():
    sl_sem = MainLangSemantics(
        FROM_LANG,
        5,
        [7, 8, 9, 10],
        VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        TO_LANG,
        11,
        [12, 13, 14],
        VarLangSemantics(TO_LANG, 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт_",
            "",
            "1/7b19",
            "вѣроують",
            "вьс_ вѣроують",
            "вѣроват_",
        ]
        + ([""] * 3)
        + [
            "πιστεύσωσι",
            "πιστεύω",
        ]
        + ([""] * 13)
        + ["hl00"]
        + ["1"] * 4
    )

    d1 = SortedDict()
    d1 = sl_sem.compile_usages(gr_sem, row, d1, "вѣроват_", "πιστεύω")
    assert d1 == {
        "πιστεύω": {
            ("вѣроують", "πιστεύσωσι"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=False,
                            page=7,
                            col="b",
                            row=19,
                            word="вѣроують",
                        ),
                        lang=FROM_LANG,
                        orig_alt=Alternative(
                            var_lemmas={Source("GH"): "вѣра"},
                            var_words={Source("GH"): ("вѣроу GH", 1)},
                        ),
                    )
                ]
            )
        }
    }
    d2 = SortedDict()
    d2 = gr_sem.compile_usages(sl_sem, row, d2, "πιστεύω", "вѣроват_")
    assert d2 == {
        "вѣроват_": {
            ("πιστεύσωσι", "вѣроують"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=False,
                            page=7,
                            col="b",
                            row=19,
                            word="πιστεύσωσι",
                        ),
                        lang=TO_LANG,
                        trans_alt=Alternative(
                            var_lemmas={Source("GH"): "вѣра"},
                            var_words={Source("GH"): ("вѣроу GH", 1)},
                        ),
                    )
                ]
            )
        }
    }


def test_mene():
    sl_sem = MainLangSemantics(
        FROM_LANG,
        5,
        [7, 8, 9, 10],
        VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        TO_LANG,
        11,
        [12, 13, 14],
        VarLangSemantics(TO_LANG, 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

    row = (
        [""] * 4
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + [""] * 3
        + ["μὲν"]
        + [""] * 4
        + ["με C", "ἐγώ"]
        + [""] * 9
        + ["1"] * 4
    )

    d3 = SortedDict()
    d3 = sl_sem.compile_usages(gr_sem.var, row, d3, "аꙁъ", "ἐγώ")
    assert d3 == {
        "ἐγώ": {
            ("мене", "με C"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="c",
                            row=7,
                            word="мене",
                        ),
                        lang=FROM_LANG,
                        var=Source("C"),
                    )
                ]
            )
        }
    }
    d4 = SortedDict()
    d4 = gr_sem.var.compile_usages(sl_sem, row, d4, "ἐγώ", "аꙁъ")
    assert d4 == {
        "аꙁъ": {
            ("με C", "мене"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="c",
                            row=7,
                            word="με C",
                        ),
                        lang=TO_LANG,
                        var=Source("C"),
                    )
                ]
            )
        }
    }


def test_monogenis():
    sl_sem = MainLangSemantics(
        FROM_LANG,
        5,
        [7, 8, 9, 10],
        VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        TO_LANG,
        11,
        [12, 13, 14],
        VarLangSemantics(TO_LANG, 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

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
        + ["1"] * 4
    )

    d0 = SortedDict()
    d0 = sl_sem.compile_usages(gr_sem, row, d0, "\ue205но\ue20dѧдъ", "μονογενής")
    assert d0 == {
        "μονογενής": {
            ("\ue205но\ue20dадꙑ\ue205", "μονογενὴς"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=False,
                            page=5,
                            col="a",
                            row=4,
                            word="\ue205но\ue20dадꙑ\ue205",
                        ),
                        lang=FROM_LANG,
                        orig_alt=Alternative(
                            var_lemmas={Source("WH"): "\ue201д\ue205но\ue20dѧдъ"},
                            var_words={
                                Source("WH"): ("\ue201д\ue205но\ue20dеды WH", 1)
                            },
                        ),
                    )
                ]
            )
        }
    }

    d01 = SortedDict()
    # d01 = gr_sem.compile_usages(sl_sem.var, row, d01, "μονογενής", "\ue205но\ue20dѧдъ")
    # assert d01 == SortedDict()

    d01 = gr_sem.compile_usages(sl_sem, row, d01, "μονογενής", "\ue205но\ue20dѧдъ")
    assert d01 == {
        "\ue205но\ue20dѧдъ": {
            ("μονογενὴς", "\ue205но\ue20dадꙑ\ue205"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=False,
                            page=5,
                            col="a",
                            row=4,
                            word="μονογενὴς",
                        ),
                        lang=TO_LANG,
                        trans_alt=Alternative(
                            var_lemmas={Source("WH"): "\ue201д\ue205но\ue20dѧдъ"},
                            var_words={
                                Source("WH"): ("\ue201д\ue205но\ue20dеды WH", 1)
                            },
                        ),
                    )
                ]
            )
        }
    }

    row = (
        [
            "\ue205но\ue20dедаго G  \ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ H / \ue205но\ue20dѧдъ G",
        ]
        + [""] * 2
        + [
            "1/W168a25",
            "\ue201д\ue205но\ue20dедоу",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 13
        + ["bold|italic"]
        + ["1"] * 4
    )

    d1 = SortedDict()
    d1 = sl_sem.var.compile_usages(gr_sem, row, d1, "\ue205но\ue20dѧдъ", "μονογενής")
    assert d1 == {
        "μονογενής": {
            ("\ue205но\ue20dедаго G", "μονογενοῦς"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="a",
                            row=25,
                            bold=True,
                            italic=True,
                            word="\ue205но\ue20dедаго G",
                        ),
                        lang=FROM_LANG,
                        var=Source("G"),
                        orig_alt=Alternative(
                            main_lemma="\ue201д\ue205но\ue20dѧдъ",
                            var_lemmas={Source("H"): "\ue201д\ue205нородъ"},
                            main_word="\ue201д\ue205но\ue20dедоу",
                            var_words={Source("H"): ("\ue201д\ue205нородоу H", 1)},
                        ),
                    )
                ]
            )
        }
    }

    d2 = SortedDict()
    d2 = sl_sem.var.compile_usages(gr_sem, row, d2, "\ue201д\ue205нородъ", "μονογενής")
    assert d2 == {
        "μονογενής": {
            ("\ue201д\ue205нородоу H", "μονογενοῦς"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="a",
                            row=25,
                            bold=True,
                            italic=True,
                            word="\ue201д\ue205нородоу H",
                        ),
                        lang=FROM_LANG,
                        var=Source("H"),
                        orig_alt=Alternative(
                            main_lemma="\ue201д\ue205но\ue20dѧдъ",
                            var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
                            main_word="\ue201д\ue205но\ue20dедоу",
                            var_words={Source("G"): ("\ue205но\ue20dедаго G", 1)},
                        ),
                    )
                ]
            )
        }
    }

    row = (
        [
            "\ue205но\ue20dедаго G  \ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ H / \ue205но\ue20dѧдъ G",
        ]
        + [""] * 2
        + [
            "1/W168a25",
            "\ue201д\ue205но\ue20dедоу",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 14
        + ["1"] * 4
    )

    d = SortedDict()
    d = sl_sem.var.compile_usages(gr_sem, row, d, "\ue205но\ue20dѧдъ", "μονογενής")
    # print(d)
    expected = {
        "μονογενής": {
            ("\ue205но\ue20dедаго G", "μονογενοῦς"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="a",
                            row=25,
                            word="\ue205но\ue20dедаго G",
                        ),
                        lang=FROM_LANG,
                        var=Source("G"),
                        orig_alt=Alternative(
                            main_lemma="\ue201д\ue205но\ue20dѧдъ",
                            var_lemmas={Source("H"): "\ue201д\ue205нородъ"},
                            main_word="\ue201д\ue205но\ue20dедоу",
                            var_words={Source("H"): ("\ue201д\ue205нородоу H", 1)},
                        ),
                    )
                ]
            )
        }
    }
    assert d == expected

    d = SortedDict()
    d = sl_sem.var.compile_usages(gr_sem, row, d, "\ue201д\ue205нородъ", "μονογενής")
    expected = {
        "μονογενής": {
            ("\ue201д\ue205нородоу H", "μονογενοῦς"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="a",
                            row=25,
                            word="\ue201д\ue205нородоу H",
                        ),
                        lang=FROM_LANG,
                        var=Source("H"),
                        orig_alt=Alternative(
                            main_lemma="\ue201д\ue205но\ue20dѧдъ",
                            var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
                            main_word="\ue201д\ue205но\ue20dедоу",
                            var_words={Source("G"): ("\ue205но\ue20dедаго G", 1)},
                        ),
                    )
                ]
            )
        }
    }
    assert d == expected

    d = SortedDict()
    d = gr_sem.compile_usages(sl_sem, row, d, "μονογενής", "\ue201д\ue205но\ue20dѧдъ")
    expected = {
        "\ue201д\ue205но\ue20dѧдъ": {
            ("μονογενοῦς", "\ue201д\ue205но\ue20dедоу"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="a",
                            row=25,
                            word="μονογενοῦς",
                        ),
                        lang=TO_LANG,
                        trans_alt=Alternative(
                            var_lemmas={
                                Source("H"): "\ue201д\ue205нородъ",
                                Source("G"): "\ue205но\ue20dѧдъ",
                            },
                            var_words={
                                Source("H"): ("\ue201д\ue205нородоу H", 1),
                                Source("G"): ("\ue205но\ue20dедаго G", 1),
                            },
                        ),
                    )
                ]
            )
        }
    }
    assert d == expected

    d = SortedDict()
    d = gr_sem.compile_usages(sl_sem.var, row, d, "μονογενής", "\ue201д\ue205нородъ")
    expected = {
        "\ue201д\ue205нородъ": {
            ("μονογενοῦς", "\ue201д\ue205нородоу H"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="a",
                            row=25,
                            word="μονογενοῦς",
                        ),
                        lang=TO_LANG,
                        var=Source("H"),
                        trans_alt=Alternative(
                            main_lemma="\ue201д\ue205но\ue20dѧдъ",
                            var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
                            main_word="\ue201д\ue205но\ue20dедоу",
                            var_words={Source("G"): ("\ue205но\ue20dедаго G", 1)},
                        ),
                    )
                ]
            )
        }
    }
    assert d == expected

    d = SortedDict()
    d = gr_sem.compile_usages(sl_sem.var, row, d, "μονογενής", "\ue205но\ue20dѧдъ")
    expected = {
        "\ue205но\ue20dѧдъ": {
            ("μονογενοῦς", "\ue205но\ue20dедаго G"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="a",
                            row=25,
                            word="μονογενοῦς",
                        ),
                        lang=TO_LANG,
                        var=Source("G"),
                        trans_alt=Alternative(
                            main_lemma="\ue201д\ue205но\ue20dѧдъ",
                            var_lemmas={Source("H"): "\ue201д\ue205нородъ"},
                            main_word="\ue201д\ue205но\ue20dедоу",
                            var_words={Source("H"): ("\ue201д\ue205нородоу H", 1)},
                        ),
                    )
                ]
            )
        }
    }
    assert d == expected


def test_bozhii():
    sl_sem = MainLangSemantics(
        FROM_LANG,
        5,
        [7, 8, 9, 10],
        VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        TO_LANG,
        11,
        [12, 13, 14],
        VarLangSemantics(TO_LANG, 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

    r = (
        ["б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H", "бож\ue205\ue205"]
        + [""] * 2
        + ["1/7a4", "боꙁѣ", "о боꙁѣ словес\ue205•", "богъ", "Dat."]
        + [""] * 2
        + ["Θεοῦ", "θεός", "Gen."]
        + [""] * 13
        + ["1"] * 4
    )

    result = SortedDict()
    result = sl_sem.var.compile_usages(gr_sem, r, result, "бож\ue205\ue205", "θεός")
    assert result == {
        "θεός Gen.": {
            (
                "б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G",
                "Θεοῦ",
            ): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=False,
                            page=7,
                            col="a",
                            row=4,
                            word="б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G",
                        ),
                        lang=FROM_LANG,
                        var=Source("WGH"),
                        orig_alt=Alternative(
                            main_lemma="богъ",
                            main_word="боꙁѣ",
                        ),
                    )
                ]
            )
        }
    }
