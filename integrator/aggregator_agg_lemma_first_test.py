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


def test_missing_gr_main():
    row = (
        [""] * 4
        + ["16/80a08", "хлѣбꙑ•", "ре\ue20dе хлѣбꙑ• не", "хлѣбъ"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 3
        + ["ἄρτους Ch", "ἄρτος"]
        + [""] * 9
        + ["1"] * 4
    )
    result = SortedDict()
    result = _agg_lemma(row, gr_sem.var, sl_sem, result)
    assert result == {
        "ἄρτος": {
            "": {
                "": {
                    "": {
                        "хлѣбъ": {
                            ("ἄρτους Ch", "хлѣбꙑ•"): SortedSet(
                                [
                                    Alignment(
                                        Index("16/80a8"),
                                        Usage(
                                            "gr",
                                            var=Source("Ch"),
                                            alt=Alternative(
                                                main_lemma="om.",
                                                main_word="om.",
                                            ),
                                            word="ἄρτους Ch",
                                            lemmas=["ἄρτος"],
                                        ),
                                        Usage(
                                            lang="sl", word="хлѣбꙑ•", lemmas=["хлѣбъ"]
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


def test_hodom_spiti():
    row = (
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "д\ue205мъ спѣюще•",
            "спѣт\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
        ]
        + [""] * 2
        + ["προβαίνοντες", "προβαίνω"]
        + [""] * 13
        + ["hl05"]
        + ["1"] * 4
    )

    result = SortedDict()
    _agg_lemma(row, sl_sem, gr_sem, result)
    # _agg_lemma(row_var, sl_sem.var, gr_sem, result)
    assert result == {
        "спѣт\ue205": {
            "≈ ход\ue205т\ue205 спѣѭще": {
                "": {
                    "": {
                        "προβαίνω": {
                            ("ход\ue205мъ спѣюще•", "προβαίνοντες"): SortedSet(
                                [
                                    Alignment(
                                        Index("14/72d18-19"),
                                        Usage(
                                            "sl",
                                            alt=Alternative(
                                                var_lemmas={
                                                    Source("WG"): "ходомь спѣт\ue205"
                                                },
                                                var_words={
                                                    Source("WG"): (
                                                        "хⷪ҇домь спѣюще WG",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="ход\ue205мъ спѣюще•",
                                            lemmas=[
                                                "спѣт\ue205",
                                                "≈ ход\ue205т\ue205 спѣѭще",
                                            ],
                                        ),
                                        Usage(
                                            lang="gr",
                                            word="προβαίνοντες",
                                            lemmas=["προβαίνω"],
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


def test_hodom_spiti_var():
    row = (
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "д\ue205мъ спѣюще•",
            "ход\ue205т\ue205 спѣт\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
        ]
        + [""] * 2
        + ["προβαίνοντες", "προβαίνω"]
        + [""] * 13
        + ["hl05"]
        + ["1"] * 4
    )

    result = SortedDict()
    _agg_lemma(row, sl_sem.var, gr_sem, result)
    # _agg_lemma(row_var, sl_sem.var, gr_sem, result)
    assert result == {
        "": {
            "ходомь спѣт\ue205 WG": {
                "": {
                    "": {
                        "προβαίνω": {
                            ("", "προβαίνοντες"): SortedSet(
                                [
                                    Alignment(
                                        Index("14/72d18-19"),
                                        Usage(
                                            "sl",
                                            alt=Alternative(
                                                var_lemmas={
                                                    Source("WG"): "ходомь спѣт\ue205"
                                                },
                                                var_words={
                                                    Source("WG"): (
                                                        "хⷪ҇домь спѣюще WG",
                                                        1,
                                                    )
                                                },
                                            ),
                                        ),
                                        Usage(
                                            lang="gr",
                                            word="προβαίνοντες",
                                            lemmas=["προβαίνω"],
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


def test_shestvie_first():
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
    result = _agg_lemma(row, sl_sem.var, gr_sem, result)
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
                                            Alternative(
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
            },
        },
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


def test_nechuvstven():
    row = (
        [
            "не\ue20dю\ue205но W  не\ue20dю\ue205нь G  не\ue20dювьствьнь H",
            "не\ue20dѹ\ue205нъ WG / не\ue20dѹвьствьнъ H",
        ]
        + [""] * 2
        + ["04/17d20", "не\ue20dювьнъ", "кою ꙗко не\ue20dю-", "не\ue20dѹвьнъ"]
        + [""] * 3
        + ["ἀναίσθητος", "ἀναίσθητος"]
        + [""] * 14
        + [1] * 4
    )
    result = SortedDict()
    result = _agg_lemma(row, sl_sem.var, gr_sem, result)
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
                                            lang="gr",
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
                                            lang="gr",
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


def test_greh():
    row = (
        [""] * 4
        + ["05/17b12", "грѣхъм\ue205", "оубо ꙗко грѣ-", "грѣхъ", "#"]
        + [""] * 2
        + ["υἱός"] * 2
        + [""] * 14
        + ["1"] * 4
    )
    result = SortedDict()
    result = _agg_lemma(row, sl_sem, gr_sem, result)
    assert result == {
        "грѣхъ": {
            "": {
                "": {
                    "": {
                        "# υἱός": {
                            ("грѣхъм\ue205", "υἱός"): SortedSet(
                                [
                                    Alignment(
                                        idx=Index("5/17b12"),
                                        orig=Usage(
                                            lang="sl",
                                            word="грѣхъм\ue205",
                                            lemmas=["грѣхъ"],
                                        ),
                                        trans=Usage(
                                            lang="gr",
                                            word="υἱός",
                                            lemmas=["# υἱός"],
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
