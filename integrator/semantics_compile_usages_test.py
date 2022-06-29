"""Tests of LangSemantics.compile_usages"""

from sortedcontainers.sorteddict import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL
from model import Alternative, Index, Source, Usage, UsageContent
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

    d2 = SortedDict()
    d2 = gr_sem.compile_usages(sl_sem, row, d2, "παρά", "Instr.")
    # print(d2)
    assert d2 == {
        "Instr.": {
            ("παρὰ", "Instr."): SortedSet(
                [
                    Usage(
                        Index("1/W168a19"),
                        UsageContent(
                            TO_LANG,
                            word="παρὰ",
                            lemmas=["παρά", "παρά + Dat."],
                        ),
                        UsageContent("sl", word="Instr.", lemmas=["Instr."]),
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
    d3 = gr_sem.var.compile_usages(sl_sem, row, d3, "παρά", "ѹ", Source("C"))
    assert d3 == {
        "ѹ": {
            ("παρ’ C", "оу"): SortedSet(
                [
                    Usage(
                        Index("1/7d1"),
                        UsageContent(
                            "gr",
                            Source("C"),
                            word="παρ’ C",
                            lemmas=["παρά", "παρά + Acc."],
                        ),
                        UsageContent(
                            "sl",
                            alt=Alternative(
                                var_lemmas={Source("WGH"): "въ + Loc."},
                                var_words={Source("WGH"): ("вь WGH", 1)},
                            ),
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
        sl_sem, rows[0], d2, "ὑπερβλύω", "\ue205сто\ue20dен\ue205\ue201", Source("C")
    )
    d2 = gr_sem.var.compile_usages(
        sl_sem, rows[1], d2, "ὑπερβλύω", "прѣ\ue205сто\ue20d\ue205т\ue205", Source("C")
    )
    assert d2 == {
        "прѣ\ue205сто\ue20d\ue205т\ue205": {
            ("ὑπερβλύζων C", "прѣ\ue205сто\ue20dе"): SortedSet(
                [
                    Usage(
                        Index("1/W168c17"),
                        UsageContent(
                            "gr",
                            Source("C"),
                            Alternative(
                                main_lemma="ὑπερκλύζω",
                                main_word="ὑπερκλύζων",
                            ),
                            "ὑπερβλύζων C",
                            ["ὑπερβλύω"],
                        ),
                        UsageContent(
                            "sl",
                            word="прѣ\ue205сто\ue20dе",
                            lemmas=["прѣ\ue205сто\ue20d\ue205т\ue205"],
                        ),
                    )
                ]
            )
        },
        "\ue205сто\ue20dен\ue205\ue201": {
            ("ὑπερβλύσαι C", "\ue205сто\ue20dен\ue205\ue205"): SortedSet(
                [
                    Usage(
                        Index("1/W168c17"),
                        UsageContent(
                            "gr",
                            Source("C"),
                            Alternative(
                                main_lemma="ὑπερκλύζω",
                                main_word="ὑπερκλύσαι",
                            ),
                            "ὑπερβλύσαι C",
                            ["ὑπερβλύω", "inf."],
                        ),
                        UsageContent(
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

    d1 = SortedDict()
    d1 = sl_sem.compile_usages(gr_sem, row, d1, "вѣроват_", "πιστεύω")
    assert d1 == {
        "πιστεύω": {
            ("вѣроують", "πιστεύσωσι"): SortedSet(
                [
                    Usage(
                        Index("1/7b19"),
                        UsageContent(
                            "sl",
                            alt=Alternative(
                                var_lemmas={Source("GH"): "вѣрѫ ѩт_"},
                                var_words={Source("GH"): ("вѣроу GH", 1)},
                            ),
                            word="вѣроують",
                            lemmas=["вѣроват_"],
                        ),
                        UsageContent("gr", word="πιστεύσωσι", lemmas=["πιστεύω"]),
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
                        Index("1/7b19"),
                        UsageContent(
                            "gr",
                            word="πιστεύσωσι",
                            lemmas=["πιστεύω"],
                        ),
                        UsageContent(
                            "sl",
                            alt=Alternative(
                                var_lemmas={Source("GH"): "вѣрѫ ѩт_"},
                                var_words={Source("GH"): ("вѣроу GH", 1)},
                            ),
                            word="вѣроують",
                            lemmas=["вѣроват_"],
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
                        Index("1/W168c7"),
                        UsageContent("sl", word="мене", lemmas=["аꙁъ"]),
                        UsageContent("gr", Source("C"), word="με C", lemmas=["ἐγώ"]),
                    )
                ]
            )
        }
    }
    d4 = SortedDict()
    d4 = gr_sem.var.compile_usages(sl_sem, row, d4, "ἐγώ", "аꙁъ", Source("C"))
    assert d4 == {
        "аꙁъ": {
            ("με C", "мене"): SortedSet(
                [
                    Usage(
                        Index("1/W168c7"),
                        UsageContent(
                            TO_LANG, var=Source("C"), word="με C", lemmas=["ἐγώ"]
                        ),
                        UsageContent(lang="sl", word="мене", lemmas=["аꙁъ"]),
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

    d0 = SortedDict()
    d0 = sl_sem.compile_usages(gr_sem, row, d0, "\ue205но\ue20dѧдъ", "μονογενής")
    assert d0 == {
        "μονογενής": {
            ("\ue205но\ue20dадꙑ\ue205", "μονογενὴς"): SortedSet(
                [
                    Usage(
                        Index("1/5a4"),
                        UsageContent(
                            FROM_LANG,
                            alt=Alternative(
                                var_lemmas={Source("WH"): "\ue201д\ue205но\ue20dѧдъ"},
                                var_words={
                                    Source("WH"): ("\ue201д\ue205но\ue20dеды WH", 1)
                                },
                            ),
                            word="\ue205но\ue20dадꙑ\ue205",
                            lemmas=["\ue205но\ue20dѧдъ"],
                        ),
                        UsageContent(lang="gr", word="μονογενὴς", lemmas=["μονογενής"]),
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
                        Index("1/5a4"),
                        UsageContent(TO_LANG, word="μονογενὴς", lemmas=["μονογενής"]),
                        UsageContent(
                            FROM_LANG,
                            alt=Alternative(
                                var_lemmas={Source("WH"): "\ue201д\ue205но\ue20dѧдъ"},
                                var_words={
                                    Source("WH"): ("\ue201д\ue205но\ue20dеды WH", 1)
                                },
                            ),
                            word="\ue205но\ue20dадꙑ\ue205",
                            lemmas=["\ue205но\ue20dѧдъ"],
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

    d1 = SortedDict()
    d1 = sl_sem.var.compile_usages(
        gr_sem, row, d1, "\ue205но\ue20dѧдъ", "μονογενής", Source("G")
    )
    assert d1 == {
        "μονογενής": {
            ("\ue205но\ue20dедаго G", "μονογενοῦς"): SortedSet(
                [
                    Usage(
                        Index("1/W168a25"),
                        UsageContent(
                            "sl",
                            var=Source("G"),
                            alt=Alternative(
                                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                var_lemmas={Source("H"): "\ue201д\ue205нородъ"},
                                main_word="\ue201д\ue205но\ue20dедоу",
                                var_words={Source("H"): ("\ue201д\ue205нородоу H", 1)},
                            ),
                            word="\ue205но\ue20dедаго G",
                            lemmas=["\ue205но\ue20dѧдъ"],
                        ),
                        UsageContent(
                            lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]
                        ),
                        bold=True,
                        italic=True,
                    )
                ]
            ),
        }
    }

    d2 = SortedDict()
    d2 = sl_sem.var.compile_usages(
        gr_sem, row, d2, "\ue201д\ue205нородъ", "μονογενής", Source("H")
    )
    assert d2 == {
        "μονογενής": {
            ("\ue201д\ue205нородоу H", "μονογενοῦς"): SortedSet(
                [
                    Usage(
                        Index("1/W168a25"),
                        UsageContent(
                            "sl",
                            var=Source("H"),
                            alt=Alternative(
                                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
                                main_word="\ue201д\ue205но\ue20dедоу",
                                var_words={Source("G"): ("\ue205но\ue20dедаго G", 1)},
                            ),
                            word="\ue201д\ue205нородоу H",
                            lemmas=["\ue201д\ue205нородъ"],
                        ),
                        UsageContent(
                            lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]
                        ),
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

    d = SortedDict()
    d = sl_sem.var.compile_usages(
        gr_sem, row, d, "\ue205но\ue20dѧдъ", "μονογενής", Source("G")
    )
    # print(d)
    assert d == {
        "μονογενής": {
            ("\ue205но\ue20dедаго G", "μονογενοῦς"): SortedSet(
                [
                    Usage(
                        Index("1/W168a25"),
                        UsageContent(
                            "sl",
                            var=Source("G"),
                            alt=Alternative(
                                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                var_lemmas={Source("H"): "\ue201д\ue205нородъ"},
                                main_word="\ue201д\ue205но\ue20dедоу",
                                var_words={Source("H"): ("\ue201д\ue205нородоу H", 1)},
                            ),
                            word="\ue205но\ue20dедаго G",
                            lemmas=["\ue205но\ue20dѧдъ"],
                        ),
                        UsageContent(
                            lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]
                        ),
                    )
                ]
            ),
        }
    }

    d = SortedDict()
    d = sl_sem.var.compile_usages(
        gr_sem, row, d, "\ue201д\ue205нородъ", "μονογενής", Source("H")
    )
    assert d == {
        "μονογενής": {
            ("\ue201д\ue205нородоу H", "μονογενοῦς"): SortedSet(
                [
                    Usage(
                        Index("1/W168a25"),
                        UsageContent(
                            "sl",
                            Source("H"),
                            Alternative(
                                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
                                main_word="\ue201д\ue205но\ue20dедоу",
                                var_words={Source("G"): ("\ue205но\ue20dедаго G", 1)},
                            ),
                            word="\ue201д\ue205нородоу H",
                            lemmas=["\ue201д\ue205нородъ"],
                        ),
                        UsageContent(
                            lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]
                        ),
                    )
                ]
            ),
        }
    }

    d = SortedDict()
    d = gr_sem.compile_usages(sl_sem, row, d, "μονογενής", "\ue201д\ue205но\ue20dѧдъ")
    assert d == {
        "\ue201д\ue205но\ue20dѧдъ": {
            ("μονογενοῦς", "\ue201д\ue205но\ue20dедоу"): SortedSet(
                [
                    Usage(
                        Index("1/W168a25"),
                        UsageContent(TO_LANG, word="μονογενοῦς", lemmas=["μονογενής"]),
                        UsageContent(
                            FROM_LANG,
                            alt=Alternative(
                                var_lemmas={
                                    Source("H"): "\ue201д\ue205нородъ",
                                    Source("G"): "\ue205но\ue20dѧдъ",
                                },
                                var_words={
                                    Source("H"): ("\ue201д\ue205нородоу H", 1),
                                    Source("G"): ("\ue205но\ue20dедаго G", 1),
                                },
                            ),
                            word="\ue201д\ue205но\ue20dедоу",
                            lemmas=["\ue201д\ue205но\ue20dѧдъ"],
                        ),
                    )
                ]
            )
        }
    }

    d = SortedDict()
    d = gr_sem.compile_usages(sl_sem.var, row, d, "μονογενής", "\ue201д\ue205нородъ")
    assert d == {
        "\ue201д\ue205нородъ": {
            ("μονογενοῦς", "\ue201д\ue205нородоу H"): SortedSet(
                [
                    Usage(
                        Index("1/W168a25"),
                        UsageContent(
                            "gr",
                            word="μονογενοῦς",
                            lemmas=["μονογενής"],
                        ),
                        UsageContent(
                            "sl",
                            var=Source("H"),
                            alt=Alternative(
                                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
                                main_word="\ue201д\ue205но\ue20dедоу",
                                var_words={Source("G"): ("\ue205но\ue20dедаго G", 1)},
                            ),
                            word="\ue201д\ue205нородоу H",
                            lemmas=["\ue201д\ue205нородъ"],
                        ),
                    )
                ]
            )
        }
    }

    d = SortedDict()
    d = gr_sem.compile_usages(sl_sem.var, row, d, "μονογενής", "\ue205но\ue20dѧдъ")
    assert d == {
        "\ue205но\ue20dѧдъ": {
            ("μονογενοῦς", "\ue205но\ue20dедаго G"): SortedSet(
                [
                    Usage(
                        Index("1/W168a25"),
                        UsageContent(
                            "gr",
                            word="μονογενοῦς",
                            lemmas=["μονογενής"],
                        ),
                        UsageContent(
                            "sl",
                            Source("G"),
                            alt=Alternative(
                                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                var_lemmas={Source("H"): "\ue201д\ue205нородъ"},
                                main_word="\ue201д\ue205но\ue20dедоу",
                                var_words={Source("H"): ("\ue201д\ue205нородоу H", 1)},
                            ),
                            word="\ue205но\ue20dедаго G",
                            lemmas=["\ue205но\ue20dѧдъ"],
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

    result = SortedDict()
    result = sl_sem.var.compile_usages(
        gr_sem, r, result, "бож\ue205\ue205", "θεός", Source("H")
    )
    assert result == {
        "θεός Gen.": {
            ("б\ue010жї\ue205 H", "Θεοῦ",): SortedSet(
                [
                    Usage(
                        Index("1/7a4"),
                        UsageContent(
                            FROM_LANG,
                            var=Source("H"),
                            alt=Alternative(
                                main_lemma="богъ",
                                main_word="боꙁѣ",
                            ),
                            word="б\ue010жї\ue205 H",
                            lemmas=["бож\ue205\ue205"],
                        ),
                        UsageContent(lang="gr", word="Θεοῦ", lemmas=["θεός", "Gen."]),
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
    result = SortedDict()
    result = gr_sem.var.compile_usages(
        sl_sem, row, result, "ἄρτος", "хлѣбъ", Source("Ch")
    )
    assert result == {
        "хлѣбъ": {
            ("ἄρτους Ch", "хлѣбꙑ•"): SortedSet(
                [
                    Usage(
                        Index("16/80a8"),
                        UsageContent(
                            "gr",
                            var=Source("Ch"),
                            alt=Alternative(
                                main_lemma="om.",
                                main_word="om.",
                            ),
                            word="ἄρτους Ch",
                            lemmas=["ἄρτος"],
                        ),
                        UsageContent(lang="sl", word="хлѣбꙑ•", lemmas=["хлѣбъ"]),
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
    result = SortedDict()
    result = sl_sem.var.compile_usages(gr_sem, row, result, "бꙑт", "Ø", Source("GH"))
    assert result == {
        "Ø": {
            ("\ue201сть GH", "Ø"): SortedSet(
                [
                    Usage(
                        Index("7/47a6"),
                        UsageContent(
                            "sl",
                            Source("GH"),
                            Alternative(
                                main_lemma="om.",
                                main_word="om.",
                            ),
                            "\ue201сть GH",
                            ["бꙑт\ue205", "", "gramm."],
                        ),
                        UsageContent(lang="gr", word="Ø", lemmas=["Ø"]),
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

    result = SortedDict()
    result = gr_sem.compile_usages(sl_sem.var, row, result, "προβαίνω", "ходъ")
    assert result == {
        "ходомь спѣт\ue205 → ходъ": {
            ("προβαίνοντες", "хⷪ҇домь WG"): SortedSet(
                [
                    Usage(
                        Index("14/72d18"),
                        UsageContent("gr", word="προβαίνοντες", lemmas=["προβαίνω"]),
                        UsageContent(
                            "sl",
                            Source("WG"),
                            alt=Alternative(
                                main_lemma="≈ ход\ue205т\ue205 спѣѭще",
                                main_word="ход\ue205мъ",
                            ),
                            word="хⷪ҇домь WG",
                            lemmas=["ходъ", "ходомь спѣт\ue205"],
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

    result = SortedDict()
    result = sl_sem.var.compile_usages(
        gr_sem, row, result, "пѫть", "ὁδοιπορία", Source("H")
    )
    assert result == {
        "ὁδοιπορία": {
            ("шьств\ue205ꙗ пꙋт\ue205 H", "ὁδοιπορίας",): SortedSet(
                [
                    Usage(
                        Index("5/28d18"),
                        UsageContent(
                            "sl",
                            Source("H"),
                            alt=Alternative(
                                main_lemma="пѫтошьств",
                                var_lemmas={
                                    Source("G"): "шьст\ue205\ue201 пѫт\ue205",
                                },
                                main_word="поутошьствꙗ",
                                var_words={
                                    Source("G"): ("шьст\ue205ꙗ пꙋт\ue205 G", 1),
                                },
                            ),
                            word="шьств\ue205ꙗ пꙋт\ue205 H",
                            lemmas=["пѫть", "шьств\ue205\ue201 пѫт\ue205"],
                        ),
                        UsageContent(
                            lang="gr", word="ὁδοιπορίας", lemmas=["ὁδοιπορία"]
                        ),
                    )
                ]
            )
        }
    }
