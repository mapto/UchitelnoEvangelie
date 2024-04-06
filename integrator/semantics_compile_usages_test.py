"""Tests of LangSemantics.compile_usages"""

from sortedcontainers.sorteddict import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL
from model import Alternative, Index, Source, Alignment, Usage
from semantics import MainLangSemantics, VarLangSemantics

# semantics update from September 2021
# with repetitions added (as if after merge)
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


def test_para():
    row = (
        [""] * 4
        + ["1/W168a19"]
        + ["Instr.", ""] * 2
        + [""] * 2
        + ["παρὰ", "παρά", "παρά + Dat."]
        + [""] * 13
        + ["1"] * 4
    )

    d2 = gr_sem.compile_usages(sl_sem, row, "Instr.", d=SortedDict())
    # print(d2)
    assert d2 == {
        "Instr.": {
            ("παρὰ", "Instr."): SortedSet(
                [
                    Alignment(
                        Index("1/W168a19"),
                        Usage(
                            TO_LANG,
                            word="παρὰ",
                            lemmas=["παρά", "παρά + Dat."],
                        ),
                        Usage("sl", word="Instr.", lemmas=["Instr."]),
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
        + ["παρ’ Cs", "παρά", "παρά + Acc."]
        + [""] * 8
        + ["1"] * 4
    )
    d3 = gr_sem.var.compile_usages(sl_sem, row, "ѹ", Source("Cs"), SortedDict())
    assert d3 == {
        "ѹ": {
            ("παρ’ Cs", "оу"): SortedSet(
                [
                    Alignment(
                        Index("1/7d1"),
                        Usage(
                            "gr",
                            Source("Cs"),
                            word="παρ’ Cs",
                            lemmas=["παρά", "παρά + Acc."],
                        ),
                        Usage(
                            "sl",
                            var_alt={
                                Source("WGH"): Alternative(
                                    "вь WGH", ["въ", "въ + Loc."]
                                ),
                            },
                            word="оу",
                            lemmas=["ѹ"],
                        ),
                    )
                ]
            )
        }
    }


def test_ipercliso():
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
        + ["ὑπερβλύσαι Cs", "ὑπερβλύω", "inf."]
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
        + ["ὑπερβλύζων Cs", "ὑπερβλύω"]
        + [""] * 9
        + ["1"] * 4,
    ]

    d2 = gr_sem.var.compile_usages(
        sl_sem, rows[0], "\ue205сто\ue20dен\ue205\ue201", Source("Cs"), SortedDict()
    )
    d2 = gr_sem.var.compile_usages(
        sl_sem, rows[1], "прѣ\ue205сто\ue20d\ue205т\ue205", Source("Cs"), d2
    )
    assert d2 == {
        "прѣ\ue205сто\ue20d\ue205т\ue205": {
            ("ὑπερβλύζων Cs", "прѣ\ue205сто\ue20dе"): SortedSet(
                [
                    Alignment(
                        Index("1/W168c17"),
                        Usage(
                            "gr",
                            Source("Cs"),
                            main_alt=Alternative("ὑπερκλύζων", ["ὑπερκλύζω"]),
                            word="ὑπερβλύζων Cs",
                            lemmas=["ὑπερβλύω"],
                        ),
                        Usage(
                            "sl",
                            word="прѣ\ue205сто\ue20dе",
                            lemmas=["прѣ\ue205сто\ue20d\ue205т\ue205"],
                        ),
                    )
                ]
            )
        },
        "\ue205сто\ue20dен\ue205\ue201": {
            ("ὑπερβλύσαι Cs", "\ue205сто\ue20dен\ue205\ue205"): SortedSet(
                [
                    Alignment(
                        Index("1/W168c17"),
                        Usage(
                            "gr",
                            Source("Cs"),
                            main_alt=Alternative("ὑπερκλύσαι", ["ὑπερκλύζω", "inf."]),
                            word="ὑπερβλύσαι Cs",
                            lemmas=["ὑπερβλύω", "inf."],
                        ),
                        Usage(
                            "sl",
                            word="\ue205сто\ue20dен\ue205\ue205",
                            lemmas=["\ue205сто\ue20dен\ue205\ue201"],
                        ),
                    )
                ]
            )
        },
    }


def test_verovat():
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

    d1 = sl_sem.compile_usages(gr_sem, row, "πιστεύω", d=SortedDict())
    assert d1 == {
        "πιστεύω": {
            ("вѣроують", "πιστεύσωσι"): SortedSet(
                [
                    Alignment(
                        Index("1/7b19"),
                        Usage(
                            "sl",
                            word="вѣроують",
                            lemmas=["вѣроват_"],
                            var_alt={
                                Source("GH"): Alternative(
                                    "вѣроу GH", ["вѣра", "вѣрѫ ѩт_"]
                                ),
                            },
                        ),
                        Usage("gr", word="πιστεύσωσι", lemmas=["πιστεύω"]),
                    )
                ]
            )
        }
    }

    d2 = gr_sem.compile_usages(sl_sem, row, "вѣроват_", d=SortedDict())
    assert d2 == {
        "вѣроват_": {
            ("πιστεύσωσι", "вѣроують"): SortedSet(
                [
                    Alignment(
                        Index("1/7b19"),
                        Usage(
                            "gr",
                            word="πιστεύσωσι",
                            lemmas=["πιστεύω"],
                        ),
                        Usage(
                            "sl",
                            word="вѣроують",
                            lemmas=["вѣроват_"],
                            var_alt={
                                Source("GH"): Alternative(
                                    "вѣроу GH", ["вѣра", "вѣрѫ ѩт_"]
                                ),
                            },
                        ),
                    )
                ]
            )
        }
    }


def test_mene():
    row = (
        [""] * 4
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + [""] * 3
        + ["μὲν"]
        + [""] * 4
        + ["με Cs", "ἐγώ"]
        + [""] * 9
        + ["1"] * 4
    )

    d3 = sl_sem.compile_usages(gr_sem.var, row, "ἐγώ", d=SortedDict())
    assert d3 == {
        "ἐγώ": {
            ("мене", "με Cs"): SortedSet(
                [
                    Alignment(
                        Index("1/W168c7"),
                        Usage("sl", word="мене", lemmas=["аꙁъ"]),
                        Usage("gr", Source("Cs"), word="με Cs", lemmas=["ἐγώ"]),
                    )
                ]
            )
        }
    }
    d4 = gr_sem.var.compile_usages(sl_sem, row, "аꙁъ", Source("Cs"), SortedDict())
    assert d4 == {
        "аꙁъ": {
            ("με Cs", "мене"): SortedSet(
                [
                    Alignment(
                        Index("1/W168c7"),
                        Usage(TO_LANG, var=Source("Cs"), word="με Cs", lemmas=["ἐγώ"]),
                        Usage(lang="sl", word="мене", lemmas=["аꙁъ"]),
                    )
                ]
            )
        }
    }


def test_monogenis():
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

    d0 = sl_sem.compile_usages(gr_sem, row, "μονογενής", d=SortedDict())
    assert d0 == {
        "μονογενής": {
            ("\ue205но\ue20dадꙑ\ue205", "μονογενὴς"): SortedSet(
                [
                    Alignment(
                        Index("1/5a4"),
                        Usage(
                            FROM_LANG,
                            word="\ue205но\ue20dадꙑ\ue205",
                            lemmas=["\ue205но\ue20dѧдъ"],
                            var_alt={
                                Source("WH"): Alternative(
                                    "\ue201д\ue205но\ue20dеды WH",
                                    ["\ue201д\ue205но\ue20dѧдъ"],
                                ),
                            },
                        ),
                        Usage(lang="gr", word="μονογενὴς", lemmas=["μονογενής"]),
                    )
                ]
            )
        }
    }

    d01 = gr_sem.compile_usages(sl_sem, row, "\ue205но\ue20dѧдъ", d=SortedDict())
    assert d01 == {
        "\ue205но\ue20dѧдъ": {
            ("μονογενὴς", "\ue205но\ue20dадꙑ\ue205"): SortedSet(
                [
                    Alignment(
                        Index("1/5a4"),
                        Usage(TO_LANG, word="μονογενὴς", lemmas=["μονογενής"]),
                        Usage(
                            FROM_LANG,
                            word="\ue205но\ue20dадꙑ\ue205",
                            lemmas=["\ue205но\ue20dѧдъ"],
                            var_alt={
                                Source("WH"): Alternative(
                                    "\ue201д\ue205но\ue20dеды WH",
                                    ["\ue201д\ue205но\ue20dѧдъ"],
                                ),
                            },
                        ),
                    )
                ]
            )
        }
    }


def test_monogenis2():
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

    d1 = sl_sem.var.compile_usages(gr_sem, row, "μονογενής", Source("G"), SortedDict())
    assert d1 == {
        "μονογενής": {
            ("\ue205но\ue20dедаго G", "μονογενοῦς"): SortedSet(
                [
                    Alignment(
                        Index("1/W168a25"),
                        Usage(
                            "sl",
                            var=Source("G"),
                            word="\ue205но\ue20dедаго G",
                            lemmas=["\ue205но\ue20dѧдъ"],
                            main_alt=Alternative(
                                "\ue201д\ue205но\ue20dедоу",
                                ["\ue201д\ue205но\ue20dѧдъ"],
                            ),
                            var_alt={
                                Source("H"): Alternative(
                                    "\ue201д\ue205нородоу H", ["\ue201д\ue205нородъ"]
                                )
                            },
                        ),
                        Usage(lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]),
                        bold=True,
                        italic=True,
                    )
                ]
            ),
        }
    }

    d2 = sl_sem.var.compile_usages(gr_sem, row, "μονογενής", Source("H"), SortedDict())
    assert d2 == {
        "μονογενής": {
            ("\ue201д\ue205нородоу H", "μονογενοῦς"): SortedSet(
                [
                    Alignment(
                        Index("1/W168a25"),
                        Usage(
                            "sl",
                            var=Source("H"),
                            word="\ue201д\ue205нородоу H",
                            lemmas=["\ue201д\ue205нородъ"],
                            main_alt=Alternative(
                                "\ue201д\ue205но\ue20dедоу",
                                ["\ue201д\ue205но\ue20dѧдъ"],
                            ),
                            var_alt={
                                Source("G"): Alternative(
                                    "\ue205но\ue20dедаго G", ["\ue205но\ue20dѧдъ"]
                                )
                            },
                        ),
                        Usage(lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]),
                        bold=True,
                        italic=True,
                    )
                ]
            )
        }
    }


def test_monogenis3():
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

    d = sl_sem.var.compile_usages(gr_sem, row, "μονογενής", Source("G"), SortedDict())
    # print(d)
    assert d == {
        "μονογενής": {
            ("\ue205но\ue20dедаго G", "μονογενοῦς"): SortedSet(
                [
                    Alignment(
                        Index("1/W168a25"),
                        Usage(
                            "sl",
                            var=Source("G"),
                            word="\ue205но\ue20dедаго G",
                            lemmas=["\ue205но\ue20dѧдъ"],
                            main_alt=Alternative(
                                "\ue201д\ue205но\ue20dедоу",
                                ["\ue201д\ue205но\ue20dѧдъ"],
                            ),
                            var_alt={
                                Source("H"): Alternative(
                                    "\ue201д\ue205нородоу H", ["\ue201д\ue205нородъ"]
                                )
                            },
                        ),
                        Usage(lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]),
                    )
                ]
            ),
        }
    }

    d = sl_sem.var.compile_usages(gr_sem, row, "μονογενής", Source("H"), SortedDict())
    assert d == {
        "μονογενής": {
            ("\ue201д\ue205нородоу H", "μονογενοῦς"): SortedSet(
                [
                    Alignment(
                        Index("1/W168a25"),
                        Usage(
                            "sl",
                            Source("H"),
                            word="\ue201д\ue205нородоу H",
                            lemmas=["\ue201д\ue205нородъ"],
                            main_alt=Alternative(
                                "\ue201д\ue205но\ue20dедоу",
                                ["\ue201д\ue205но\ue20dѧдъ"],
                            ),
                            var_alt={
                                Source("G"): Alternative(
                                    "\ue205но\ue20dедаго G", ["\ue205но\ue20dѧдъ"]
                                )
                            },
                        ),
                        Usage(lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]),
                    )
                ]
            ),
        }
    }

    d = gr_sem.compile_usages(sl_sem, row, "\ue201д\ue205но\ue20dѧдъ", d=SortedDict())
    assert d == {
        "\ue201д\ue205но\ue20dѧдъ": {
            ("μονογενοῦς", "\ue201д\ue205но\ue20dедоу"): SortedSet(
                [
                    Alignment(
                        Index("1/W168a25"),
                        Usage(TO_LANG, word="μονογενοῦς", lemmas=["μονογενής"]),
                        Usage(
                            FROM_LANG,
                            var_alt={
                                Source("G"): Alternative(
                                    "\ue205но\ue20dедаго G", ["\ue205но\ue20dѧдъ"]
                                ),
                                Source("H"): Alternative(
                                    "\ue201д\ue205нородоу H", ["\ue201д\ue205нородъ"]
                                ),
                            },
                            word="\ue201д\ue205но\ue20dедоу",
                            lemmas=["\ue201д\ue205но\ue20dѧдъ"],
                        ),
                    )
                ]
            )
        }
    }

    d = gr_sem.compile_usages(sl_sem.var, row, "\ue201д\ue205нородъ", d=SortedDict())
    assert d == {
        "\ue201д\ue205нородъ": {
            ("μονογενοῦς", "\ue201д\ue205нородоу H"): SortedSet(
                [
                    Alignment(
                        Index("1/W168a25"),
                        Usage(
                            "gr",
                            word="μονογενοῦς",
                            lemmas=["μονογενής"],
                        ),
                        Usage(
                            "sl",
                            var=Source("H"),
                            word="\ue201д\ue205нородоу H",
                            lemmas=["\ue201д\ue205нородъ"],
                            main_alt=Alternative(
                                "\ue201д\ue205но\ue20dедоу",
                                ["\ue201д\ue205но\ue20dѧдъ"],
                            ),
                            var_alt={
                                Source("G"): Alternative(
                                    "\ue205но\ue20dедаго G", ["\ue205но\ue20dѧдъ"]
                                )
                            },
                        ),
                    )
                ]
            )
        }
    }

    d = gr_sem.compile_usages(sl_sem.var, row, "\ue205но\ue20dѧдъ", d=SortedDict())
    assert d == {
        "\ue205но\ue20dѧдъ": {
            ("μονογενοῦς", "\ue205но\ue20dедаго G"): SortedSet(
                [
                    Alignment(
                        Index("1/W168a25"),
                        Usage(
                            "gr",
                            word="μονογενοῦς",
                            lemmas=["μονογενής"],
                        ),
                        Usage(
                            "sl",
                            Source("G"),
                            word="\ue205но\ue20dедаго G",
                            lemmas=["\ue205но\ue20dѧдъ"],
                            main_alt=Alternative(
                                "\ue201д\ue205но\ue20dедоу",
                                ["\ue201д\ue205но\ue20dѧдъ"],
                            ),
                            var_alt={
                                Source("H"): Alternative(
                                    "\ue201д\ue205нородоу H", ["\ue201д\ue205нородъ"]
                                )
                            },
                        ),
                    )
                ]
            )
        },
    }


def test_bozhii():
    r = (
        ["б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H", "бож\ue205\ue205"]
        + [""] * 2
        + ["1/7a4", "боꙁѣ", "о боꙁѣ словес\ue205•", "богъ", "Dat."]
        + [""] * 2
        + ["Θεοῦ", "θεός", "Gen."]
        + [""] * 13
        + ["1"] * 4
    )

    result = sl_sem.var.compile_usages(gr_sem, r, "θεός", Source("H"), SortedDict())
    assert result == {
        "θεός Gen.": {
            (
                "б\ue010жї\ue205 H",
                "Θεοῦ",
            ): SortedSet(
                [
                    Alignment(
                        Index("1/7a4"),
                        Usage(
                            FROM_LANG,
                            Source("H"),
                            "б\ue010жї\ue205 H",
                            ["бож\ue205\ue205"],
                            main_alt=Alternative("боꙁѣ", ["богъ", "Dat."]),
                        ),
                        Usage(lang="gr", word="Θεοῦ", lemmas=["θεός", "Gen."]),
                    )
                ]
            )
        }
    }


def test_artos():
    row = (
        [""] * 4
        + ["16/80a08", "хлѣбꙑ•", "ре\ue20dе хлѣбꙑ• не", "хлѣбъ"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 3
        + ["ἄρτους Ch", "ἄρτος"]
        + [""] * 9
        + ["1"] * 4
    )
    result = gr_sem.var.compile_usages(sl_sem, row, "хлѣбъ", Source("Ch"), SortedDict())
    assert result == {
        "хлѣбъ": {
            ("ἄρτους Ch", "хлѣбꙑ•"): SortedSet(
                [
                    Alignment(
                        Index("16/80a8"),
                        Usage(
                            "gr",
                            Source("Ch"),
                            "ἄρτους Ch",
                            ["ἄρτος"],
                            main_alt=Alternative("om.", ["om."]),
                        ),
                        Usage(lang="sl", word="хлѣбꙑ•", lemmas=["хлѣбъ"]),
                    )
                ]
            )
        }
    }


def test_est_in_var_no_main():
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
        [12, 13, 14, 15],
        VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

    row = (
        [
            "\ue201сть GH",
            "бꙑт\ue205",
            "",
            "gramm.",
            "07/47a06",
            "om.",
            "сътвор\ue205лъ",
            "om.",
        ]
        + [""] * 3
        + ["Ø"] * 2
        + [""] * 13
        + ["hl03"]
        + ["1"] * 4
    )
    result = sl_sem.var.compile_usages(gr_sem, row, "Ø", Source("GH"), SortedDict())
    assert result == {
        "Ø": {
            ("\ue201сть GH", "Ø"): SortedSet(
                [
                    Alignment(
                        Index("7/47a6"),
                        Usage(
                            "sl",
                            Source("GH"),
                            "\ue201сть GH",
                            ["бꙑт\ue205", "", "gramm."],
                            main_alt=Alternative("om.", ["om."]),
                        ),
                        Usage(lang="gr", word="Ø", lemmas=["Ø"]),
                    )
                ]
            )
        }
    }


def test_hodom_spiti():
    row = (
        [
            "хⷪ҇домь WG ход\ue205т\ue205 H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/72d18",
            "ход\ue205мъ",
            "себе• по поут\ue205 хо-",
            "ход\ue205т\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
            "",
            "",
            "προβαίνοντες",
            "προβαίνω",
        ]
        + [""] * 13
        + ["hl05|hl00"]
        + ["1"] * 4
    )

    result = gr_sem.compile_usages(sl_sem.var, row, "ходъ", d=SortedDict())
    assert result == {
        "ходомь спѣт\ue205 → ходъ": {
            ("προβαίνοντες", "хⷪ҇домь WG"): SortedSet(
                [
                    Alignment(
                        Index("14/72d18"),
                        Usage("gr", word="προβαίνοντες", lemmas=["προβαίνω"]),
                        Usage(
                            "sl",
                            Source("WG"),
                            word="хⷪ҇домь WG",
                            lemmas=["ходъ", "ходомь спѣт\ue205"],
                            main_alt=Alternative(
                                "ход\ue205мъ",
                                ["ход\ue205т\ue205", "ход\ue205т\ue205 спѣѭще"],
                                semantic="≈",
                            ),
                        ),
                    )
                ]
            )
        }
    }


def test_put():
    row = (
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "пѫть GH",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/028d18",
            "поутошьств\ue205ꙗ",
            "",
            "пѫтошьств\ue205\ue201",
        ]
        + [""] * 3
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00"]
        + ["1"] * 4
    )

    result = sl_sem.var.compile_usages(
        gr_sem, row, "ὁδοιπορία", Source("H"), SortedDict()
    )
    assert result == {
        "ὁδοιπορία": {
            (
                "шьств\ue205ꙗ пꙋт\ue205 H",
                "ὁδοιπορίας",
            ): SortedSet(
                [
                    Alignment(
                        Index("5/28d18"),
                        Usage(
                            "sl",
                            Source("H"),
                            "шьств\ue205ꙗ пꙋт\ue205 H",
                            ["пѫть", "шьств\ue205\ue201 пѫт\ue205"],
                            main_alt=Alternative("поутошьствꙗ", ["пѫтошьств"]),
                            var_alt={
                                Source("G"): Alternative(
                                    "шьст\ue205ꙗ пꙋт\ue205 G",
                                    ["пѫть", "шьст\ue205\ue201 пѫт\ue205"],
                                ),
                            },
                        ),
                        Usage(lang="gr", word="ὁδοιπορίας", lemmas=["ὁδοιπορία"]),
                    )
                ]
            )
        }
    }


def test_prichatnik():
    row = (
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 G пр\ue205\ue20dестн\ue205ц\ue205 H",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "",
            "05/28c21",
            "пр\ue205\ue20dьтьн\ue205ц\ue205",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
        ]
        + [""] * 2
        + ["ποιῆσαι", "ποιέω", "ποιέω κοινωνόν"]
        + [""] * 12
        + ["hl05:FFFCD5B4|hl11:FFFCD5B4"]
        + ["1"] * 4
    )
    result = sl_sem.var.compile_usages(gr_sem, row, "ποιέω", Source("GH"), SortedDict())
    assert result == {
        "ποιέω κοινωνόν → ποιέω": {
            (
                "пр\ue205\ue20dестн\ue205ц\ue205 H пр\ue205\ue20dестьн\ue205ц\ue205 G",
                "ποιῆσαι",
            ): SortedSet(
                [
                    Alignment(
                        idx=Index("5/28c21"),
                        orig=Usage(
                            "sl",
                            Source("GH"),
                            "пр\ue205\ue20dестн\ue205ц\ue205 H пр\ue205\ue20dестьн\ue205ц\ue205 G",
                            [
                                "пр\ue205\ue20dѧстьн\ue205къ",
                                "пр\ue205\ue20dѧстьн\ue205къ",
                            ],
                            main_alt=Alternative(
                                "пр\ue205\ue20dьтьн\ue205ц\ue205",
                                [
                                    "пр\ue205\ue20dьтьн\ue205къ",
                                    "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
                                ],
                            ),
                        ),
                        trans=Usage(
                            "gr",
                            word="ποιῆσαι",
                            lemmas=["ποιέω", "ποιέω κοινωνόν"],
                        ),
                    )
                ]
            )
        }
    }


def test_greh():
    row = (
        [""] * 4
        + ["05/17b12", "грѣхъм\ue205", "оубо ꙗко грѣ-", "грѣхъ"]
        + [""] * 3
        + ["υἱός", "# υἱός"]
        + [""] * 14
        + ["1"] * 4
    )
    result = sl_sem.compile_usages(gr_sem, row, "# υἱός", d=SortedDict())
    assert result == {
        "# υἱός": {
            ("грѣхъм\ue205", "υἱός"): SortedSet(
                [
                    Alignment(
                        idx=Index("5/17b12"),
                        orig=Usage(
                            lang="sl",
                            word="грѣхъм\ue205",
                            lemmas=["грѣхъ"],
                        ),
                        trans=Usage(
                            lang="gr",
                            word="υἱός",
                            lemmas=["# υἱός"],
                        ),
                    )
                ]
            )
        }
    }


def test_special_mulitword():
    row = (
        ["проꙁрѣвшоѡмоу G  проꙁрѣвшоумоу H", "проꙁьрѣт\ue205"]
        + [""] * 2
        + [
            "06/38b11",
            "\ue205сцѣленоумоу",
            "сповѣдат\ue205• нъ \ue205-",
            "\ue205цѣл\ue205т\ue205",
        ]
        + [""] * 3
        + ["τεθαραπευμένον", "# θεραπεύω"]
        + [""] * 14
        + ["1"] * 4
    )
    result = sl_sem.var.compile_usages(
        gr_sem, row, "# θεραπεύω", Source("GH"), SortedDict()
    )
    assert result == {
        "# θεραπεύω": {
            ("проꙁрѣвшоумоу H проꙁрѣвшоѡмоу G", "τεθαραπευμένον"): SortedSet(
                [
                    Alignment(
                        idx=Index("6/38b11"),
                        orig=Usage(
                            "sl",
                            Source("GH"),
                            "проꙁрѣвшоумоу H проꙁрѣвшоѡмоу G",
                            ["проꙁьрѣт\ue205"],
                            main_alt=Alternative(
                                "\ue205сцѣленоумоу", ["\ue205цѣл\ue205т\ue205"]
                            ),
                        ),
                        trans=Usage(
                            lang="gr",
                            word="τεθαραπευμένον",
                            lemmas=["# θεραπεύω"],
                        ),
                    )
                ]
            )
        }
    }
