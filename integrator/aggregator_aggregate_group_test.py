from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import STYLE_COL
from config import FROM_LANG, TO_LANG

from model import Alternative, Index, Source, Alignment, Usage
from semantics import MainLangSemantics, VarLangSemantics
from aggregator import aggregate

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
    VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20], cnt_col=STYLE_COL + 4),
    cnt_col=STYLE_COL + 3,
)


def test_prichatnik_biti_combined():
    rows = [
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H "
            "боудемь W",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + [
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H "
            "боудемь W",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "боудоуть• \ue201же",
            "бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
            "",
            "",
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
    ]

    result = SortedDict()
    result = aggregate([rows[1]], sl_sem, gr_sem, result)
    assert result == {
        "бꙑт\ue205": {
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205": {
                "": {
                    "": {
                        "ποιέω κοινωνόν → ποιέω & κοινωνός": {
                            (
                                "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                "ποιῆσαι κοινωνοὺς",
                            ): SortedSet(
                                [
                                    Alignment(
                                        Index("5/28c21-d1"),
                                        Usage(
                                            "sl",
                                            word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            lemmas=[
                                                "бꙑт\ue205",
                                                "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
                                            ],
                                            var_alt={
                                                Source("GH"): Alternative(
                                                    "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H",
                                                    [
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                    ],
                                                )
                                            },
                                        ),
                                        Usage(
                                            "gr",
                                            word="ποιῆσαι κοινωνοὺς",
                                            lemmas=[
                                                "ποιέω & κοινωνός",
                                                "ποιέω κοινωνόν",
                                            ],
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

    rows_var = [
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H боудемь W"
            "",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + ["ποιῆσαι κοινωνοὺς", "ποιέω & κοινωνός", "ποιέω κοινωνόν"]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H боудемь W",
            "бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "боудоуть• \ue201же",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + ["ποιῆσαι κοινωνοὺς", "ποιέω & κοινωνός", "ποιέω κοινωνόν"]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
    ]

    result = aggregate([rows_var[1]], sl_sem.var, gr_sem, result)
    assert result == {
        "бꙑт\ue205": {
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205": {
                "": {
                    "": {
                        "ποιέω κοινωνόν → ποιέω & κοινωνός": {
                            (
                                "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                "ποιῆσαι κοινωνοὺς",
                            ): SortedSet(
                                [
                                    Alignment(
                                        Index("5/28c21-d1"),
                                        Usage(
                                            "sl",
                                            word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            lemmas=[
                                                "бꙑт\ue205",
                                                "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
                                            ],
                                            var_alt={
                                                Source("GH"): Alternative(
                                                    "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H",
                                                    [
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                    ],
                                                )
                                            },
                                        ),
                                        Usage(
                                            "gr",
                                            word="ποιῆσαι κοινωνοὺς",
                                            lemmas=[
                                                "ποιέω & κοινωνός",
                                                "ποιέω κοινωνόν",
                                            ],
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            },
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205": {
                "": {
                    "": {
                        "ποιέω κοινωνόν → ποιέω & κοινωνός": {
                            (
                                "пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                "ποιῆσαι κοινωνοὺς",
                            ): SortedSet(
                                [
                                    Alignment(
                                        Index("5/28c21-d1"),
                                        Usage(
                                            "sl",
                                            Source("GH"),
                                            "пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                            [
                                                "бꙑт\ue205",
                                                "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                            ],
                                            main_alt=Alternative(
                                                "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                                [
                                                    "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
                                                    "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
                                                ],
                                            ),
                                        ),
                                        Usage(
                                            "gr",
                                            word="ποιῆσαι κοινωνοὺς",
                                            lemmas=[
                                                "ποιέω & κοινωνός",
                                                "ποιέω κοινωνόν",
                                            ],
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            },
        }
    }


def test_sumeromadrost():
    rows = [
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
            "съмѣрѹмѫдрость WG / съмѣр\ue201нъ мѫдрость H",
            "съмѣр\ue201наꙗ мѫдрость H",
            "",
            "25/125a03",
            "съмѣромоудрост\ue205",
            "съмѣромоудро-",
            "съмѣромѫдрость",
        ]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
        + ["hl00:FFFCD5B4"]
        + ["1"] * 4,
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
            "съмѣрѹмѫдрость WG / съмѣр\ue201нъ мѫдрость H",
            "съмѣр\ue201наꙗ мѫдрость H",
            "",
            "25/125a03",
            "съмѣромоудрост\ue205",
        ]
        + [""] * 5
        + ["om."]
        + [""] * 4
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
        + ["hl00:FFFCD5B4"]
        + ["1"] * 4,
    ]
    result = SortedDict()
    result = aggregate(rows, sl_sem, gr_sem, result)
    assert result == {
        "съмѣромѫдрость": {
            "": {
                "": {
                    "": {
                        "ταπεινοφροσύνη": {
                            ("съмѣромоудрост\ue205", "ταπεινοφροσύνην Ch"): SortedSet(
                                [
                                    Alignment(
                                        Index("25/125a3"),
                                        Usage(
                                            "sl",
                                            word="съмѣромоудрост\ue205",
                                            lemmas=["съмѣромѫдрость"],
                                            var_alt={
                                                Source("H"): Alternative(
                                                    "смѣрены\ue201 моудрост\ue205 H",
                                                    [
                                                        "съмѣр\ue201нъ мѫдрость",
                                                        "съмѣр\ue201наꙗ мѫдрость",
                                                    ],
                                                ),
                                                Source("WG"): Alternative(
                                                    "смѣроумоудрост\ue205 WG",
                                                    ["съмѣрѹмѫдрость"],
                                                ),
                                            },
                                        ),
                                        Usage(
                                            "gr",
                                            Source("Ch"),
                                            "ταπεινοφροσύνην Ch",
                                            ["ταπεινοφροσύνη"],
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


def test_repeated_om():
    rows = [
        ["om. WH", "om."]
        + [""] * 2
        + ["1/7c6", "аще", "аще \ue205 не", "аще"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["1/7c6", "не", "аще \ue205 не", "не"]
        + [""] * 3
        + ["οὐ", "οὐ"]
        + [""] * 14
        + ["1"] * 4,
        ["om. WH", "om."]
        + [""] * 2
        + ["1/7c6", "\ue205", "аще \ue205 не", "\ue205 conj."]
        + [""] * 3
        + ["om."] * 2
        + [""] * 14
        + ["1"] * 4,
    ]

    result = SortedDict()
    result = aggregate([rows[0]], gr_sem, sl_sem, result)
    result = aggregate([rows[2]], gr_sem, sl_sem, result)
    assert result == {
        "om.": {
            "": {
                "": {
                    "": {
                        "om.": {
                            ("om.", "om. WH"): SortedSet(
                                [
                                    Alignment(
                                        Index("1/7c6"),
                                        Usage("gr", word="om.", lemmas=["om."]),
                                        Usage(
                                            "sl",
                                            Source("WH"),
                                            "om. WH",
                                            ["om."],
                                            main_alt=Alternative("аще", ["аще"]),
                                        ),
                                    ),
                                    Alignment(
                                        Index("1/7c6"),
                                        Usage("gr", word="om.", lemmas=["om."]),
                                        Usage(
                                            "sl",
                                            Source("WH"),
                                            "om. WH",
                                            ["om."],
                                            main_alt=Alternative(
                                                "\ue205", ["\ue205 conj."]
                                            ),
                                        ),
                                    ),
                                ]
                            )
                        },
                        "аще": {
                            ("om.", "аще"): SortedSet(
                                [
                                    Alignment(
                                        Index("1/7c6"),
                                        Usage("gr", word="om.", lemmas=["om."]),
                                        Usage(
                                            "sl",
                                            var_alt={
                                                Source("WH"): Alternative(
                                                    "om. WH", ["om."]
                                                )
                                            },
                                            word="аще",
                                            lemmas=["аще"],
                                        ),
                                    )
                                ]
                            )
                        },
                        "\ue205 conj.": {
                            ("om.", "\ue205"): SortedSet(
                                [
                                    Alignment(
                                        Index("1/7c6"),
                                        Usage("gr", word="om.", lemmas=["om."]),
                                        Usage(
                                            "sl",
                                            var_alt={
                                                Source("WH"): Alternative(
                                                    "om. WH", ["om."]
                                                )
                                            },
                                            word="\ue205",
                                            lemmas=["\ue205 conj."],
                                        ),
                                    )
                                ]
                            )
                        },
                    }
                }
            }
        }
    }
