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


def test_first():
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
    _agg_lemma(row, sl_sem.var, gr_sem, result)
    assert result == {
        "съмѣрѹмѫдрость": {
            "": {
                "": {
                    "": {
                        "om.": {
                            ("смѣроумоудрост\ue205 WG", "om."): SortedSet(
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
                                            alt=Alternative(
                                                var_lemmas={
                                                    Source("Ch"): "ταπεινοφροσύνη"
                                                },
                                                var_words={
                                                    Source("Ch"): (
                                                        "ταπεινοφροσύνην Ch",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="om.",
                                            lemmas=["om."],
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
                        "om.": {
                            ("смѣрены\ue201 моудрост\ue205 H", "om."): SortedSet(
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
                                            alt=Alternative(
                                                var_lemmas={
                                                    Source("Ch"): "ταπεινοφροσύνη"
                                                },
                                                var_words={
                                                    Source("Ch"): (
                                                        "ταπεινοφροσύνην Ch",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="om.",
                                            lemmas=["om."],
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
                                    idx=Index("25/125a3"),
                                    orig=Usage(
                                        lang="sl",
                                        var=Source("H"),
                                        alt=Alternative(
                                            main_lemma="съмѣромѫдрость",
                                            var_lemmas={Source("WG"): "съмѣрѹмѫдрость"},
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
                                        alt=Alternative(
                                            var_lemmas={Source("Ch"): "ταπεινοφροσύνη"},
                                            var_words={
                                                Source("Ch"): ("ταπεινοφροσύνην Ch", 1)
                                            },
                                        ),
                                        word="om.",
                                        lemmas=["om."],
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
    result = _agg_lemma(row, sl_sem.var, gr_sem, result)
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


def test_ashte():
    row = (
        ["om. WH", "om."]
        + [""] * 2
        + ["1/7c6", "аще", "аще \ue205 не", "аще"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 14
        + ["1"] * 4
    )

    result = SortedDict()
    _agg_lemma(row, gr_sem, sl_sem, result)
    assert result == {
        "om.": {
            "": {
                "": {
                    "": {
                        "аще": {
                            ("om.", "аще"): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("1/7c6"),
                                        orig=Usage(
                                            lang="gr",
                                            word="om.",
                                            lemmas=["om."],
                                        ),
                                        trans=Usage(
                                            lang="sl",
                                            alt=Alternative(
                                                var_lemmas={Source("WH"): "om."},
                                                var_words={Source("WH"): ("om. WH", 1)},
                                                main_cnt=1,
                                            ),
                                            word="аще",
                                            lemmas=["аще"],
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


def test_gr_dat():
    row = (
        ["к WGH", "къ"]
        + [""] * 2
        + ["13/69a30"]
        + ["om.", ""] * 2
        + [""] * 2
        + ["om."]
        + [""] * 4
        + ["Dat. Nt", "Dat."]
        + [""] * 8
        + ["bold|italic"]
        + ["1"] * 4
    )
    result = SortedDict()
    result = _agg_lemma(row, sl_sem.var, gr_sem.var, result)
    assert result == {
        "къ": {
            "": {
                "": {
                    "": {
                        "Dat.": {
                            ("к WGH", "Dat. Nt"): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("13/69a30"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("WGH"),
                                            alt=Alternative(
                                                main_lemma="om.",
                                                main_word="om.",
                                            ),
                                            word="к WGH",
                                            lemmas=["къ"],
                                        ),
                                        trans=Usage(
                                            lang="gr",
                                            var=Source("Nt"),
                                            word="Dat. Nt",
                                            lemmas=["Dat."],
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
        }
    }
