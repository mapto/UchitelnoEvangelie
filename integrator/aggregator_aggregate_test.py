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
                                            var=Source("GH"),
                                            alt=Alternative(
                                                main_lemma="om.",
                                                main_word="om.",
                                            ),
                                            word="\ue201сть GH",
                                            lemmas=["бꙑт\ue205", "", "gramm."],
                                        ),
                                        Usage(lang="gr", word="Ø", lemmas=["Ø"]),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        }
    }


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
                                            alt=Alternative(
                                                var_lemmas={
                                                    Source(
                                                        "GH"
                                                    ): "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205"
                                                },
                                                var_words={
                                                    Source("GH"): (
                                                        "пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            lemmas=[
                                                "пр\ue205\ue20dьтьн\ue205къ",
                                                "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
                                            ],
                                        ),
                                        Usage(
                                            lang="gr",
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
                                            alt=Alternative(
                                                var_lemmas={
                                                    Source(
                                                        "GH"
                                                    ): "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205"
                                                },
                                                var_words={
                                                    Source("GH"): (
                                                        "пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            lemmas=[
                                                "бꙑт\ue205",
                                                "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
                                            ],
                                        ),
                                        Usage(
                                            lang="gr",
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
                                            var=Source("GH"),
                                            alt=Alternative(
                                                main_lemma="пр\ue205\ue20dьтьн\ue205къ быт\ue205",
                                                main_word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            ),
                                            word="пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                            lemmas=[
                                                "пр\ue205\ue20dѧстьн\ue205къ",
                                                "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                            ],
                                        ),
                                        Usage(
                                            lang="gr",
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
                                            var=Source("GH"),
                                            alt=Alternative(
                                                main_lemma="пр\ue205\ue20dьтьн\ue205къ быт\ue205",
                                                main_word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            ),
                                            word="пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                            lemmas=[
                                                "бꙑт\ue205",
                                                "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                            ],
                                        ),
                                        Usage(
                                            lang="gr",
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


def test_monogenes():
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

    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "\ue201д\ue205нородъ": {
            "": {
                "": {
                    "": {
                        "μονογενής": {
                            ("\ue201д\ue205нородоу H", "μονογενοῦς"): SortedSet(
                                [
                                    Alignment(
                                        Index("1/W168a25"),
                                        Usage(
                                            "sl",
                                            var=Source("H"),
                                            alt=Alternative(
                                                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                                var_lemmas={
                                                    Source("G"): "\ue205но\ue20dѧдъ"
                                                },
                                                main_word="\ue201д\ue205но\ue20dедоу",
                                                var_words={
                                                    Source("G"): (
                                                        "\ue205но\ue20dедаго G",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="\ue201д\ue205нородоу H",
                                            lemmas=["\ue201д\ue205нородъ"],
                                        ),
                                        Usage(
                                            lang="gr",
                                            word="μονογενοῦς",
                                            lemmas=["μονογενής"],
                                        ),
                                        bold=True,
                                        italic=True,
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
        "\ue205но\ue20dѧдъ": {
            "": {
                "": {
                    "": {
                        "μονογενής": {
                            ("\ue205но\ue20dедаго G", "μονογενοῦς"): SortedSet(
                                [
                                    Alignment(
                                        Index("1/W168a25"),
                                        Usage(
                                            "sl",
                                            var=Source("G"),
                                            alt=Alternative(
                                                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                                var_lemmas={
                                                    Source("H"): "\ue201д\ue205нородъ"
                                                },
                                                main_word="\ue201д\ue205но\ue20dедоу",
                                                var_words={
                                                    Source("H"): (
                                                        "\ue201д\ue205нородоу H",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="\ue205но\ue20dедаго G",
                                            lemmas=["\ue205но\ue20dѧдъ"],
                                        ),
                                        Usage(
                                            lang="gr",
                                            word="μονογενοῦς",
                                            lemmas=["μονογενής"],
                                        ),
                                        bold=True,
                                        italic=True,
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
    }


def test_puteshestvie_sl_var():
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
    result = aggregate([rows[0]], sl_sem.var, gr_sem, result)
    assert result == {
        "шьств\ue205\ue201": {
            "шьств\ue205\ue201 пѫт\ue205": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            ("шьств\ue205ꙗ пꙋт\ue205 H", "ὁδοιπορίας"): SortedSet(
                                [
                                    Alignment(
                                        Index("5/28d18"),
                                        Usage(
                                            "sl",
                                            var=Source("H"),
                                            alt=Alternative(
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
                                            word="шьств\ue205ꙗ пꙋт\ue205 H",
                                            lemmas=[
                                                "шьств\ue205\ue201",
                                                "шьств\ue205\ue201 пѫт\ue205",
                                            ],
                                        ),
                                        Usage(
                                            "gr",
                                            word="ὁδοιπορίας",
                                            lemmas=["ὁδοιπορία"],
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
                                    Alignment(
                                        Index("5/28d18"),
                                        Usage(
                                            "sl",
                                            var=Source("G"),
                                            alt=Alternative(
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
                                            word="шьст\ue205ꙗ пꙋт\ue205 G",
                                            lemmas=[
                                                "шьст\ue205\ue201",
                                                "шьст\ue205\ue201 пѫт\ue205",
                                            ],
                                        ),
                                        Usage(
                                            lang="gr",
                                            word="ὁδοιπορίας",
                                            lemmas=["ὁδοιπορία"],
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

    result = SortedDict()
    result = aggregate([rows[1]], sl_sem.var, gr_sem, result)
    assert result == {
        "пѫть": {
            "шьств\ue205\ue201 пѫт\ue205": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            ("шьств\ue205ꙗ пꙋт\ue205 H", "ὁδοιπορίας"): SortedSet(
                                [
                                    Alignment(
                                        Index("5/28d18"),
                                        Usage(
                                            "sl",
                                            var=Source("H"),
                                            alt=Alternative(
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
                                            word="шьств\ue205ꙗ пꙋт\ue205 H",
                                            lemmas=[
                                                "пѫть",
                                                "шьств\ue205\ue201 пѫт\ue205",
                                            ],
                                        ),
                                        Usage(
                                            lang="gr",
                                            word="ὁδοιπορίας",
                                            lemmas=["ὁδοιπορία"],
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
                            ("шьст\ue205ꙗ пꙋт\ue205 G", "ὁδοιπορίας"): SortedSet(
                                [
                                    Alignment(
                                        Index("5/28d18"),
                                        Usage(
                                            lang="sl",
                                            var=Source("G"),
                                            alt=Alternative(
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
                                            word="шьст\ue205ꙗ пꙋт\ue205 G",
                                            lemmas=[
                                                "пѫть",
                                                "шьст\ue205\ue201 пѫт\ue205",
                                            ],
                                        ),
                                        Usage(
                                            lang="gr",
                                            word="ὁδοιπορίας",
                                            lemmas=["ὁδοιπορία"],
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


def test_puteshestvie_gr():
    row = (
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст & пѫть G / шьств & пѫть H",
            "шьст\ue205\ue201 пѫт\ue205 G шьств\ue205\ue201 пѫт\ue205 H",
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
        + ["1"] * 4
    )

    result = SortedDict()
    result = aggregate([row], gr_sem, sl_sem.var, result)
    assert result == {
        "ὁδοιπορία": {
            "": {
                "": {
                    "": {
                        "шьств\ue205\ue201 пѫт\ue205 → шьств\ue205\ue201 & пѫть": {
                            ("ὁδοιπορίας", "шьств\ue205ꙗ пꙋт\ue205 H"): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("5/28d18"),
                                        orig=Usage(
                                            lang="gr",
                                            word="ὁδοιπορίας",
                                            lemmas=["ὁδοιπορία"],
                                        ),
                                        trans=Usage(
                                            lang="sl",
                                            var=Source("H"),
                                            alt=Alternative(
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
                                            word="шьств\ue205ꙗ пꙋт\ue205 H",
                                            lemmas=[
                                                "шьств\ue205\ue201 & пѫть",
                                                "шьств\ue205\ue201 пѫт\ue205",
                                            ],
                                        ),
                                    )
                                ]
                            )
                        },
                        "шьст\ue205\ue201 пѫт\ue205 → шьст\ue205\ue201 & пѫть": {
                            ("ὁδοιπορίας", "шьст\ue205ꙗ пꙋт\ue205 G"): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("5/28d18"),
                                        orig=Usage(
                                            lang="gr",
                                            word="ὁδοιπορίας",
                                            lemmas=["ὁδοιπορία"],
                                        ),
                                        trans=Usage(
                                            lang="sl",
                                            var=Source("G"),
                                            alt=Alternative(
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
                                            word="шьст\ue205ꙗ пꙋт\ue205 G",
                                            lemmas=[
                                                "шьст\ue205\ue201 & пѫть",
                                                "шьст\ue205\ue201 пѫт\ue205",
                                            ],
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
                                        idx=Index("2/W169a17"),
                                        orig=Usage(
                                            lang="sl",
                                            word="м\ue205рно\ue201•",
                                            lemmas=["м\ue205рьнъ"],
                                        ),
                                        trans=Usage(
                                            lang="gr",
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
                                        idx=Index("5/28c21"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("GH"),
                                            alt=Alternative(
                                                main_lemma="пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
                                                main_word="пр\ue205\ue20dьтьн\ue205ц\ue205",
                                            ),
                                            word="пр\ue205\ue20dестн\ue205ц\ue205 H пр\ue205\ue20dестьн\ue205ц\ue205 G",
                                            lemmas=[
                                                "пр\ue205\ue20dѧстьн\ue205къ",
                                                "пр\ue205\ue20dѧстьн\ue205къ",
                                            ],
                                        ),
                                        trans=Usage(
                                            lang="gr",
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
