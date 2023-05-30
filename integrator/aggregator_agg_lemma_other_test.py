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
