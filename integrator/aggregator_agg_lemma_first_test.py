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
