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

"""
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
                                            word="ход\ue205мъ спѣюще•",
                                            lemmas=[
                                                "спѣт\ue205",
                                                "≈ ход\ue205т\ue205 спѣѭще",
                                            ],
                                            var_alt={
                                                Source("WG"): Alternative(
                                                    "хⷪ҇домь спѣюще WG",
                                                    "ходомь спѣт\ue205",
                                                )
                                            },
                                        ),
                                        Usage(
                                            "gr",
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
"""


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
                                        Index("1/7c6"),
                                        Usage(
                                            "gr",
                                            word="om.",
                                            lemmas=["om."],
                                        ),
                                        Usage(
                                            "sl",
                                            word="аще",
                                            lemmas=["аще"],
                                            var_alt={
                                                Source("WH"): Alternative(
                                                    "om. WH", ["om."]
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
                                        Index("5/17b12"),
                                        Usage(
                                            "sl",
                                            word="грѣхъм\ue205",
                                            lemmas=["грѣхъ"],
                                        ),
                                        Usage(
                                            "gr",
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


def test_special_var():
    row = (
        [
            "проꙁрѣвшоѡмоу G  проꙁрѣвшоумоу H",
            "проꙁьрѣт\ue205",
            "#",
            "",
            "06/38b11",
            "\ue205сцѣленоумоу",
            "сповѣдат\ue205• нъ \ue205-",
            "\ue205цѣл\ue205т\ue205",
        ]
        + [""] * 3
        + ["τεθαραπευμένον", "θεραπεύω"]
        + [""] * 14
        + ["1"] * 4
    )
    result = SortedDict()
    result = _agg_lemma(row, sl_sem, gr_sem, result)
    assert result == {
        "\ue205цѣл\ue205т\ue205": {
            "": {
                "": {
                    "": {
                        "θεραπεύω": {
                            ("\ue205сцѣленоумоу", "τεθαραπευμένον"): SortedSet(
                                [
                                    Alignment(
                                        Index("6/38b11"),
                                        Usage(
                                            "sl",
                                            word="\ue205сцѣленоумоу",
                                            lemmas=["\ue205цѣл\ue205т\ue205"],
                                            var_alt={
                                                Source("GH"): Alternative(
                                                    "проꙁрѣвшоѡмоу G проꙁрѣвшоумоу H",
                                                    ["проꙁьрѣт\ue205"],
                                                    semantic="#",
                                                )
                                            },
                                        ),
                                        Usage(
                                            "gr",
                                            word="τεθαραπευμένον",
                                            lemmas=["θεραπεύω"],
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
    result = _agg_lemma(row, sl_sem, gr_sem, result, col=8, tlemma="ποιέω & κοινωνός")
    assert result == SortedDict(
        {
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205": SortedDict(
                {
                    "": SortedDict(
                        {
                            "": SortedDict(
                                {
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
                                                                "пр\ue205\ue20dестьн\ue205ц\ue205 G пр\ue205\ue20dестн\ue205ц\ue205 H",
                                                                [
                                                                    "пр\ue205\ue20dѧстьн\ue205къ",
                                                                    "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                                                ],
                                                                semantic="≈",
                                                            )
                                                        },
                                                    ),
                                                    Usage(
                                                        "gr",
                                                        word="ποιῆσαι κοινωνοὺς",
                                                        lemmas=[
                                                            "ποιέω & κοινωνός",
                                                            "≈ ποιέω κοινωνόν",
                                                        ],
                                                    ),
                                                    semantic="≈",
                                                )
                                            ]
                                        )
                                    }
                                }
                            )
                        }
                    )
                }
            )
        }
    )
