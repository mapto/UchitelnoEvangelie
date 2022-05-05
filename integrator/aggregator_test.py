from sortedcontainers import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL

from address import Index
from model import Usage, Source, Alternative

from semantics import MainLangSemantics, VarLangSemantics
from aggregator import (
    FIRST_LEMMA,
    LAST_LEMMA,
    present,
    _expand_and_aggregate,
    _agg_lemma,
)

# semantics change from September 2021
# with repetitions added (as if after merge)
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
    VarLangSemantics(TO_LANG, 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
    cnt_col=STYLE_COL + 3,
)


def test_present():
    sem = VarLangSemantics(lang=FROM_LANG, word=0, lemmas=[1, 2, 20, 21])
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "",
            "1/7b19",
            "вѣроують",
            "вьс\ue205 вѣроують",
            "вѣроват\ue205",
        ]
        + ([""] * 3)
        + ["πιστεύσωσι", "πιστεύω"]
        + ([""] * 13)
        + ["hl00"]
    )
    assert present(row, sem)
    row = (
        ["\ue205моуть GH", "ѩт\ue205"]
        + ([""] * 2)
        + ["1/7b19"]
        + ([""] * 20)
        + ["hl00"]
    )
    assert present(row, sem)
    row = ["\ue205моуть GH"] + ([""] * 3) + ["1/7b19"] + ([""] * 20) + ["hl00"]
    assert not present(row, sem)

    sem = VarLangSemantics(lang=TO_LANG, word=16, lemmas=[17, 18, 19])
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "",
            "1/7b19",
            "вѣроують",
            "вьс\ue205 вѣроують",
            "вѣроват\ue205",
        ]
        + ([""] * 3)
        + [
            "πιστεύσωσι",
            "πιστεύω",
        ]
        + ([""] * 13)
        + ["hl00"]
    )
    assert not present(row, sem)
    row = (
        ["\ue205моуть GH", "ѩт\ue205"]
        + ([""] * 2)
        + ["1/7b19"]
        + ([""] * 20)
        + ["hl00"]
    )
    assert not present(row, sem)

    row = (
        ([""] * 4)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με C", "ἐγώ"]
        + ([""] * 9)
    )
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )
    assert not present(row, sl_sem.var)
    assert present(row, sl_sem)
    assert not present(row, gr_sem)
    assert present(row, gr_sem.var)


def test_expand_and_aggregate():
    row = [""] * STYLE_COL
    dummy_sem = VarLangSemantics(lang="sl_var", word=0, lemmas=[1, 2, 19, 20])
    d = SortedDict()

    d = _expand_and_aggregate(row, None, dummy_sem, d)
    assert len(d) == 0

    d = _expand_and_aggregate(row, dummy_sem, None, d)
    assert len(d) == 0

    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )


def test_agg_lemma_missing_gr_main():
    # semantics change from September 2021
    # with repetitions added (as if after merge)
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
        VarLangSemantics(TO_LANG, 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

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
                    "хлѣбъ": {
                        ("ἄρτους Ch", "хлѣбꙑ•"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=16,
                                        alt=False,
                                        page=80,
                                        col="a",
                                        row=8,
                                        word="ἄρτους Ch",
                                    ),
                                    lang="gr",
                                    var=Source("Ch"),
                                    orig_alt=Alternative(
                                        main_lemma="om.",
                                        main_word="om.",
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
    result = _agg_lemma(row, gr_sem.var, sl_sem, result, -2, "ἄρτος", "хлѣбъ")
    assert result == {
        "хлѣбъ": {
            ("ἄρτους Ch", "хлѣбꙑ•"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=16,
                            alt=False,
                            page=80,
                            col="a",
                            row=8,
                            word="ἄρτους Ch",
                        ),
                        lang="gr",
                        var=Source("Ch"),
                        orig_alt=Alternative(
                            main_lemma="om.",
                            main_word="om.",
                        ),
                    )
                ]
            )
        }
    }


def test_agg_lemma_est_in_var_no_main():
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
        [12, 13, 14, 15],
        VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )
    row = (
        [
            "\ue201сть GH",
            "бꙑт\ue205",
            "",
            "gramm.",
            "07/47a06",
            "om.",
            "сътвор\ue205лъ",
            "om.",
        ]
        + [""] * 3
        + ["Ø"] * 2
        + [""] * 13
        + ["hl03"]
        + ["1"] * 4
    )
    result = SortedDict()
    result = _agg_lemma(
        row, sl_sem.var, gr_sem, result, LAST_LEMMA, olemma="бꙑт\ue205", tlemma="Ø"
    )
    assert result == {
        "Ø": {
            ("\ue201сть GH", "Ø"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=7,
                            alt=False,
                            page=47,
                            col="a",
                            row=6,
                            word="\ue201сть GH",
                        ),
                        lang="sl",
                        var=Source("GH"),
                        orig_alt=Alternative(
                            main_lemma="om.",
                            main_word="om.",
                        ),
                    )
                ]
            )
        }
    }
