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
                                        Index("35/162a10"),
                                        Usage(
                                            "gr",
                                            Source("MPePgPkR"),
                                            "εἰς MPePgPkR",
                                            ["εἰς"],
                                            main_alt=Alternative("om.", "om."),
                                            var_alt={
                                                Source("PhPi"): Alternative(
                                                    "πρὸς PhPi", "πρός + Acc."
                                                )
                                            },
                                        ),
                                        Usage(
                                            "sl",
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
                                        Index("35/162a10"),
                                        Usage(
                                            "gr",
                                            Source("PhPi"),
                                            "πρὸς PhPi",
                                            ["πρός", "πρός + Acc."],
                                            main_alt=Alternative("om.", "om."),
                                            var_alt={
                                                Source("MPePgPkR"): Alternative(
                                                    "εἰς MPePgPkR",
                                                    "εἰς",
                                                )
                                            },
                                        ),
                                        Usage(
                                            "sl",
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


def test_nechuvan():
    row = (
        [
            "не\ue20dю\ue205но W  не\ue20dю\ue205нь G  не\ue20dювьствьнь H",
            "не\ue20dѹ\ue205нъ WG / не\ue20dѹвьствьнъ H",
        ]
        + [""] * 2
        + ["04/17d20", "не\ue20dювьнъ", "кою ꙗко не\ue20dю-", "не\ue20dѹвьнъ"]
        + [""] * 3
        + ["ἀναίσθητος"] * 2
        + [""] * 14
        + ["1"] * 4
    )
    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "не\ue20dѹвьствьнъ": {
            "": {
                "": {
                    "": {
                        "ἀναίσθητος": {
                            (
                                "не\ue20dювьствьнь H",
                                "ἀναίσθητος",
                            ): SortedSet(
                                [
                                    Alignment(
                                        Index("4/17d20"),
                                        Usage(
                                            "sl",
                                            Source("H"),
                                            "не\ue20dювьствьнь H",
                                            ["не\ue20dѹвьствьнъ"],
                                            main_alt=Alternative(
                                                word="не\ue20dювьнъ",
                                                lemma="не\ue20dѹвьнъ",
                                            ),
                                            var_alt={
                                                Source("W"): Alternative(
                                                    word="не\ue20dю\ue205но W",
                                                    lemma="не\ue20dѹ\ue205нъ",
                                                ),
                                                Source("G"): Alternative(
                                                    word="не\ue20dю\ue205нь G",
                                                    lemma="не\ue20dѹ\ue205нъ",
                                                ),
                                            },
                                        ),
                                        Usage(
                                            "gr",
                                            word="ἀναίσθητος",
                                            lemmas=["ἀναίσθητος"],
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            }
        },
        "не\ue20dѹ\ue205нъ": {
            "": {
                "": {
                    "": {
                        "ἀναίσθητος": {
                            (
                                "не\ue20dю\ue205но W не\ue20dю\ue205нь G",
                                "ἀναίσθητος",
                            ): SortedSet(
                                [
                                    Alignment(
                                        Index("4/17d20"),
                                        Usage(
                                            "sl",
                                            Source("WG"),
                                            "не\ue20dю\ue205но W не\ue20dю\ue205нь G",
                                            ["не\ue20dѹ\ue205нъ"],
                                            main_alt=Alternative(
                                                word="не\ue20dювьнъ",
                                                lemma="не\ue20dѹвьнъ",
                                            ),
                                            var_alt={
                                                Source("H"): Alternative(
                                                    word="не\ue20dювьствьнь H",
                                                    lemma="не\ue20dѹвьствьнъ",
                                                )
                                            },
                                        ),
                                        trans=Usage(
                                            "gr",
                                            word="ἀναίσθητος",
                                            lemmas=["ἀναίσθητος"],
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
                                                "съмѣромоудрост\ue205", "съмѣромѫдрость"
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


def test_vyara():
    row = (
        [
            "вѣрою хвальна G",
            "вѣра хвальнъ G",
            "вѣра хвальна G",
            "# G",
            "34/156c21-d01",
            "вѣра … вельꙗ",
            "твор\ue205• \ue205 вѣ-",
            "вѣра",
            "вѣра вел\ue205ꙗ",
            "#",
            "",
            "ἐγκώμιον μέγα",
            "ἐγκώμιον & μέγας",
            "ἐγκώμιον μέγα",
        ]
        + [""] * 12
        + ["hl05:FFFCE4D6|hl11:FFFCE4D6"]
        + ["1"] * 4
    )

    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "вѣра хвальнъ": {
            "вѣра хвальна": {
                "": {
                    "": {
                        "# ἐγκώμιον μέγα → ἐγκώμιον & μέγας": {
                            ("вѣрою хвальна G", "ἐγκώμιον μέγα"): SortedSet(
                                [
                                    Alignment(
                                        Index("34/156c21-d1"),
                                        Usage(
                                            "sl",
                                            Source("G"),
                                            "вѣрою хвальна G",
                                            ["вѣра хвальнъ", "вѣра хвальна"],
                                            main_alt=Alternative(
                                                "вѣра … вельꙗ",
                                                "вѣра вел\ue205ꙗ",
                                                semantic="#",
                                            ),
                                        ),
                                        Usage(
                                            "gr",
                                            word="ἐγκώμιον μέγα",
                                            lemmas=[
                                                "ἐγκώμιον & μέγας",
                                                "# ἐγκώμιον μέγα",
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


def test_vyara_inverse():
    row = (
        [
            "вѣрою хвальна G",
            "вѣра & хвальнъ G",
            "вѣра хвальна G",
            "# G",
            "34/156c21-d01",
            "вѣра … вельꙗ",
            "твор\ue205• \ue205 вѣ-",
            "вѣра & вел\ue205\ue205",
            "вѣра вел\ue205ꙗ",
            "#",
            "",
            "ἐγκώμιον μέγα",
            "ἐγκώμιον",
            "ἐγκώμιον μέγα",
        ]
        + [""] * 12
        + ["hl05:FFFCE4D6|hl11:FFFCE4D6"]
        + ["1"] * 4
    )
    result = SortedDict()
    result = aggregate([row], gr_sem, sl_sem, result)
    assert result == {
        "ἐγκώμιον": {
            "ἐγκώμιον μέγα": {
                "": {
                    "": {
                        "# вѣра вел\ue205ꙗ → вѣра & вел\ue205\ue205": {
                            ("ἐγκώμιον μέγα", "вѣра … вельꙗ"): SortedSet(
                                [
                                    Alignment(
                                        Index("34/156c21-d1"),
                                        Usage(
                                            "gr",
                                            word="ἐγκώμιον μέγα",
                                            lemmas=["ἐγκώμιον", "ἐγκώμιον μέγα"],
                                        ),
                                        Usage(
                                            "sl",
                                            word="вѣра … вельꙗ",
                                            lemmas=[
                                                "вѣра & вел\ue205\ue205",
                                                "вѣра вел\ue205ꙗ",
                                                "#",
                                            ],
                                            var_alt={
                                                Source("G"): Alternative(
                                                    "вѣрою хвальна G",
                                                    "вѣра хвальна",
                                                    semantic="#",
                                                )
                                            },
                                        ),
                                    )
                                ]
                            )
                        },
                        "# вѣра хвальна → вѣра & хвальнъ": {
                            ("ἐγκώμιον μέγα", "вѣрою хвальна G"): SortedSet(
                                [
                                    Alignment(
                                        Index("34/156c21-d1"),
                                        Usage(
                                            "gr",
                                            word="ἐγκώμιον μέγα",
                                            lemmas=["ἐγκώμιον", "ἐγκώμιον μέγα"],
                                        ),
                                        trans=Usage(
                                            "sl",
                                            Source("G"),
                                            "вѣрою хвальна G",
                                            ["вѣра & хвальнъ", "вѣра хвальна", "#"],
                                            main_alt=Alternative(
                                                "вѣра … вельꙗ",
                                                "вѣра вел\ue205ꙗ",
                                                semantic="#",
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
    }


def test_bozhii():
    row = (
        [
            "б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H",
            "бож\ue205\ue205",
            "",
            "",
            "1/7a4",
            "боꙁѣ",
            "о боꙁѣ словес\ue205•",
            "богъ",
            "Dat.",
            "",
            "",
            "Θεοῦ",
            "θεός",
            "Gen.",
        ]
        + [""] * 13
        + ["1"] * 4
    )
    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
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
                                            "sl",
                                            Source("WGH"),
                                            "б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G",
                                            ["бож\ue205\ue205"],
                                            main_alt=Alternative(
                                                word="боꙁѣ", lemma="богъ"
                                            ),
                                        ),
                                        trans=Usage(
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


"""
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
                                                lemma="ꙁлатоѹстъ",
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
                                                lemma="ꙁлатоѹстъ",
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
"""
