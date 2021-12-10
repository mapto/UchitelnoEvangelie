from sortedcontainers import SortedDict, SortedSet  # type: ignore

from model import Index, Usage
from semantics import MainLangSemantics, VarLangSemantics
from aggregator import aggregate


def test_aggregate_monogenis():
    # simplified semantics
    sl_sem = MainLangSemantics("sl", 5, [7], VarLangSemantics("sl", 0, [1]))
    gr_sem = MainLangSemantics("gr", 11, [12], VarLangSemantics("gr", 16, [17, 18]))

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
                            orig_alt_var={
                                "H": "\ue201д\ue205нородъ",
                                "G": "\ue205но\ue20dѧдъ",
                            },
                        )
                    ]
                )
            }
        },
    }

    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "\ue201д\ue205нородъ": {
            "μονογενής": {
                ("\ue201д\ue205нородоу", "μονογενοῦς"): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                var=True,
                                word="\ue201д\ue205нородоу",
                            ),
                            lang="sl",
                            var="H",
                            orig_alt="\ue201д\ue205но\ue20dѧдъ",
                            orig_alt_var={"G": "\ue205но\ue20dѧдъ"},
                        )
                    ]
                )
            }
        },
        "\ue205но\ue20dѧдъ": {
            "μονογενής": {
                ("\ue205но\ue20dедаго", "μονογενοῦς"): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                var=True,
                                word="\ue205но\ue20dедаго",
                            ),
                            lang="sl",
                            var="G",
                            orig_alt="\ue201д\ue205но\ue20dѧдъ",
                            orig_alt_var={"H": "\ue201д\ue205нородъ"},
                        )
                    ]
                )
            }
        },
    }

    # semantics change from September 2021
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
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
        + [""] * 14,
        [""] * 4
        + [
            "1/W168a28",
            "\ue201д\ue205но\ue20dедаго",
            "цⷭ҇ре \ue201д\ue205но\ue20dедаго ѡтрока ѡ\ue010\ue20dа•",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 14,
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
        + [
            "bold|italic",
        ],
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
        + [""] * 14,
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
        + [""] * 14,
    ]
    # result = aggregate(rows, sl_sem, gr_sem)
    # print(result)

    result = SortedDict()
    result = aggregate(rows, gr_sem, sl_sem, result)
    assert result == SortedDict(
        {
            "μονογενής": SortedDict(
                {
                    "": SortedDict(
                        {
                            "": SortedDict(
                                {
                                    "\ue205но\ue20dѧдъ": {
                                        (
                                            "μονογενοῦς",
                                            "\ue205но\ue20dедаго",
                                        ): SortedSet(
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
                                                    var="G",
                                                    trans_alt="\ue201д\ue205но\ue20dѧдъ",
                                                    trans_alt_var={
                                                        "H": "\ue201д\ue205нородъ"
                                                    },
                                                )
                                            ]
                                        ),
                                        (
                                            "μονογενὴς",
                                            "\ue205но\ue20dадꙑ\ue205",
                                        ): SortedSet(
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
                                                    trans_alt_var={
                                                        "WH": "\ue201д\ue205но\ue20dѧдъ"
                                                    },
                                                )
                                            ]
                                        ),
                                        (
                                            "μονογενοῦς",
                                            "\ue205но\ue20dадѣмь",
                                        ): SortedSet(
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
                                                    trans_alt_var={
                                                        "WH": "\ue201д\ue205но\ue20dѧдъ"
                                                    },
                                                )
                                            ]
                                        ),
                                    },
                                    "\ue201д\ue205нородъ": {
                                        (
                                            "μονογενοῦς",
                                            "\ue201д\ue205нородоу",
                                        ): SortedSet(
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
                                                    var="H",
                                                    trans_alt="\ue201д\ue205но\ue20dѧдъ",
                                                    trans_alt_var={
                                                        "G": "\ue205но\ue20dѧдъ"
                                                    },
                                                )
                                            ]
                                        )
                                    },
                                    "\ue201д\ue205но\ue20dѧдъ": {
                                        (
                                            "μονογενοῦς",
                                            "\ue201д\ue205но\ue20dедаго",
                                        ): SortedSet(
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
                                        (
                                            "μονογενοῦς",
                                            "\ue201д\ue205но\ue20dедоу",
                                        ): SortedSet(
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
                                                    trans_alt_var={
                                                        "H": "\ue201д\ue205нородъ",
                                                        "G": "\ue205но\ue20dѧдъ",
                                                    },
                                                )
                                            ]
                                        ),
                                        (
                                            "μονογενὴς",
                                            "\ue201д\ue205но\ue20dеды",
                                        ): SortedSet(
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
                                                    var="WH",
                                                    trans_alt="\ue205но\ue20dѧдъ ",
                                                )
                                            ]
                                        ),
                                        (
                                            "μονογενοῦς",
                                            "\ue201д\ue205но\ue20dедѣмь",
                                        ): SortedSet(
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
                                                    var="WH",
                                                    trans_alt="\ue205но\ue20dѧдъ",
                                                )
                                            ]
                                        ),
                                    },
                                }
                            )
                        }
                    )
                }
            )
        }
    )


def test_aggregate_ipercliso():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
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
        + [""] * 8,
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
        + [""] * 9,
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
                                    orig_alt_var={"C": "ὑπερβλύω"},
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
                                    orig_alt_var={"C": "ὑπερβλύω"},
                                )
                            ]
                        )
                    }
                }
            },
        },
    }

    result = SortedDict()
    result = aggregate(rows, gr_sem.var, sl_sem, result)
    assert result == {
        "ὑπερβλύω": {
            "": {
                "": {
                    "прѣ\ue205сто\ue20d\ue205т\ue205": {
                        ("ὑπερβλύζων", "прѣ\ue205сто\ue20dе"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        var=True,
                                        word="ὑπερβλύζων",
                                    ),
                                    lang="gr",
                                    var="C",
                                    orig_alt="ὑπερκλύζω",
                                )
                            ]
                        )
                    }
                }
            },
            "inf.": {
                "": {
                    "\ue205сто\ue20dен\ue205\ue201": {
                        ("ὑπερβλύσαι", "\ue205сто\ue20dен\ue205\ue205"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        var=True,
                                        word="ὑπερβλύσαι",
                                    ),
                                    lang="gr",
                                    var="C",
                                    orig_alt="ὑπερκλύζω",
                                )
                            ]
                        )
                    }
                }
            },
        },
    }
