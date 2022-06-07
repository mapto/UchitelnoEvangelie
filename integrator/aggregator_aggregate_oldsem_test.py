from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import FROM_LANG, TO_LANG
from config import FROM_LANG
from const import IDX_COL, STYLE_COL

from model import Index, Usage, Source, Alternative
from semantics import MainLangSemantics, VarLangSemantics
from aggregator import aggregate

# semantics change from September 2021
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


def test_monogenis():
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
                                        lemma="μονογενής",
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
                                        lemma="μονογενής",
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
                                        lemma="μονογενής",
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
                                        lemma="μονογενής",
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
                                        lemma="μονογενής",
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
                                        lemma="μονογενής",
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
                                        lemma="μονογενής",
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
                                        lemma="μονογενής",
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
                                        lemma="ὑπερκλύζω",
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
                                        lemma="ὑπερκλύζω",
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
                                        lemma="ὑπερβλύω",
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
                                        lemma="ὑπερβλύω",
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
                                            lemma="богъ",
                                        ),
                                        lang=FROM_LANG,
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
                                            lemma="бож\ue205\ue205",
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
                                        lemma="θεός",
                                    ),
                                    lang=TO_LANG,
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
                                        lemma="ἀκούω",
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
                                        lemma="ἀκούω",
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
                                        lemma="ἀκούω",
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
                                        lemma="ἀκούω",
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
                                            lemma="ѹслꙑшат\ue205",
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
                                            lemma="ѹслꙑшат\ue205",
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
                                            lemma="послꙑшат\ue205",
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
                                            lemma="слꙑшат\ue205",
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
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["2", "1"] * 2,
    ]

    result = SortedDict()
    result = aggregate(rows, gr_sem, sl_sem, result)
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
                                        lemma="ἄτυφος",
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
                    "невел\ue205\ue20dан\ue205\ue201": {
                        ("ἄτυφον", "невел\ue205\ue20dан\ue205\ue201"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=5,
                                        alt=False,
                                        page=21,
                                        col="a",
                                        row=19,
                                        word="ἄτυφον",
                                        lemma="ἄτυφος",
                                    ),
                                    lang="gr",
                                    trans_alt=Alternative(
                                        var_lemmas={
                                            Source(
                                                "WGH"
                                            ): "вел\ue205\ue20dан\ue205\ue201"
                                        },
                                        var_words={
                                            Source("WGH"): (
                                                "вел\ue205\ue20dан\ue205е WGH",
                                                1,
                                            )
                                        },
                                    ),
                                ),
                                Usage(
                                    idx=Index(
                                        ch=5,
                                        alt=False,
                                        page=21,
                                        col="a",
                                        row=19,
                                        ocnt=2,
                                        tcnt=2,
                                        word="ἄτυφον",
                                        lemma="ἄτυφος",
                                    ),
                                    lang="gr",
                                    trans_alt=Alternative(
                                        var_lemmas={
                                            Source(
                                                "WGH"
                                            ): "невел\ue205\ue20d\ue205\ue201"
                                        },
                                        var_words={
                                            Source("WGH"): (
                                                "невел\ue205\ue20d\ue205\ue201 WGH",
                                                1,
                                            )
                                        },
                                    ),
                                ),
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
                                        lemma="ἄτυφος",
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

    result = SortedDict()
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
                                        lemma="ἄτυφος",
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
                                        lemma="ἄτυφος",
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

    result = SortedDict()
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
                                            lemma="вел\ue205\ue20dан\ue205\ue201",
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
                                            lemma="невел\ue205\ue20d\ue205\ue201",
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


def test_puteshestive():
    rows = [
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст\ue205\ue201 G / шьств\ue205\ue201 H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/028d18",
            "поутошьств\ue205ꙗ",
            "поутошьств\ue205-",
            "пѫтошьств\ue205\ue201",
        ]
        + [""] * 3
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00"]
        + ["1"] * 4,
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
        + ["1"] * 4,
    ]

    result = SortedDict()
    result = aggregate(rows, sl_sem, gr_sem, result)
    assert result == {
        "пѫтошьств\ue205\ue201": {
            "": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            ("поутошьств\ue205ꙗ", "ὁδοιπορίας"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="d",
                                            row=18,
                                            word="поутошьств\ue205ꙗ",
                                            lemma="пѫтошьств\ue205\ue201",
                                        ),
                                        lang="sl",
                                        orig_alt=Alternative(
                                            var_lemmas={
                                                Source(
                                                    "H"
                                                ): "шьств\ue205\ue201 пѫт\ue205",
                                                Source(
                                                    "G"
                                                ): "шьст\ue205\ue201 пѫт\ue205",
                                            },
                                            var_words={
                                                Source("H"): (
                                                    "шьств\ue205ꙗ пꙋт\ue205 H",
                                                    1,
                                                ),
                                                Source("G"): (
                                                    "шьст\ue205ꙗ пꙋт\ue205 G",
                                                    1,
                                                ),
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

    result = SortedDict()
    result = aggregate(rows, sl_sem.var, gr_sem, result)
    assert result == {
        "пѫть": {
            "шьств\ue205\ue201 пѫт\ue205": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            (
                                "шьств\ue205ꙗ пꙋт\ue205 H шьст\ue205ꙗ пꙋт\ue205 G",
                                "ὁδοιπορίας",
                            ): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="d",
                                            row=18,
                                            word="шьств\ue205ꙗ пꙋт\ue205 H шьст\ue205ꙗ пꙋт\ue205 G",
                                            lemma="пѫть",
                                        ),
                                        lang="sl",
                                        var=Source("GH"),
                                        orig_alt=Alternative(
                                            main_lemma="пѫтошьств\ue205\ue201",
                                            var_lemmas={
                                                Source(
                                                    "H"
                                                ): "шьств\ue205\ue201 пѫт\ue205",
                                                Source(
                                                    "G"
                                                ): "шьст\ue205\ue201 пѫт\ue205",
                                            },
                                            main_word="поутошьств\ue205ꙗ",
                                            var_words={
                                                Source("G"): (
                                                    "шьст\ue205ꙗ пꙋт\ue205 G",
                                                    1,
                                                ),
                                                Source("H"): (
                                                    "шьств\ue205ꙗ пꙋт\ue205 H",
                                                    1,
                                                ),
                                            },
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            },
            "шьст\ue205\ue201 пѫт\ue205": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            (
                                "шьств\ue205ꙗ пꙋт\ue205 H шьст\ue205ꙗ пꙋт\ue205 G",
                                "ὁδοιπορίας",
                            ): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="d",
                                            row=18,
                                            word="шьств\ue205ꙗ пꙋт\ue205 H шьст\ue205ꙗ пꙋт\ue205 G",
                                            lemma="пѫть",
                                        ),
                                        lang="sl",
                                        var=Source("GH"),
                                        orig_alt=Alternative(
                                            main_lemma="пѫтошьств\ue205\ue201",
                                            var_lemmas={
                                                Source(
                                                    "H"
                                                ): "шьств\ue205\ue201 пѫт\ue205",
                                                Source(
                                                    "G"
                                                ): "шьст\ue205\ue201 пѫт\ue205",
                                            },
                                            main_word="поутошьств\ue205ꙗ",
                                            var_words={
                                                Source("G"): (
                                                    "шьст\ue205ꙗ пꙋт\ue205 G",
                                                    1,
                                                ),
                                                Source("H"): (
                                                    "шьств\ue205ꙗ пꙋт\ue205 H",
                                                    1,
                                                ),
                                            },
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            },
        },
        "шьств\ue205\ue201": {
            "шьств\ue205\ue201 пѫт\ue205": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            ("шьств\ue205ꙗ пꙋт\ue205 H", "ὁδοιπορίας"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="d",
                                            row=18,
                                            word="шьств\ue205ꙗ пꙋт\ue205 H",
                                            lemma="шьств\ue205\ue201",
                                        ),
                                        lang="sl",
                                        var=Source("H"),
                                        orig_alt=Alternative(
                                            main_lemma="пѫтошьств\ue205\ue201",
                                            var_lemmas={
                                                Source(
                                                    "G"
                                                ): "шьст\ue205\ue201 пѫт\ue205"
                                            },
                                            main_word="поутошьств\ue205ꙗ",
                                            var_words={
                                                Source("G"): (
                                                    "шьст\ue205ꙗ пꙋт\ue205 G",
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
        },
        "шьст\ue205\ue201": {
            "шьст\ue205\ue201 пѫт\ue205": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            ("шьст\ue205ꙗ пꙋт\ue205 G", "ὁδοιπορίας"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="d",
                                            row=18,
                                            word="шьст\ue205ꙗ пꙋт\ue205 G",
                                            lemma="шьст\ue205\ue201",
                                        ),
                                        lang="sl",
                                        var=Source("G"),
                                        orig_alt=Alternative(
                                            main_lemma="пѫтошьств\ue205\ue201",
                                            var_lemmas={
                                                Source(
                                                    "H"
                                                ): "шьств\ue205\ue201 пѫт\ue205"
                                            },
                                            main_word="поутошьств\ue205ꙗ",
                                            var_words={
                                                Source("H"): (
                                                    "шьств\ue205ꙗ пꙋт\ue205 H",
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
        },
    }


def test_missing_gr_main():
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
    result = aggregate([row], gr_sem.var, sl_sem, result)
    assert result == {
        "ἄρτος": {
            "": {
                "": {
                    "хлѣбъ": {
                        ("ἄρτους Ch", "хлѣбꙑ•"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=16,
                                        alt=False,
                                        page=80,
                                        col="a",
                                        row=8,
                                        word="ἄρτους Ch",
                                        lemma="ἄρτος",
                                    ),
                                    lang="gr",
                                    var=Source("Ch"),
                                    orig_alt=Alternative(
                                        main_lemma="om.",
                                        main_word="om.",
                                    ),
                                )
                            ]
                        )
                    }
                }
            }
        }
    }


def test_v_loc():
    row = (
        [
            "вь WGH",
            "въ",
            "въ + Loc.",
            "",
            "1/7d1",
            "оу",
            "оу насъ",
            "ѹ praep.",
            "оу + Gen.",
        ]
        + [""] * 2
        + ["om."]
        + [""] * 4
        + ["παρ’", "παρά", "παρά + Acc."]
        + [""] * 8
        + ["1"] * 4
    )
    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "въ": {
            "въ + Loc.": {
                "": {
                    "": {
                        "παρά + Acc. → παρά": {
                            ("вь WGH", "παρ’ C"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=1,
                                            alt=False,
                                            page=7,
                                            col="d",
                                            row=1,
                                            word="вь WGH",
                                            lemma="въ",
                                        ),
                                        lang="sl",
                                        var=Source("WHGC"),
                                        orig_alt=Alternative(
                                            main_lemma="оу + Gen.",
                                            main_word="оу",
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


def test_hodom_spiti():
    # TODO: verify that this is the correct input for main sl_sem
    rows = [
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
        + ["1"] * 4,
        ["спѣюще WG с пѣн\ue205\ue201мь H"]
        + ["", "ходомь спѣт\ue205 WG", ""]
        + ["14/72d19", "спѣюще•", "д\ue205мъ спѣюще•", "спѣт\ue205"]
        + [""] * 18
        + ["hl05|hl00"]
        + ["1"] * 4,
    ]

    result = SortedDict()
    result = aggregate(rows, sl_sem, gr_sem, result)
    assert result == {
        "ход\ue205т\ue205": {
            "≈ ход\ue205т\ue205 спѣѭще": {
                "": {
                    "": {
                        "προβαίνω": {
                            ("ход\ue205мъ", "προβαίνοντες"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=14,
                                            alt=False,
                                            page=72,
                                            col="d",
                                            row=18,
                                            word="ход\ue205мъ",
                                            lemma="ход\ue205т\ue205",
                                        ),
                                        lang="sl",
                                        orig_alt=Alternative(
                                            var_lemmas={
                                                Source("WG"): "ходомь спѣт\ue205"
                                            },
                                            var_words={Source("WG"): ("хⷪ҇домь WG", 1)},
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


def test_agg_lemma_hodom_spiti():
    # TODO: verify inputs for sl_sems, need to see hodom spiti as a sublemma for spiti
    row_main = [
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "себе• по поут\ue205 хо-",
            "ход\ue205т\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
        ]
        + [""] * 2
        + ["προβαίνοντες", "προβαίνω"]
        + [""] * 13
        + ["hl05"]
        + ["1"] * 4,
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "д\ue205мъ спѣюще•",
            "спѣт\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
        ]
        + [""] * 2
        + ["προβαίνοντες", "προβαίνω"]
        + [""] * 13
        + ["hl05"]
        + ["1"] * 4,
    ]

    row_var = [
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "себе• по поут\ue205 хо-",
            "ход\ue205т\ue205 спѣт\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
            "",
            "",
            "προβαίνοντες",
            "προβαίνω",
        ]
        + [""] * 13
        + ["hl05"]
        + ["1"] * 4,
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "д\ue205мъ спѣюще•",
            "ход\ue205т\ue205 спѣт\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
            "",
            "",
            "προβαίνοντες",
            "προβαίνω",
        ]
        + [""] * 13
        + ["hl05"]
        + ["1"] * 4,
    ]

    result = SortedDict()
    aggregate(row_main, sl_sem, gr_sem, result)
    aggregate(row_var, sl_sem.var, gr_sem, result)
    assert result == {
        "спѣт\ue205": {
            "≈ ход\ue205т\ue205 спѣѭще": {
                "": {
                    "": {
                        "προβαίνω": {
                            ("ход\ue205мъ спѣюще•", "προβαίνοντες"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=14,
                                            alt=False,
                                            page=72,
                                            col="d",
                                            row=18,
                                            end=Index(
                                                ch=14,
                                                alt=False,
                                                page=72,
                                                col="d",
                                                row=19,
                                                word="ход\ue205мъ спѣюще•",
                                                lemma="спѣт\ue205",
                                            ),
                                            word="ход\ue205мъ спѣюще•",
                                            lemma="спѣт\ue205",
                                        ),
                                        lang="sl",
                                        orig_alt=Alternative(
                                            var_lemmas={
                                                Source("WG"): "ходомь спѣт\ue205"
                                            },
                                            var_words={
                                                Source("WG"): ("хⷪ҇домь спѣюще WG", 1)
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
        "ходъ": {
            "ходомь спѣт\ue205": {
                "": {
                    "": {
                        "προβαίνω": {
                            ("хⷪ҇домь спѣюще WG", "προβαίνοντες"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=14,
                                            alt=False,
                                            page=72,
                                            col="d",
                                            row=18,
                                            end=Index(
                                                ch=14,
                                                alt=False,
                                                page=72,
                                                col="d",
                                                row=19,
                                                word="хⷪ҇домь спѣюще WG",
                                                lemma="ходъ",
                                            ),
                                            word="хⷪ҇домь спѣюще WG",
                                            lemma="ходъ",
                                        ),
                                        lang="sl",
                                        var=Source("WG"),
                                        orig_alt=Alternative(
                                            main_lemma="≈ ход\ue205т\ue205 спѣѭще",
                                            main_word="ход\ue205мъ спѣюще•",
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
        "ход\ue205т\ue205": {
            "≈ ход\ue205т\ue205 спѣѭще": {
                "": {
                    "": {
                        "προβαίνω": {
                            ("ход\ue205мъ спѣюще•", "προβαίνοντες"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=14,
                                            alt=False,
                                            page=72,
                                            col="d",
                                            row=18,
                                            end=Index(
                                                ch=14,
                                                alt=False,
                                                page=72,
                                                col="d",
                                                row=19,
                                                word="ход\ue205мъ спѣюще•",
                                                lemma="ход\ue205т\ue205",
                                            ),
                                            word="ход\ue205мъ спѣюще•",
                                            lemma="ход\ue205т\ue205",
                                        ),
                                        lang="sl",
                                        orig_alt=Alternative(
                                            var_lemmas={
                                                Source("WG"): "ходомь спѣт\ue205"
                                            },
                                            var_words={
                                                Source("WG"): ("хⷪ҇домь спѣюще WG", 1)
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
