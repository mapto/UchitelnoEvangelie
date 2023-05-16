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


def test_pros_eis():
    row = (
        [""] * 4
        + ["35/162a10", "въ", "въ \ue205ер\ue205хѫ• съвы-", "въ", "въ + Acc."]
        + [""] * 2
        + ["om."] * 2
        + [""] * 3
        + ["εἰς MPePgPkR πρὸς PhPi", "εἰς MPePgPkR / πρός PhPi", "πρός + Acc. PhPi"]
        + [""] * 7
        + ["bold|italic"]
        + ["1"] * 4
    )
    result = SortedDict()
    result = aggregate([row], gr_sem.var, sl_sem, result)
    assert result == {
        "εἰς": {
            "": {
                "": {
                    "": {
                        "въ + Acc. → въ": {
                            ("εἰς MPePgPkR", "въ"): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("35/162a10"),
                                        orig=Usage(
                                            lang="gr",
                                            var=Source("MPePgPkR"),
                                            alt=Alternative(
                                                main_lemma="om.",
                                                var_lemmas={
                                                    Source("PhPi"): "πρός + Acc."
                                                },
                                                main_word="om.",
                                                var_words={
                                                    Source("PhPi"): ("πρὸς PhPi", 1)
                                                },
                                            ),
                                            word="εἰς MPePgPkR",
                                            lemmas=["εἰς"],
                                        ),
                                        trans=Usage(
                                            lang="sl",
                                            word="въ",
                                            lemmas=["въ", "въ + Acc."],
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
        "πρός": {
            "πρός + Acc.": {
                "": {
                    "": {
                        "въ + Acc. → въ": {
                            ("πρὸς PhPi", "въ"): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("35/162a10"),
                                        orig=Usage(
                                            lang="gr",
                                            var=Source("PhPi"),
                                            alt=Alternative(
                                                main_lemma="om.",
                                                var_lemmas={Source("MPePgPkR"): "εἰς"},
                                                main_word="om.",
                                                var_words={
                                                    Source("MPePgPkR"): (
                                                        "εἰς MPePgPkR",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="πρὸς PhPi",
                                            lemmas=["πρός", "πρός + Acc."],
                                        ),
                                        trans=Usage(
                                            lang="sl",
                                            word="въ",
                                            lemmas=["въ", "въ + Acc."],
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
