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
                            ("не\ue20dювьствьнь H", "ἀναίσθητος"): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("4/17d20"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("H"),
                                            alt=Alternative(
                                                main_lemma="не\ue20dѹвьнъ",
                                                var_lemmas={
                                                    Source("WG"): "не\ue20dѹ\ue205нъ"
                                                },
                                                main_word="не\ue20dювьнъ",
                                                var_words={
                                                    Source("WG"): (
                                                        "не\ue20dю\ue205но W не\ue20dю\ue205нь G",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="не\ue20dювьствьнь H",
                                            lemmas=["не\ue20dѹвьствьнъ"],
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
                                        idx=Index("4/17d20"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("WG"),
                                            alt=Alternative(
                                                main_lemma="не\ue20dѹвьнъ",
                                                var_lemmas={
                                                    Source("H"): "не\ue20dѹвьствьнъ"
                                                },
                                                main_word="не\ue20dювьнъ",
                                                var_words={
                                                    Source("H"): (
                                                        "не\ue20dювьствьнь H",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="не\ue20dю\ue205но W не\ue20dю\ue205нь G",
                                            lemmas=["не\ue20dѹ\ue205нъ"],
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
                                        idx=Index("34/156c21-d1"),
                                        orig=Usage(
                                            lang="sl",
                                            var=Source("G"),
                                            alt=Alternative(
                                                main_lemma="вѣра вел\ue205ꙗ",
                                                main_word="вѣра … вельꙗ",
                                            ),
                                            word="вѣрою хвальна G",
                                            lemmas=["вѣра хвальнъ", "вѣра хвальна"],
                                        ),
                                        trans=Usage(
                                            lang="gr",
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
