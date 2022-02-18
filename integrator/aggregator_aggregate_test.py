from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import STYLE_COL
from address import Index
from model import Usage, Source, Alternative
from semantics import MainLangSemantics, VarLangSemantics
from aggregator import aggregate


def test_monogenis():
    # simplified semantics
    sl_sem = MainLangSemantics(
        "sl",
        5,
        [7],
        VarLangSemantics("sl", 0, [1], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        "gr",
        11,
        [12],
        VarLangSemantics("gr", 16, [17, 18], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

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

    result = SortedDict()
    result = aggregate([row], sl_sem, gr_sem, result)
    assert result == {
        "\ue201д\ue205но\ue20dѧдъ": {
            "μονογενής": {
                ("\ue201д\ue205но\ue20dедоу", "μονογενοῦς"): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                word="\ue201д\ue205но\ue20dедоу",
                            ),
                            lang="sl",
                            orig_alt=Alternative(
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
    }

    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "\ue201д\ue205нородъ": {
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
                            lang="sl",
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
        },
        "\ue205но\ue20dѧдъ": {
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
                            lang="sl",
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
        },
    }

    # semantics change from September 2021
    sl_sem = MainLangSemantics(
        "sl",
        5,
        [7, 8, 9, 10],
        VarLangSemantics("sl", 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        "gr",
        11,
        [12, 13, 14],
        VarLangSemantics("gr", 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

    rows = [
        [
            "\ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ",
        ]
        + [""] * 2
        + [
            "1/W168a34",
            "\ue201д\ue205но\ue20dедоу",
            "бѣ \ue205мѣт\ue205 \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ ",
        ]
        + [""] * 2
        + ["μονογενῆ", "μονογενής"]
        + [""] * 15
        + ["1"] * 4,
        [""] * 4
        + [
            "1/W168a28",
            "\ue201д\ue205но\ue20dедаго",
            "цⷭ҇ре \ue201д\ue205но\ue20dедаго ѡтрока ѡ\ue010\ue20dа•",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 14
        + ["1"] * 4,
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
        + ["1"] * 4,
        ["\ue201д\ue205но\ue20dеды WH Ø G", "\ue201д\ue205но\ue20dѧдъ"]
        + [""] * 2
        + [
            "1/5a4",
            "\ue205но\ue20dадꙑ\ue205",
            "нъ ꙗко б\ue010ъ• а \ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ ",
        ]
        + [""] * 3
        + ["μονογενὴς", "μονογενής"]
        + [""] * 14
        + ["1"] * 4,
        ["\ue201д\ue205но\ue20dедѣмь WH Ø G", "\ue201д\ue205но\ue20dѧдъ"]
        + [""] * 2
        + [
            "1/4c15",
            "\ue205но\ue20dадѣмь",
            "о \ue205но\ue20dадѣмь",
            "\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 14
        + ["1"] * 4,
    ]
    # result = aggregate(rows, sl_sem, gr_sem)
    # print(result)

    result = SortedDict()
    result = aggregate(rows, gr_sem, sl_sem, result)
    assert result == {
        "μονογενής": {
            "": {
                "": {
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
                                        bold=True,
                                        italic=True,
                                        word="μονογενοῦς",
                                    ),
                                    lang="gr",
                                    var=Source("H"),
                                    trans_alt=Alternative(
                                        main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                        var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
                                        main_word="\ue201д\ue205но\ue20dедоу",
                                        var_words={
                                            Source("G"): ("\ue205но\ue20dедаго G", 1)
                                        },
                                    ),
                                )
                            ]
                        )
                    },
                    "\ue201д\ue205но\ue20dѧдъ": {
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедаго"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="a",
                                        row=28,
                                        word="μονογενοῦς",
                                    ),
                                    lang="gr",
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедоу"): SortedSet(
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
                                        word="μονογενοῦς",
                                    ),
                                    lang="gr",
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
                        ),
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедѣмь WH"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=False,
                                        page=4,
                                        col="c",
                                        row=15,
                                        word="μονογενοῦς",
                                    ),
                                    lang="gr",
                                    var=Source("WH"),
                                    trans_alt=Alternative(
                                        main_lemma="\ue205но\ue20dѧдъ",
                                        main_word="\ue205но\ue20dадѣмь",
                                    ),
                                )
                            ]
                        ),
                        ("μονογενὴς", "\ue201д\ue205но\ue20dеды WH"): SortedSet(
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
                                    lang="gr",
                                    var=Source("WH"),
                                    trans_alt=Alternative(
                                        main_lemma="\ue205но\ue20dѧдъ ",
                                        main_word="\ue205но\ue20dадꙑ\ue205",
                                    ),
                                )
                            ]
                        ),
                    },
                    "\ue205но\ue20dѧдъ": {
                        ("μονογενοῦς", "\ue205но\ue20dадѣмь"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=False,
                                        page=4,
                                        col="c",
                                        row=15,
                                        word="μονογενοῦς",
                                    ),
                                    lang="gr",
                                    trans_alt=Alternative(
                                        var_lemmas={
                                            Source("WH"): "\ue201д\ue205но\ue20dѧдъ"
                                        },
                                        var_words={
                                            Source("WH"): (
                                                "\ue201д\ue205но\ue20dедѣмь WH",
                                                1,
                                            )
                                        },
                                    ),
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue205но\ue20dедаго G"): SortedSet(
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
                                        word="μονογενοῦς",
                                    ),
                                    lang="gr",
                                    var=Source("G"),
                                    trans_alt=Alternative(
                                        main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                        var_lemmas={Source("H"): "\ue201д\ue205нородъ"},
                                        main_word="\ue201д\ue205но\ue20dедоу",
                                        var_words={
                                            Source("H"): ("\ue201д\ue205нородоу H", 1)
                                        },
                                    ),
                                )
                            ]
                        ),
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
                                    lang="gr",
                                    trans_alt=Alternative(
                                        var_lemmas={
                                            Source("WH"): "\ue201д\ue205но\ue20dѧдъ"
                                        },
                                        var_words={
                                            Source("WH"): (
                                                "\ue201д\ue205но\ue20dеды WH",
                                                1,
                                            )
                                        },
                                    ),
                                )
                            ]
                        ),
                    },
                }
            }
        }
    }


def test_ipercliso():
    sl_sem = MainLangSemantics(
        "sl",
        5,
        [7, 8, 9, 10],
        VarLangSemantics("sl", 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        "gr",
        11,
        [12, 13, 14],
        VarLangSemantics("gr", 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
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
    result = SortedDict()
    result = aggregate(rows, gr_sem, sl_sem, result)
    assert result == {
        "ὑπερκλύζω": {
            "": {
                "": {
                    "прѣ\ue205сто\ue20d\ue205т\ue205": {
                        ("ὑπερκλύζων", "прѣ\ue205сто\ue20dе"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        word="ὑπερκλύζων",
                                    ),
                                    lang="gr",
                                    orig_alt=Alternative(
                                        var_lemmas={Source("C"): "ὑπερβλύω"},
                                        var_words={Source("C"): ("ὑπερβλύζων C", 1)},
                                    ),
                                )
                            ]
                        )
                    }
                }
            },
            "inf.": {
                "": {
                    "\ue205сто\ue20dен\ue205\ue201": {
                        ("ὑπερκλύσαι", "\ue205сто\ue20dен\ue205\ue205"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        word="ὑπερκλύσαι",
                                    ),
                                    lang="gr",
                                    orig_alt=Alternative(
                                        var_lemmas={Source("C"): "ὑπερβλύω"},
                                        var_words={Source("C"): ("ὑπερβλύσαι C", 1)},
                                    ),
                                )
                            ]
                        )
                    }
                }
            },
        }
    }

    result = SortedDict()
    result = aggregate(rows, gr_sem.var, sl_sem, result)
    assert result == {
        "ὑπερβλύω": {
            "": {
                "": {
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
                                    lang="gr",
                                    var=Source("C"),
                                    orig_alt=Alternative(
                                        main_lemma="ὑπερκλύζω",
                                        main_word="ὑπερκλύζων",
                                    ),
                                )
                            ]
                        )
                    }
                }
            },
            "inf.": {
                "": {
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
                                    lang="gr",
                                    var=Source("C"),
                                    orig_alt=Alternative(
                                        main_lemma="ὑπερκλύζω",
                                        main_word="ὑπερκλύσαι",
                                    ),
                                )
                            ]
                        )
                    }
                }
            },
        }
    }


def test_satvoriti():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    r1 = (
        ["+ \ue201сть GH", "сътвор\ue205т\ue205"]
        + [""] * 2
        + ["17/047a06", "сътвор\ue205лъ", "сътвор\ue205лъ", "сътвор\ue205т\ue205"]
        + [""] * 4
        + ["Ø"]
        + [""] * 13
        + ["hl05"]
    )
    r2 = (
        [
            "+ \ue201сть GH",
            "бꙑт\ue205",
            "",
            "gramm.",
            "17/47a06",
            "",
            "сътвор\ue205лъ",
            "om.",
        ]
        + [""] * 18
        + ["hl05|hl03"]
    )

    rows = [r1, r2]

    result = SortedDict()
    result = aggregate(rows, gr_sem.var, sl_sem, result)
    assert not result
    result = aggregate(rows, gr_sem.var, sl_sem.var, result)
    assert not result


def test_bozhii():
    sl_sem = MainLangSemantics(
        "sl",
        5,
        [7, 8, 9, 10],
        VarLangSemantics("sl", 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        "gr",
        11,
        [12, 13, 14],
        VarLangSemantics("gr", 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
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
    result = aggregate([r], sl_sem, gr_sem, result)
    assert result == {
        "богъ": {
            "Dat.": {
                "": {
                    "": {
                        "θεός Gen.": {
                            ("боꙁѣ", "Θεοῦ"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=1,
                                            alt=False,
                                            page=7,
                                            col="a",
                                            row=4,
                                            word="боꙁѣ",
                                        ),
                                        lang="sl",
                                        orig_alt=Alternative(
                                            var_lemmas={
                                                Source("WGH"): "бож\ue205\ue205"
                                            },
                                            var_words={
                                                Source("WGH"): (
                                                    "б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G",
                                                    1,
                                                )
                                            },
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        }
    }

    # TODO: merge bozhii
    result = SortedDict()
    result = aggregate([r], sl_sem.var, gr_sem, result)
    assert result == {
        "бож\ue205\ue205": {
            "": {
                "": {
                    "": {
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
                                        lang="sl",
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
                }
            }
        }
    }

    result = SortedDict()
    result = aggregate([r], gr_sem, sl_sem.var, result)
    assert result == {
        "θεός": {
            "Gen.": {
                "": {
                    "бож\ue205\ue205": {
                        (
                            "Θεοῦ",
                            "б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G",
                        ): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=False,
                                        page=7,
                                        col="a",
                                        row=4,
                                        word="Θεοῦ",
                                    ),
                                    lang="gr",
                                    var=Source("WGH"),
                                    trans_alt=Alternative(
                                        main_lemma="богъ",
                                        main_word="боꙁѣ",
                                    ),
                                )
                            ]
                        )
                    }
                }
            }
        }
    }

    rows = [
        ["оуслышат\ue205 GH", "ѹслꙑшат\ue205"]
        + [""] * 2
        + ["05/22b05", "слꙑшат\ue205", "ноу соущоу слꙑ-", "слꙑшат\ue205"]
        + [""] * 3
        + ["ἀκοῦσαι", "ἀκούω"]
        + [""] * 14
        + ["1"] * 4,
        ["оуслышат\ue205 GH", "ѹслꙑшат\ue205"]
        + [""] * 2
        + ["05/22b05₂", "послꙑшат\ue205", "ноу соущоу слꙑ-", "послꙑшат\ue205"]
        + [""] * 3
        + ["ἀκοῦσαι", "ἀκούω"]
        + [""] * 14
        + ["1", "2", "2", "1"],
    ]
    result = SortedDict()
    result = aggregate(rows, gr_sem, sl_sem, result)
    assert result == {
        "ἀκούω": {
            "": {
                "": {
                    "послꙑшат\ue205": {
                        ("ἀκοῦσαι", "послꙑшат\ue205"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=5,
                                        alt=False,
                                        page=22,
                                        col="b",
                                        row=5,
                                        ocnt=2,
                                        word="ἀκοῦσαι",
                                    ),
                                    lang="gr",
                                    trans_alt=Alternative(
                                        var_lemmas={Source("GH"): "ѹслꙑшат\ue205"},
                                        var_words={
                                            Source("GH"): ("оуслышат\ue205 GH", 2)
                                        },
                                    ),
                                )
                            ]
                        )
                    },
                    "слꙑшат\ue205": {
                        ("ἀκοῦσαι", "слꙑшат\ue205"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=5,
                                        alt=False,
                                        page=22,
                                        col="b",
                                        row=5,
                                        word="ἀκοῦσαι",
                                    ),
                                    lang="gr",
                                    trans_alt=Alternative(
                                        var_lemmas={Source("GH"): "ѹслꙑшат\ue205"},
                                        var_words={
                                            Source("GH"): ("оуслышат\ue205 GH", 1)
                                        },
                                    ),
                                )
                            ]
                        )
                    },
                    "ѹслꙑшат\ue205": {
                        ("ἀκοῦσαι", "оуслышат\ue205 GH"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=5,
                                        alt=False,
                                        page=22,
                                        col="b",
                                        row=5,
                                        word="ἀκοῦσαι",
                                    ),
                                    lang="gr",
                                    var=Source("GH"),
                                    trans_alt=Alternative(
                                        main_lemma="слꙑшат\ue205",
                                        main_word="слꙑшат\ue205",
                                    ),
                                ),
                                Usage(
                                    idx=Index(
                                        ch=5,
                                        alt=False,
                                        page=22,
                                        col="b",
                                        row=5,
                                        ocnt=2,
                                        tcnt=2,
                                        word="ἀκοῦσαι",
                                    ),
                                    lang="gr",
                                    var=Source("GH"),
                                    trans_alt=Alternative(
                                        main_lemma="послꙑшат\ue205",
                                        main_word="послꙑшат\ue205",
                                    ),
                                ),
                            ]
                        )
                    },
                }
            }
        }
    }

    result = SortedDict()
    result = aggregate(rows, gr_sem.var, sl_sem, result)
    assert result == {}

    result = SortedDict()
    result = aggregate(rows, sl_sem.var, gr_sem, result)
    assert result == {
        "ѹслꙑшат\ue205": {
            "": {
                "": {
                    "": {
                        "ἀκούω": {
                            ("оуслышат\ue205 GH", "ἀκοῦσαι"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=22,
                                            col="b",
                                            row=5,
                                            word="оуслышат\ue205 GH",
                                        ),
                                        lang="sl",
                                        var=Source("GH"),
                                        orig_alt=Alternative(
                                            main_lemma="слꙑшат\ue205",
                                            main_word="слꙑшат\ue205",
                                        ),
                                    ),
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=22,
                                            col="b",
                                            row=5,
                                            ocnt=2,
                                            tcnt=2,
                                            word="оуслышат\ue205 GH",
                                        ),
                                        lang="sl",
                                        var=Source("GH"),
                                        orig_alt=Alternative(
                                            main_lemma="послꙑшат\ue205",
                                            main_word="послꙑшат\ue205",
                                        ),
                                    ),
                                ]
                            )
                        }
                    }
                }
            }
        }
    }

    result = SortedDict()
    result = aggregate(rows, sl_sem, gr_sem, result)
    assert result == {
        "послꙑшат\ue205": {
            "": {
                "": {
                    "": {
                        "ἀκούω": {
                            ("послꙑшат\ue205", "ἀκοῦσαι"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=22,
                                            col="b",
                                            row=5,
                                            tcnt=2,
                                            word="послꙑшат\ue205",
                                        ),
                                        lang="sl",
                                        orig_alt=Alternative(
                                            var_lemmas={Source("GH"): "ѹслꙑшат\ue205"},
                                            var_words={
                                                Source("GH"): ("оуслышат\ue205 GH", 2)
                                            },
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
        "слꙑшат\ue205": {
            "": {
                "": {
                    "": {
                        "ἀκούω": {
                            ("слꙑшат\ue205", "ἀκοῦσαι"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=22,
                                            col="b",
                                            row=5,
                                            word="слꙑшат\ue205",
                                        ),
                                        lang="sl",
                                        orig_alt=Alternative(
                                            var_lemmas={Source("GH"): "ѹслꙑшат\ue205"},
                                            var_words={
                                                Source("GH"): ("оуслышат\ue205 GH", 1)
                                            },
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
    }


def test_velichanie():
    sl_sem = MainLangSemantics(
        "sl",
        5,
        [7, 8, 9, 10],
        VarLangSemantics("sl", 0, [1, 2, 3]),
    )
    gr_sem = MainLangSemantics(
        "gr",
        11,
        [12, 13, 14],
        VarLangSemantics("gr", 16, [17, 18, 19]),
    )

    rows = [
        ["вел\ue205\ue20dан\ue205е WGH", "вел\ue205\ue20dан\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["1"] * 4,
        ["невел\ue205\ue20d\ue205\ue201 WGH", "невел\ue205\ue20d\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19₂₂",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["2", "1", "1", "2"],
    ]

    result = SortedDict()
    gr_sem.cnt_col = STYLE_COL + 1
    gr_sem.var.cnt_col = STYLE_COL + 2
    sl_sem.var.cnt_col = STYLE_COL + 3
    sl_sem.cnt_col = STYLE_COL + 4
    result = aggregate(rows, gr_sem, sl_sem.var, result)
    assert result == {
        "ἄτυφος": {
            "": {
                "": {
                    "вел\ue205\ue20dан\ue205\ue201": {
                        ("ἄτυφον", "вел\ue205\ue20dан\ue205е WGH"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=5,
                                        alt=False,
                                        page=21,
                                        col="a",
                                        row=19,
                                        word="ἄτυφον",
                                    ),
                                    lang="gr",
                                    var=Source("WGH"),
                                    trans_alt=Alternative(
                                        main_lemma="невел\ue205\ue20dан\ue205\ue201",
                                        main_word="невел\ue205\ue20dан\ue205\ue201",
                                    ),
                                )
                            ]
                        )
                    },
                    "невел\ue205\ue20d\ue205\ue201": {
                        ("ἄτυφον", "невел\ue205\ue20d\ue205\ue201 WGH"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=5,
                                        alt=False,
                                        page=21,
                                        col="a",
                                        row=19,
                                        ocnt=2,
                                        word="ἄτυφον",
                                    ),
                                    lang="gr",
                                    var=Source("WGH"),
                                    trans_alt=Alternative(
                                        main_lemma="невел\ue205\ue20dан\ue205\ue201",
                                        main_word="невел\ue205\ue20dан\ue205\ue201",
                                        main_cnt=2,
                                    ),
                                )
                            ]
                        )
                    },
                }
            }
        }
    }

    rows = [
        ["вел\ue205\ue20dан\ue205е WGH", "вел\ue205\ue20dан\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["1"] * 4,
        ["невел\ue205\ue20d\ue205\ue201 WGH", "невел\ue205\ue20d\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19₂₂",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["1", "2", "2", "1"],
    ]
    result = SortedDict()
    sl_sem.var.cnt_col = STYLE_COL + 1
    sl_sem.cnt_col = STYLE_COL + 2
    gr_sem.cnt_col = STYLE_COL + 3
    gr_sem.var.cnt_col = STYLE_COL + 4
    result = aggregate(rows, sl_sem.var, gr_sem, result)
    assert result == {
        "вел\ue205\ue20dан\ue205\ue201": {
            "": {
                "": {
                    "": {
                        "ἄτυφος": {
                            ("вел\ue205\ue20dан\ue205е WGH", "ἄτυφον"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=21,
                                            col="a",
                                            row=19,
                                            word="вел\ue205\ue20dан\ue205е WGH",
                                        ),
                                        lang="sl",
                                        var=Source("WGH"),
                                        orig_alt=Alternative(
                                            main_lemma="невел\ue205\ue20dан\ue205\ue201",
                                            main_word="невел\ue205\ue20dан\ue205\ue201",
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
        "невел\ue205\ue20d\ue205\ue201": {
            "": {
                "": {
                    "": {
                        "ἄτυφος": {
                            ("невел\ue205\ue20d\ue205\ue201 WGH", "ἄτυφον"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=21,
                                            col="a",
                                            row=19,
                                            tcnt=2,
                                            word="невел\ue205\ue20d\ue205\ue201 WGH",
                                        ),
                                        lang="sl",
                                        var=Source("WGH"),
                                        orig_alt=Alternative(
                                            main_lemma="невел\ue205\ue20dан\ue205\ue201",
                                            main_word="невел\ue205\ue20dан\ue205\ue201",
                                            main_cnt=2,
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
    }
