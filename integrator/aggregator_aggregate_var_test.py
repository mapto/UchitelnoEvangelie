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


def test_moudroust():
    row = (
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
        + ["1"] * 4
    )

    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
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
                                        Index("25/125a3"),
                                        Usage(
                                            "sl",
                                            Source("H"),
                                            "смѣрены\ue201 моудрост\ue205 H",
                                            [
                                                "мѫдрость",
                                                "съмѣр\ue201наꙗ мѫдрость",
                                            ],
                                            main_alt=Alternative(
                                                "съмѣромоудрост\ue205",
                                                ["съмѣромѫдрость"],
                                            ),
                                        ),
                                        Usage(
                                            "gr",
                                            Source("Ch"),
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


def test_smerumudrost():
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
        + ["om."]
        + [""] * 4
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
        + ["hl00:FFFCD5B4"]
        + ["1"] * 4
    )
    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
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
                                        Index("25/125a3"),
                                        Usage(
                                            "sl",
                                            Source("WG"),
                                            "смѣроумоудрост\ue205 WG",
                                            ["съмѣрѹмѫдрость"],
                                            main_alt=Alternative(
                                                "съмѣромоудрост\ue205",
                                                ["съмѣромѫдрость"],
                                            ),
                                            var_alt={
                                                Source("H"): Alternative(
                                                    "смѣрены\ue201 моудрост\ue205 H",
                                                    [
                                                        "съмѣр\ue201нъ",
                                                        "съмѣр\ue201наꙗ мѫдрость",
                                                    ],
                                                )
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
                                        Index("25/125a3"),
                                        Usage(
                                            "sl",
                                            Source("H"),
                                            "смѣрены\ue201 моудрост\ue205 H",
                                            [
                                                "съмѣр\ue201нъ",
                                                "съмѣр\ue201наꙗ мѫдрость",
                                            ],
                                            main_alt=Alternative(
                                                "съмѣромоудрост\ue205",
                                                ["съмѣромѫдрость"],
                                            ),
                                            var_alt={
                                                Source("WG"): Alternative(
                                                    "смѣроумоудрост\ue205 WG",
                                                    ["съмѣрѹмѫдрость"],
                                                )
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
        },
    }


def test_zlatoust():
    rows = [
        [
            "\ue205ѡⷩа ꙁлаⷮꙋстаго W \ue205ѡана ꙁлаⷮꙋстаго H",
            "\ue205оанъ",
            "\ue205оанъ ꙁлатоѹстъ WH",
            "",
            "17/082c08",
            "ꙀЛАтооустааго",
            "ТОГОⷱⷤ ꙀЛА-",
            "ꙁлатоѹстъ",
        ]
        + [""] * 3
        + ["Ø"] * 2
        + [""] * 13
        + ["hl00:FFFFDBB6"]
        + ["1"] * 4,
        [
            "\ue205ѡⷩа ꙁлаⷮꙋстаго W \ue205ѡана ꙁлаⷮꙋстаго H",
            "ꙁлатоѹстъ WH",
            "\ue205оанъ ꙁлатоѹстъ WH",
            "",
            "17/082c08",
            "ꙀЛАтооустааго",
            "",
            "ꙁлатоѹстъ",
        ]
        + [""] * 3
        + ["Ø"] * 2
        + [""] * 13
        + ["hl00:FFFFDBB6"]
        + ["1"] * 4,
    ]

    result = aggregate(rows, sl_sem.var, gr_sem, SortedDict())
    assert result == {
        "ꙁлатоѹстъ": {
            "\ue205оанъ ꙁлатоѹстъ": {
                "": {
                    "": {
                        "Ø": {
                            (
                                "\ue205ѡана ꙁлаⷮꙋстаго H \ue205ѡⷩа ꙁлаⷮꙋстаго W",
                                "Ø",
                            ): SortedSet(
                                [
                                    Alignment(
                                        Index("17/82c8"),
                                        Usage(
                                            "sl",
                                            Source("WH"),
                                            "\ue205ѡана ꙁлаⷮꙋстаго H \ue205ѡⷩа ꙁлаⷮꙋстаго W",
                                            [
                                                "ꙁлатоѹстъ",
                                                "\ue205оанъ ꙁлатоѹстъ",
                                            ],
                                            main_alt=Alternative(
                                                word="ꙀЛАтооустааго",
                                                lemmas=["ꙁлатоѹстъ"],
                                            ),
                                        ),
                                        Usage("gr", word="Ø", lemmas=["Ø"]),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
        "\ue205оанъ": {
            "\ue205оанъ ꙁлатоѹстъ": {
                "": {
                    "": {
                        "Ø": {
                            (
                                "\ue205ѡана ꙁлаⷮꙋстаго H \ue205ѡⷩа ꙁлаⷮꙋстаго W",
                                "Ø",
                            ): SortedSet(
                                [
                                    Alignment(
                                        Index("17/82c8"),
                                        Usage(
                                            "sl",
                                            Source("WH"),
                                            "\ue205ѡана ꙁлаⷮꙋстаго H \ue205ѡⷩа ꙁлаⷮꙋстаго W",
                                            [
                                                "\ue205оанъ",
                                                "\ue205оанъ ꙁлатоѹстъ",
                                            ],
                                            main_alt=Alternative(
                                                word="ꙀЛАтооустааго",
                                                lemmas=["ꙁлатоѹстъ"],
                                            ),
                                        ),
                                        Usage("gr", word="Ø", lemmas=["Ø"]),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
    }
