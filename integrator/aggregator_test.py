from sortedcontainers import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL

from model import Index, Usage, Source, Alternative

from semantics import MainLangSemantics, VarLangSemantics
from aggregator import present, _expand_and_aggregate, _agg_lemma
from aggregator import LAST_LEMMA

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
    [12, 13, 14, 15],
    VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20], cnt_col=STYLE_COL + 4),
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


def test_agg_lemma_missing_gr_main():
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
                                    Usage(
                                        idx=Index(
                                            ch=16,
                                            alt=False,
                                            page=80,
                                            col="a",
                                            row=8,
                                            word="ἄρτους Ch",
                                            lemma="ἄρτος",
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
    }

    result = SortedDict()
    result = _agg_lemma(row, gr_sem.var, sl_sem, result, LAST_LEMMA, "ἄρτος", "хлѣбъ")
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
                            lemma="ἄρτος",
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
                            lemma="бꙑт\ue205",
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


def test_agg_lemma_hodom_spiti():
    # TODO: verify inputs, variant seems to be wrong
    row_main = (
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

    row_var = (
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
    _agg_lemma(row_main, sl_sem, gr_sem, result)
    # _agg_lemma(row_var, sl_sem.var, gr_sem, result)
    assert result == {
        # "": {"ходомь спѣт\ue205 WG": {"": {"": {}}}},
        "спѣт\ue205": {
            "≈ ход\ue205т\ue205 спѣѭще": {
                "": {
                    "": {
                        "προβαίνω": {
                            ("ход\ue205мъ спѣюще•", "προβαίνοντες"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=14,
                                            alt=False,
                                            page=72,
                                            col="d",
                                            row=18,
                                            end=Index(
                                                ch=14,
                                                alt=False,
                                                page=72,
                                                col="d",
                                                row=19,
                                                word="ход\ue205мъ спѣюще•",
                                                lemma="спѣт\ue205",
                                            ),
                                            word="ход\ue205мъ спѣюще•",
                                            lemma="спѣт\ue205",
                                        ),
                                        lang="sl",
                                        var=Source(""),
                                        orig_alt=Alternative(
                                            var_lemmas={
                                                Source("WG"): "ходомь спѣт\ue205"
                                            },
                                            var_words={
                                                Source("WG"): ("хⷪ҇домь спѣюще WG", 1)
                                            },
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


def test_agg_lemma_monogenis():
    row = (
        [
            "\ue205но\ue20dедаго G  \ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ H / \ue205но\ue20dѧдъ G",
        ]
        + [""] * 2
        + [
            "1/W168a25",
            "\ue201д\ue205но\ue20dедоу",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 13
        + ["bold|italic"]
        + ["1"] * 4
    )
    result = SortedDict()
    result = _agg_lemma(
        row, sl_sem.var, gr_sem, result, LAST_LEMMA, "днородъ", "μονογενής"
    )
    assert result == {
        "μονογενής": {
            ("\ue201д\ue205нородоу H", "μονογενοῦς"): SortedSet(
                [
                    Usage(
                        idx=Index(
                            ch=1,
                            alt=True,
                            page=168,
                            col="a",
                            row=25,
                            bold=True,
                            italic=True,
                            word="\ue201д\ue205нородоу H",
                            lemma="\ue201д\ue205нородъ",
                        ),
                        lang="sl",
                        var=Source("H"),
                        orig_alt=Alternative(
                            main_lemma="\ue201д\ue205но\ue20dѧдъ",
                            var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
                            main_word="\ue201д\ue205но\ue20dедоу",
                            var_words={Source("G"): ("\ue205но\ue20dедаго G", 1)},
                        ),
                    )
                ]
            )
        }
    }
