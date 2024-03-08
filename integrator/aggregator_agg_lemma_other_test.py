from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import STYLE_COL
from config import FROM_LANG, TO_LANG

from model import Alternative, Index, Source, Alignment, Usage
from semantics import MainLangSemantics, VarLangSemantics
from aggregator import _agg_lemma

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


def test_shestvie_1():
    row = (
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
        + ["1"] * 4
    )

    result = SortedDict()
    result = _agg_lemma(
        row,
        sl_sem.var,
        gr_sem,
        result,
        sl_sem.var.lemmas[0],
        Source("G"),
        "ὁδοιπορία",
    )
    assert result == {
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
                                            Source("G"),
                                            "шьст\ue205ꙗ пꙋт\ue205 G",
                                            [
                                                "шьст\ue205\ue201",
                                                "шьст\ue205\ue201 пѫт\ue205",
                                            ],
                                            main_alt=Alternative(
                                                "поутошьств\ue205ꙗ",
                                                "пѫтошьств\ue205\ue201",
                                            ),
                                            var_alt={
                                                Source("H"): Alternative(
                                                    "шьств\ue205ꙗ пꙋт\ue205 H",
                                                    "шьств\ue205\ue201 пѫт\ue205",
                                                )
                                            },
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
            },
        },
    }

    result = SortedDict()
    result = _agg_lemma(
        row,
        sl_sem.var,
        gr_sem,
        result,
        sl_sem.var.lemmas[0],
        Source("H"),
        "ὁδοιπορία",
    )
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
                                            Source("H"),
                                            "шьств\ue205ꙗ пꙋт\ue205 H",
                                            [
                                                "шьств\ue205\ue201",
                                                "шьств\ue205\ue201 пѫт\ue205",
                                            ],
                                            main_alt=Alternative(
                                                "поутошьств\ue205ꙗ",
                                                "пѫтошьств\ue205\ue201",
                                            ),
                                            var_alt={
                                                Source("G"): Alternative(
                                                    "шьст\ue205ꙗ пꙋт\ue205 G",
                                                    "шьст\ue205\ue201 пѫт\ue205",
                                                )
                                            },
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
        }
    }


def test_shestvie_2():
    row = (
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
        + ["1"] * 4
    )

    result = SortedDict()
    result = _agg_lemma(
        row,
        sl_sem.var,
        gr_sem,
        result,
        sl_sem.var.lemmas[1],
        Source("G"),
        "ὁδοιπορία",
    )
    assert result == {
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
                                        Source("G"),
                                        "шьст\ue205ꙗ пꙋт\ue205 G",
                                        [
                                            "шьст\ue205\ue201",
                                            "шьст\ue205\ue201 пѫт\ue205",
                                        ],
                                        main_alt=Alternative(
                                            "поутошьств\ue205ꙗ", "пѫтошьств\ue205\ue201"
                                        ),
                                        var_alt={
                                            Source("H"): Alternative(
                                                "шьств\ue205ꙗ пꙋт\ue205 H",
                                                "шьств\ue205\ue201 пѫт\ue205",
                                            )
                                        },
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
        },
    }

    result = SortedDict()
    result = _agg_lemma(
        row,
        sl_sem.var,
        gr_sem,
        result,
        sl_sem.var.lemmas[1],
        Source("H"),
        "ὁδοιπορία",
    )
    assert result == {
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
                                        Source("H"),
                                        "шьств\ue205ꙗ пꙋт\ue205 H",
                                        [
                                            "шьств\ue205\ue201",
                                            "шьств\ue205\ue201 пѫт\ue205",
                                        ],
                                        main_alt=Alternative(
                                            "поутошьств\ue205ꙗ", "пѫтошьств\ue205\ue201"
                                        ),
                                        var_alt={
                                            Source("G"): Alternative(
                                                "шьст\ue205ꙗ пꙋт\ue205 G",
                                                "шьст\ue205\ue201 пѫт\ue205",
                                            )
                                        },
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
        },
    }


def test_2_H():
    row = (
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
        + ["om."] * 2
        + [""] * 3
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
        + ["hl00:FFFCD5B4"]
        + ["1"] * 4
    )
    result = SortedDict()
    result = _agg_lemma(row, sl_sem.var, gr_sem, result, 2, Source("H"), "om.")
    assert result == {
        "съмѣр\ue201наꙗ мѫдрость": {
            "": {
                "": {
                    "om.": {
                        ("смѣрены\ue201 моудрост\ue205 H", "om."): SortedSet(
                            [
                                Alignment(
                                    Index("25/125a3"),
                                    Usage(
                                        "sl",
                                        Source("H"),
                                        "смѣрены\ue201 моудрост\ue205 H",
                                        ["съмѣр\ue201нъ", "съмѣр\ue201наꙗ мѫдрость"],
                                        main_alt=Alternative(
                                            "съмѣромоудрост\ue205", "съмѣромѫдрость"
                                        ),
                                        var_alt={
                                            Source("WG"): Alternative(
                                                "смѣроумоудрост\ue205 WG",
                                                "съмѣрѹмѫдрость",
                                            )
                                        },
                                    ),
                                    Usage(
                                        "gr",
                                        word="om.",
                                        lemmas=["om."],
                                        var_alt={
                                            Source("Ch"): Alternative(
                                                "ταπεινοφροσύνην Ch", "ταπεινοφροσύνη"
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


def test_junotichisk():
    row = (
        ["юнотьско\ue201 WG юноть\ue20dьско\ue201 H", "юнотьскъ WG"]
        + [""] * 2
        + [
            "38/179d17",
            "ꙋноть\ue20dьско\ue201",
            "боудеть• \ue205 ꙋно-",
            "юноть\ue20dьскъ",
        ]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + [
            "νεότητος CsMdSp / νεανιότητος FbPcPePgPhPiZaAPaVCh",
            "νεότης CsMdSp / νεανιότης FbPcPePgPhPiZaAPaVCh",
            "Gen.",
        ]
        + [""] * 7
        + ["hl22:FFA9A9A9|hl20:FFA9A9A9"]
        + ["1"] * 4
    )
    result = SortedDict()
    result = _agg_lemma(
        row.copy(), gr_sem.var, sl_sem, result, 18, Source("CsMdSp"), "юнотььскъ"
    )
    assert result == {
        "Gen.": {
            "": {
                "": {
                    "юноть\ue20dьскъ": {
                        (
                            "νεότητος CsMdSp",
                            "ꙋноть\ue20dьско\ue201",
                        ): SortedSet(
                            [
                                Alignment(
                                    Index("38/179d17"),
                                    Usage(
                                        "gr",
                                        Source("CsMdSp"),
                                        "νεότητος CsMdSp",
                                        ["νεότης", "Gen."],
                                        var_alt={
                                            Source("FbPcPePgPhPiVZaAPaCh"): Alternative(
                                                "/ νεανιότητος FbPcPePgPhPiVZaAPaCh",
                                                "νεανιότης",
                                            )
                                        },
                                    ),
                                    Usage(
                                        "sl",
                                        word="ꙋноть\ue20dьско\ue201",
                                        lemmas=["юноть\ue20dьскъ"],
                                        var_alt={
                                            Source("WG"): Alternative(
                                                "юнотьско\ue201 WG",
                                                "юнотьскъ",
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

    result = SortedDict()
    result = _agg_lemma(
        row.copy(),
        gr_sem.var,
        sl_sem,
        result,
        18,
        Source("FbPcPePgPhPiZaAPaVCh"),
        "юнотььскъ",
    )
    assert result == {
        "Gen.": {
            "": {
                "": {
                    "юноть\ue20dьскъ": {
                        (
                            "/ νεανιότητος FbPcPePgPhPiVZaAPaCh",
                            "ꙋноть\ue20dьско\ue201",
                        ): SortedSet(
                            [
                                Alignment(
                                    Index("38/179d17"),
                                    Usage(
                                        "gr",
                                        Source("FbPcPePgPhPiVZaAPaCh"),
                                        word="/ νεανιότητος FbPcPePgPhPiVZaAPaCh",
                                        lemmas=["νεανιότης", "Gen."],
                                        var_alt={
                                            Source("CsMdSp"): Alternative(
                                                "νεότητος CsMdSp",
                                                "νεότης",
                                            )
                                        },
                                    ),
                                    Usage(
                                        "sl",
                                        word="ꙋноть\ue20dьско\ue201",
                                        lemmas=["юноть\ue20dьскъ"],
                                        var_alt={
                                            Source("WG"): Alternative(
                                                "юнотьско\ue201 WG",
                                                "юнотьскъ",
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


def test_prichatnik():
    row = (
        [
            "боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 G пр\ue205\ue20dестн\ue205ц\ue205 H",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "≈ GH",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "≈",
            "",
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05:FFFCD5B4|hl00:FFFCD5B4|hl11:FFFCD5B4"]
        + ["1"] * 4
    )

    result = SortedDict()
    result = _agg_lemma(row, sl_sem, gr_sem, result, col=9, tlemma="ποιέω & κοινωνός")
    assert result == {
        "": {
            "": {
                "≈ ποιέω κοινωνόν → ποιέω & κοινωνός": {
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
                                        "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
                                    ],
                                    var_alt={
                                        Source("GH"): Alternative(
                                            word="пр\ue205\ue20dестн\ue205ц\ue205 H пр\ue205\ue20dестьн\ue205ц\ue205 G",
                                            lemma="пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                            semantic="≈",
                                        )
                                    },
                                ),
                                Usage(
                                    "gr",
                                    word="ποιῆσαι κοινωνοὺς",
                                    lemmas=["ποιέω & κοινωνός", "≈ ποιέω κοινωνόν"],
                                ),
                                semantic="≈",
                            )
                        ]
                    )
                }
            }
        }
    }
