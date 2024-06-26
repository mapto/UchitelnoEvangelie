from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import FROM_LANG, TO_LANG
from config import FROM_LANG
from const import STYLE_COL

from model import Alternative, Index, Source, Alignment, Usage
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
    result = SortedDict()
    result = aggregate(rows, gr_sem, sl_sem, result)
    assert result == {
        "ὑπερκλύζω": {
            "": {
                "": {
                    "прѣ\ue205сто\ue20d\ue205т\ue205": {
                        ("ὑπερκλύζων", "прѣ\ue205сто\ue20dе"): SortedSet(
                            [
                                Alignment(
                                    Index("1/W168c17"),
                                    Usage(
                                        "gr",
                                        word="ὑπερκλύζων",
                                        lemmas=["ὑπερκλύζω"],
                                        var_alt={
                                            Source("Cs"): Alternative(
                                                "ὑπερβλύζων Cs", ["ὑπερβλύω"]
                                            )
                                        },
                                    ),
                                    Usage(
                                        "sl",
                                        word="прѣ\ue205сто\ue20dе",
                                        lemmas=["прѣ\ue205сто\ue20d\ue205т\ue205"],
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
                                Alignment(
                                    Index("1/W168c17"),
                                    Usage(
                                        "gr",
                                        word="ὑπερκλύσαι",
                                        lemmas=["ὑπερκλύζω", "inf."],
                                        var_alt={
                                            Source("Cs"): Alternative(
                                                "ὑπερβλύσαι Cs", ["ὑπερβλύω", "inf."]
                                            )
                                        },
                                    ),
                                    Usage(
                                        "sl",
                                        word="\ue205сто\ue20dен\ue205\ue205",
                                        lemmas=["\ue205сто\ue20dен\ue205\ue201"],
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
                        ("ὑπερβλύζων Cs", "прѣ\ue205сто\ue20dе"): SortedSet(
                            [
                                Alignment(
                                    Index("1/W168c17"),
                                    Usage(
                                        "gr",
                                        Source("Cs"),
                                        "ὑπερβλύζων Cs",
                                        ["ὑπερβλύω"],
                                        main_alt=Alternative(
                                            "ὑπερκλύζων", ["ὑπερκλύζω"]
                                        ),
                                    ),
                                    Usage(
                                        "sl",
                                        word="прѣ\ue205сто\ue20dе",
                                        lemmas=["прѣ\ue205сто\ue20d\ue205т\ue205"],
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
                        ("ὑπερβλύσαι Cs", "\ue205сто\ue20dен\ue205\ue205"): SortedSet(
                            [
                                Alignment(
                                    Index("1/W168c17"),
                                    Usage(
                                        "gr",
                                        Source("Cs"),
                                        "ὑπερβλύσαι Cs",
                                        ["ὑπερβλύω", "inf."],
                                        main_alt=Alternative(
                                            "ὑπερκλύσαι", ["ὑπερκλύζω", "inf."]
                                        ),
                                    ),
                                    Usage(
                                        "sl",
                                        word="\ue205сто\ue20dен\ue205\ue205",
                                        lemmas=["\ue205сто\ue20dен\ue205\ue201"],
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
                                    Alignment(
                                        Index("1/7a4"),
                                        Usage(
                                            FROM_LANG,
                                            word="боꙁѣ",
                                            lemmas=["богъ", "Dat."],
                                            var_alt={
                                                Source("WGH"): Alternative(
                                                    "б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H",
                                                    ["бож\ue205\ue205"],
                                                )
                                            },
                                        ),
                                        Usage(
                                            "gr", word="Θεοῦ", lemmas=["θεός", "Gen."]
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
                                    Alignment(
                                        Index("1/7a4"),
                                        Usage(
                                            FROM_LANG,
                                            Source("WGH"),
                                            "б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G",
                                            ["бож\ue205\ue205"],
                                            main_alt=Alternative(
                                                "боꙁѣ", ["богъ", "Dat."]
                                            ),
                                        ),
                                        Usage(
                                            "gr", word="Θεοῦ", lemmas=["θεός", "Gen."]
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
                                Alignment(
                                    Index("1/7a4"),
                                    Usage("gr", word="Θεοῦ", lemmas=["θεός", "Gen."]),
                                    Usage(
                                        "sl",
                                        Source("GHW"),
                                        "б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G",
                                        ["бож\ue205\ue205"],
                                        main_alt=Alternative("боꙁѣ", ["богъ", "Dat."]),
                                    ),
                                )
                            ]
                        )
                    }
                }
            }
        }
    }


def test_oslushat():
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
        + ["05/22b05", "послꙑшат\ue205", "ноу соущоу слꙑ-", "послꙑшат\ue205"]
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
                                Alignment(
                                    Index("5/22b5"),
                                    Usage(
                                        "gr", cnt=2, word="ἀκοῦσαι", lemmas=["ἀκούω"]
                                    ),
                                    Usage(
                                        "sl",
                                        word="послꙑшат\ue205",
                                        lemmas=["послꙑшат\ue205"],
                                        var_alt={
                                            Source("GH"): Alternative(
                                                "оуслышат\ue205 GH",
                                                ["ѹслꙑшат\ue205"],
                                                2,
                                            )
                                        },
                                    ),
                                )
                            ]
                        )
                    },
                    "слꙑшат\ue205": {
                        ("ἀκοῦσαι", "слꙑшат\ue205"): SortedSet(
                            [
                                Alignment(
                                    Index("5/22b5"),
                                    Usage("gr", word="ἀκοῦσαι", lemmas=["ἀκούω"]),
                                    Usage(
                                        "sl",
                                        word="слꙑшат\ue205",
                                        lemmas=["слꙑшат\ue205"],
                                        var_alt={
                                            Source("GH"): Alternative(
                                                "оуслышат\ue205 GH", ["ѹслꙑшат\ue205"]
                                            )
                                        },
                                    ),
                                )
                            ]
                        )
                    },
                    "ѹслꙑшат\ue205": {
                        ("ἀκοῦσαι", "оуслышат\ue205 GH"): SortedSet(
                            [
                                Alignment(
                                    Index("5/22b5"),
                                    Usage("gr", word="ἀκοῦσαι", lemmas=["ἀκούω"]),
                                    Usage(
                                        "sl",
                                        Source("GH"),
                                        "оуслышат\ue205 GH",
                                        ["ѹслꙑшат\ue205"],
                                        main_alt=Alternative(
                                            "слꙑшат\ue205", ["слꙑшат\ue205"]
                                        ),
                                    ),
                                ),
                                Alignment(
                                    Index("5/22b5"),
                                    Usage(
                                        "gr", cnt=2, word="ἀκοῦσαι", lemmas=["ἀκούω"]
                                    ),
                                    Usage(
                                        "sl",
                                        Source("GH"),
                                        "оуслышат\ue205 GH",
                                        ["ѹслꙑшат\ue205"],
                                        2,
                                        Alternative(
                                            "послꙑшат\ue205", ["послꙑшат\ue205"]
                                        ),
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
                                    Alignment(
                                        Index("5/22b5"),
                                        Usage(
                                            "sl",
                                            Source("GH"),
                                            "оуслышат\ue205 GH",
                                            ["ѹслꙑшат\ue205"],
                                            main_alt=Alternative(
                                                "слꙑшат\ue205", ["слꙑшат\ue205"]
                                            ),
                                        ),
                                        Usage("gr", word="ἀκοῦσαι", lemmas=["ἀκούω"]),
                                    ),
                                    Alignment(
                                        Index("5/22b5"),
                                        Usage(
                                            "sl",
                                            Source("GH"),
                                            "оуслышат\ue205 GH",
                                            ["ѹслꙑшат\ue205"],
                                            2,
                                            Alternative(
                                                "послꙑшат\ue205", ["послꙑшат\ue205"]
                                            ),
                                        ),
                                        Usage(
                                            "gr",
                                            word="ἀκοῦσαι",
                                            lemmas=["ἀκούω"],
                                            cnt=2,
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
                                    Alignment(
                                        Index("5/22b5"),
                                        Usage(
                                            "sl",
                                            word="послꙑшат\ue205",
                                            lemmas=["послꙑшат\ue205"],
                                            var_alt={
                                                Source("GH"): Alternative(
                                                    "оуслышат\ue205 GH",
                                                    ["ѹслꙑшат\ue205"],
                                                    2,
                                                )
                                            },
                                        ),
                                        Usage(
                                            "gr",
                                            word="ἀκοῦσαι",
                                            lemmas=["ἀκούω"],
                                            cnt=2,
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
                                    Alignment(
                                        Index("5/22b5"),
                                        Usage(
                                            "sl",
                                            word="слꙑшат\ue205",
                                            lemmas=["слꙑшат\ue205"],
                                            var_alt={
                                                Source("GH"): Alternative(
                                                    "оуслышат\ue205 GH",
                                                    ["ѹслꙑшат\ue205"],
                                                )
                                            },
                                        ),
                                        Usage("gr", word="ἀκοῦσαι", lemmas=["ἀκούω"]),
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
                                Alignment(
                                    Index("5/21a19"),
                                    Usage("gr", word="ἄτυφον", lemmas=["ἄτυφος"]),
                                    Usage(
                                        "sl",
                                        Source("WGH"),
                                        "вел\ue205\ue20dан\ue205е WGH",
                                        ["вел\ue205\ue20dан\ue205\ue201"],
                                        main_alt=Alternative(
                                            "невел\ue205\ue20dан\ue205\ue201",
                                            ["невел\ue205\ue20dан\ue205\ue201"],
                                        ),
                                    ),
                                )
                            ]
                        )
                    },
                    "невел\ue205\ue20dан\ue205\ue201": {
                        ("ἄτυφον", "невел\ue205\ue20dан\ue205\ue201"): SortedSet(
                            [
                                Alignment(
                                    Index("5/21a19"),
                                    Usage("gr", word="ἄτυφον", lemmas=["ἄτυφος"]),
                                    Usage(
                                        "sl",
                                        word="невел\ue205\ue20dан\ue205\ue201",
                                        lemmas=["невел\ue205\ue20dан\ue205\ue201"],
                                        var_alt={
                                            Source("WGH"): Alternative(
                                                "вел\ue205\ue20dан\ue205е WGH",
                                                ["вел\ue205\ue20dан\ue205\ue201"],
                                            )
                                        },
                                    ),
                                ),
                                Alignment(
                                    Index("5/21a19"),
                                    Usage(
                                        "gr", cnt=2, word="ἄτυφον", lemmas=["ἄτυφος"]
                                    ),
                                    Usage(
                                        "sl",
                                        word="невел\ue205\ue20dан\ue205\ue201",
                                        lemmas=["невел\ue205\ue20dан\ue205\ue201"],
                                        cnt=2,
                                        var_alt={
                                            Source("WGH"): Alternative(
                                                "невел\ue205\ue20d\ue205\ue201 WGH",
                                                ["невел\ue205\ue20d\ue205\ue201"],
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
                                Alignment(
                                    Index("5/21a19"),
                                    Usage(
                                        "gr", cnt=2, word="ἄτυφον", lemmas=["ἄτυφος"]
                                    ),
                                    Usage(
                                        "sl",
                                        Source("WGH"),
                                        "невел\ue205\ue20d\ue205\ue201 WGH",
                                        ["невел\ue205\ue20d\ue205\ue201"],
                                        main_alt=Alternative(
                                            "невел\ue205\ue20dан\ue205\ue201",
                                            ["невел\ue205\ue20dан\ue205\ue201"],
                                            2,
                                        ),
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
                                Alignment(
                                    Index("5/21a19"),
                                    Usage("gr", word="ἄτυφον", lemmas=["ἄτυφος"]),
                                    Usage(
                                        "sl",
                                        Source("WGH"),
                                        "вел\ue205\ue20dан\ue205е WGH",
                                        ["вел\ue205\ue20dан\ue205\ue201"],
                                        main_alt=Alternative(
                                            "невел\ue205\ue20dан\ue205\ue201",
                                            ["невел\ue205\ue20dан\ue205\ue201"],
                                        ),
                                    ),
                                )
                            ]
                        )
                    },
                    "невел\ue205\ue20d\ue205\ue201": {
                        ("ἄτυφον", "невел\ue205\ue20d\ue205\ue201 WGH"): SortedSet(
                            [
                                Alignment(
                                    Index("5/21a19"),
                                    Usage(
                                        "gr", cnt=2, word="ἄτυφον", lemmas=["ἄτυφος"]
                                    ),
                                    Usage(
                                        "sl",
                                        Source("WGH"),
                                        "невел\ue205\ue20d\ue205\ue201 WGH",
                                        ["невел\ue205\ue20d\ue205\ue201"],
                                        main_alt=Alternative(
                                            "невел\ue205\ue20dан\ue205\ue201",
                                            ["невел\ue205\ue20dан\ue205\ue201"],
                                            2,
                                        ),
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
                                    Alignment(
                                        Index("5/21a19"),
                                        Usage(
                                            "sl",
                                            Source("WGH"),
                                            "вел\ue205\ue20dан\ue205е WGH",
                                            ["вел\ue205\ue20dан\ue205\ue201"],
                                            main_alt=Alternative(
                                                "невел\ue205\ue20dан\ue205\ue201",
                                                ["невел\ue205\ue20dан\ue205\ue201"],
                                            ),
                                        ),
                                        Usage("gr", word="ἄτυφον", lemmas=["ἄτυφος"]),
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
                                    Alignment(
                                        Index("5/21a19"),
                                        Usage(
                                            "sl",
                                            Source("WGH"),
                                            "невел\ue205\ue20d\ue205\ue201 WGH",
                                            ["невел\ue205\ue20d\ue205\ue201"],
                                            main_alt=Alternative(
                                                "невел\ue205\ue20dан\ue205\ue201",
                                                ["невел\ue205\ue20dан\ue205\ue201"],
                                                2,
                                            ),
                                        ),
                                        Usage(
                                            "gr",
                                            word="ἄτυφον",
                                            lemmas=["ἄτυφος"],
                                            cnt=2,
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
                                Alignment(
                                    Index("16/80a8"),
                                    Usage(
                                        "gr",
                                        Source("Ch"),
                                        "ἄρτους Ch",
                                        ["ἄρτος"],
                                        main_alt=Alternative("om.", ["om."]),
                                    ),
                                    Usage("sl", word="хлѣбꙑ•", lemmas=["хлѣбъ"]),
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
                            ("вь WGH", "παρ’ Cs"): SortedSet(
                                [
                                    Alignment(
                                        Index("1/7d1"),
                                        Usage(
                                            "sl",
                                            Source("WHG"),
                                            "вь WGH",
                                            ["въ", "въ + Loc."],
                                            main_alt=Alternative(
                                                "оу",
                                                [
                                                    "ѹ praep.",
                                                    "оу + Gen.",
                                                ],
                                            ),
                                        ),
                                        Usage(
                                            "gr",
                                            Source("Cs"),
                                            "παρ’ Cs",
                                            ["παρά", "παρά + Acc."],
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
