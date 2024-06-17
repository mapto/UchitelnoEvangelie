from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import FROM_LANG, TO_LANG
from config import FROM_LANG
from const import STYLE_COL

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


def test_est_in_var_no_main():
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
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "бꙑт\ue205": {
            "": {
                "gramm.": {
                    "": {
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
                                        Usage("gr", word="Ø", lemmas=["Ø"]),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        }
    }


"""
def test_prichatnik_biti_sl():
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
    result = aggregate([rows[0]], sl_sem, gr_sem, result)
    assert result == {
        "пр\ue205\ue20dьтьн\ue205къ": {
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
                                                "пр\ue205\ue20dьтьн\ue205къ",
                                                "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
                                            ],
                                            var_alt={
                                                Source("G"): Alternative(
                                                    "пр\ue205\ue20dестьн\ue205ц\ue205 б•",
                                                    [
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                    ],
                                                ),
                                                Source("H"): Alternative(
                                                    "пр\ue205\ue20dестн\ue205ц\ue205 б•",
                                                    [
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                    ],
                                                ),
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
                                                Source("G"): Alternative(
                                                    "пр\ue205\ue20dестьн\ue205ц\ue205 б•",
                                                    [
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                    ],
                                                ),
                                                Source("H"): Alternative(
                                                    "пр\ue205\ue20dестн\ue205ц\ue205 б•",
                                                    [
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                    ],
                                                ),
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
"""


def test_prichatnik_biti_sl_var():
    rows = [
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

    result = SortedDict()
    result = aggregate([rows[0]], sl_sem.var, gr_sem, result)
    assert result == {
        "пр\ue205\ue20dѧстьн\ue205къ": {
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
                                                "пр\ue205\ue20dѧстьн\ue205къ",
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
            }
        }
    }

    result = SortedDict()
    result = aggregate([rows[1]], sl_sem.var, gr_sem, result)
    assert result == {
        "бꙑт\ue205": {
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
            }
        }
    }


def test_mirno_sl():
    row = (
        [""] * 4
        + [
            "02/W169a17",
            "м\ue205рно\ue201•",
            "да\ue201 бран\ue205• ꙋтѣшен\ue205\ue201 м\ue205-",
            "м\ue205рьнъ",
        ]
        + [""] * 3
        + ["ἐκ", "ἐκ", "ἐκ τῆς εἰρήνης"]
        + [""] * 12
        + ["hl11:FFFCE4D6"]
        + ["1"] * 4
    )
    result = SortedDict()
    result = aggregate([row], sl_sem, gr_sem, result)
    assert result == {
        "м\ue205рьнъ": {
            "": {
                "": {
                    "": {
                        "ἐκ τῆς εἰρήνης → ἐκ": {
                            ("м\ue205рно\ue201•", "ἐκ"): SortedSet(
                                [
                                    Alignment(
                                        Index("2/W169a17"),
                                        Usage(
                                            "sl",
                                            word="м\ue205рно\ue201•",
                                            lemmas=["м\ue205рьнъ"],
                                        ),
                                        Usage(
                                            "gr",
                                            word="ἐκ",
                                            lemmas=["ἐκ", "ἐκ τῆς εἰρήνης"],
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
    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "пр\ue205\ue20dѧстьн\ue205къ": {
            "пр\ue205\ue20dѧстьн\ue205къ": {
                "": {
                    "": {
                        "ποιέω κοινωνόν → ποιέω": {
                            (
                                "пр\ue205\ue20dестн\ue205ц\ue205 H пр\ue205\ue20dестьн\ue205ц\ue205 G",
                                "ποιῆσαι",
                            ): SortedSet(
                                [
                                    Alignment(
                                        Index("5/28c21"),
                                        Usage(
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
                                        Usage(
                                            "gr",
                                            word="ποιῆσαι",
                                            lemmas=["ποιέω", "ποιέω κοινωνόν"],
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
