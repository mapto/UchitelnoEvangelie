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
                                        idx=Index("5/28c21-d1"),
                                        orig=Usage(
                                            lang="sl",
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
                                        trans=Usage(
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
                                        idx=Index("5/28c21-d1"),
                                        orig=Usage(
                                            lang="sl",
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
                                        trans=Usage(
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
                                        idx=Index("25/125a3"),
                                        orig=Usage(
                                            lang="sl",
                                            alt=Alternative(
                                                var_lemmas={
                                                    Source(
                                                        "H"
                                                    ): "съмѣр\ue201наꙗ мѫдрость",
                                                    Source("WG"): "съмѣрѹмѫдрость",
                                                },
                                                var_words={
                                                    Source("H"): (
                                                        "смѣрены\ue201 моудрост\ue205 H",
                                                        1,
                                                    ),
                                                    Source("WG"): (
                                                        "смѣроумоудрост\ue205 WG",
                                                        1,
                                                    ),
                                                },
                                            ),
                                            word="съмѣромоудрост\ue205",
                                            lemmas=["съмѣромѫдрость"],
                                        ),
                                        trans=Usage(
                                            lang="gr",
                                            var=Source("Ch"),
                                            word="ταπεινοφροσύνην Ch",
                                            lemmas=["ταπεινοφροσύνη"],
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


def test_sumeromadrost_slvar():
    rows = [
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
            "съмѣрѹмѫдрость WG / съмѣр\ue201нъ H",
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
            "мѫдрость H",
            "съмѣр\ue201наꙗ мѫдрость H",
            "",
            "25/125a03",
            "съмѣромоудрост\ue205",
            "",
            "съмѣромѫдрость",
        ]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
        + ["hl00:FFFCD5B4"]
        + ["1"] * 4,
    ]
    result = SortedDict()
    result = aggregate(rows, sl_sem.var, gr_sem, result)
    assert result == {
        "мѫдрость": {
            "съмѣр\ue201наꙗ мѫдрость": {
                "": {
                    "": {
                        "ταπεινοφροσύνη": {
                            (
                                "смѣрены\ue201 моудрост\ue205 H",
                                "ταπεινοφροσύνην Ch",
                            ): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("25/125a3"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("H"),
                                            alt=Alternative(
                                                main_lemma="съмѣромѫдрость",
                                                main_word="съмѣромоудрост\ue205",
                                            ),
                                            word="смѣрены\ue201 моудрост\ue205 H",
                                            lemmas=[
                                                "мѫдрость",
                                                "съмѣр\ue201наꙗ мѫдрость",
                                            ],
                                        ),
                                        trans=Usage(
                                            lang="gr",
                                            var=Source("Ch"),
                                            word="ταπεινοφροσύνην Ch",
                                            lemmas=["ταπεινοφροσύνη"],
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
        "съмѣрѹмѫдрость": {
            "": {
                "": {
                    "": {
                        "ταπεινοφροσύνη": {
                            (
                                "смѣроумоудрост\ue205 WG",
                                "ταπεινοφροσύνην Ch",
                            ): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("25/125a3"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("WG"),
                                            alt=Alternative(
                                                main_lemma="съмѣромѫдрость",
                                                var_lemmas={
                                                    Source(
                                                        "H"
                                                    ): "съмѣр\ue201наꙗ мѫдрость"
                                                },
                                                main_word="съмѣромоудрост\ue205",
                                                var_words={
                                                    Source("H"): (
                                                        "смѣрены\ue201 моудрост\ue205 H",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="смѣроумоудрост\ue205 WG",
                                            lemmas=["съмѣрѹмѫдрость"],
                                        ),
                                        trans=Usage(
                                            lang="gr",
                                            var=Source("Ch"),
                                            word="ταπεινοφροσύνην Ch",
                                            lemmas=["ταπεινοφροσύνη"],
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
        "съмѣр\ue201нъ": {
            "съмѣр\ue201наꙗ мѫдрость": {
                "": {
                    "": {
                        "ταπεινοφροσύνη": {
                            (
                                "смѣрены\ue201 моудрост\ue205 H",
                                "ταπεινοφροσύνην Ch",
                            ): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("25/125a3"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("H"),
                                            alt=Alternative(
                                                main_lemma="съмѣромѫдрость",
                                                var_lemmas={
                                                    Source("WG"): "съмѣрѹмѫдрость"
                                                },
                                                main_word="съмѣромоудрост\ue205",
                                                var_words={
                                                    Source("WG"): (
                                                        "смѣроумоудрост\ue205 WG",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="смѣрены\ue201 моудрост\ue205 H",
                                            lemmas=[
                                                "съмѣр\ue201нъ",
                                                "съмѣр\ue201наꙗ мѫдрость",
                                            ],
                                        ),
                                        trans=Usage(
                                            lang="gr",
                                            var=Source("Ch"),
                                            word="ταπεινοφροσύνην Ch",
                                            lemmas=["ταπεινοφροσύνη"],
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


def test_sumeromadrost_slvar1():
    rows = [
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
            "съмѣрѹмѫдрость WG / съмѣр\ue201нъ H",
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
    ]
    result = SortedDict()
    result = aggregate(rows, sl_sem.var, gr_sem, result)
    assert result == {
        "съмѣрѹмѫдрость": {
            "": {
                "": {
                    "": {
                        "ταπεινοφροσύνη": {
                            (
                                "смѣроумоудрост\ue205 WG",
                                "ταπεινοφροσύνην Ch",
                            ): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("25/125a3"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("WG"),
                                            alt=Alternative(
                                                main_lemma="съмѣромѫдрость",
                                                var_lemmas={
                                                    Source(
                                                        "H"
                                                    ): "съмѣр\ue201наꙗ мѫдрость"
                                                },
                                                main_word="съмѣромоудрост\ue205",
                                                var_words={
                                                    Source("H"): (
                                                        "смѣрены\ue201 моудрост\ue205 H",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="смѣроумоудрост\ue205 WG",
                                            lemmas=["съмѣрѹмѫдрость"],
                                        ),
                                        trans=Usage(
                                            lang="gr",
                                            var=Source("Ch"),
                                            word="ταπεινοφροσύνην Ch",
                                            lemmas=["ταπεινοφροσύνη"],
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
        "съмѣр\ue201нъ": {
            "съмѣр\ue201наꙗ мѫдрость": {
                "": {
                    "": {
                        "ταπεινοφροσύνη": {
                            (
                                "смѣрены\ue201 моудрост\ue205 H",
                                "ταπεινοφροσύνην Ch",
                            ): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("25/125a3"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("H"),
                                            alt=Alternative(
                                                main_lemma="съмѣромѫдрость",
                                                var_lemmas={
                                                    Source("WG"): "съмѣрѹмѫдрость"
                                                },
                                                main_word="съмѣромоудрост\ue205",
                                                var_words={
                                                    Source("WG"): (
                                                        "смѣроумоудрост\ue205 WG",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="смѣрены\ue201 моудрост\ue205 H",
                                            lemmas=[
                                                "съмѣр\ue201нъ",
                                                "съмѣр\ue201наꙗ мѫдрость",
                                            ],
                                        ),
                                        trans=Usage(
                                            lang="gr",
                                            var=Source("Ch"),
                                            word="ταπεινοφροσύνην Ch",
                                            lemmas=["ταπεινοφροσύνη"],
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


def test_sumeromadrost_slvar1_grvar():
    rows = [
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
            "съмѣрѹмѫдрость WG / съмѣр\ue201нъ H",
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
    ]
    result = SortedDict()
    result = aggregate(rows, sl_sem.var, gr_sem.var, result)
    assert result == {
        "съмѣрѹмѫдрость": {
            "": {
                "": {
                    "": {
                        "ταπεινοφροσύνη": {
                            (
                                "смѣроумоудрост\ue205 WG",
                                "ταπεινοφροσύνην Ch",
                            ): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("25/125a3"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("WG"),
                                            alt=Alternative(
                                                main_lemma="съмѣромѫдрость",
                                                var_lemmas={
                                                    Source(
                                                        "H"
                                                    ): "съмѣр\ue201наꙗ мѫдрость"
                                                },
                                                main_word="съмѣромоудрост\ue205",
                                                var_words={
                                                    Source("H"): (
                                                        "смѣрены\ue201 моудрост\ue205 H",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="смѣроумоудрост\ue205 WG",
                                            lemmas=["съмѣрѹмѫдрость"],
                                        ),
                                        trans=Usage(
                                            lang="gr",
                                            var=Source("Ch"),
                                            word="ταπεινοφροσύνην Ch",
                                            lemmas=["ταπεινοφροσύνη"],
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
        "съмѣр\ue201нъ": {
            "съмѣр\ue201наꙗ мѫдрость": {
                "": {
                    "": {
                        "ταπεινοφροσύνη": {
                            (
                                "смѣрены\ue201 моудрост\ue205 H",
                                "ταπεινοφροσύνην Ch",
                            ): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("25/125a3"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("H"),
                                            alt=Alternative(
                                                main_lemma="съмѣромѫдрость",
                                                var_lemmas={
                                                    Source("WG"): "съмѣрѹмѫдрость"
                                                },
                                                main_word="съмѣромоудрост\ue205",
                                                var_words={
                                                    Source("WG"): (
                                                        "смѣроумоудрост\ue205 WG",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="смѣрены\ue201 моудрост\ue205 H",
                                            lemmas=[
                                                "съмѣр\ue201нъ",
                                                "съмѣр\ue201наꙗ мѫдрость",
                                            ],
                                        ),
                                        trans=Usage(
                                            lang="gr",
                                            var=Source("Ch"),
                                            word="ταπεινοφροσύνην Ch",
                                            lemmas=["ταπεινοφροσύνη"],
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
                                            var=Source("WH"),
                                            alt=Alternative(
                                                main_lemma="аще",
                                                main_word="аще",
                                            ),
                                            word="om. WH",
                                            lemmas=["om."],
                                        ),
                                    ),
                                    Alignment(
                                        Index("1/7c6"),
                                        Usage("gr", word="om.", lemmas=["om."]),
                                        Usage(
                                            "sl",
                                            var=Source("WH"),
                                            alt=Alternative(
                                                main_lemma="\ue205 conj.",
                                                main_word="\ue205",
                                            ),
                                            word="om. WH",
                                            lemmas=["om."],
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
                                            alt=Alternative(
                                                var_lemmas={Source("WH"): "om."},
                                                var_words={Source("WH"): ("om. WH", 1)},
                                            ),
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
                                            alt=Alternative(
                                                var_lemmas={Source("WH"): "om."},
                                                var_words={Source("WH"): ("om. WH", 1)},
                                            ),
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
