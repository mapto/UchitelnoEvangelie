from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import STYLE_COL
from config import FROM_LANG, TO_LANG

from model import Alternative, Index, Source, Alignment, Usage
from semantics import MainLangSemantics, VarLangSemantics
from aggregator import LAST_LEMMA, _agg_lemma

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
    result = _agg_lemma(
        row, gr_sem.var, sl_sem, result, LAST_LEMMA, Source("Ch"), "хлѣбъ"
    )
    assert result == {
        "хлѣбъ": {
            ("ἄρτους Ch", "хлѣбꙑ•"): SortedSet(
                [
                    Alignment(
                        Index("16/80a8"),
                        Usage(
                            "gr",
                            Source("Ch"),
                            "ἄρτους Ch",
                            ["ἄρτος"],
                            main_alt=Alternative("om.", "om."),
                        ),
                        Usage("sl", word="хлѣбꙑ•", lemmas=["хлѣбъ"]),
                    )
                ]
            )
        }
    }


def test_est_in_var_no_main():
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
        row,
        sl_sem.var,
        gr_sem,
        result,
        LAST_LEMMA,
        olemvar=Source("GH"),
        tlemma="Ø",
    )
    assert result == {
        "Ø": {
            ("\ue201сть GH", "Ø"): SortedSet(
                [
                    Alignment(
                        Index("7/47a6"),
                        Usage(
                            "sl",
                            Source("GH"),
                            "\ue201сть GH",
                            ["бꙑт\ue205", "", "gramm."],
                            main_alt=Alternative("om.", "om."),
                        ),
                        Usage("gr", word="Ø", lemmas=["Ø"]),
                    )
                ]
            )
        }
    }


def test_monogenis():
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
        row,
        sl_sem.var,
        gr_sem,
        result,
        LAST_LEMMA,
        Source("H"),
        "μονογενής",
    )
    assert result == {
        "μονογενής": {
            ("\ue201д\ue205нородоу H", "μονογενοῦς"): SortedSet(
                [
                    Alignment(
                        Index("1/W168a25"),
                        Usage(
                            "sl",
                            Source("H"),
                            "\ue201д\ue205нородоу H",
                            ["\ue201д\ue205нородъ"],
                            main_alt=Alternative(
                                "\ue201д\ue205но\ue20dедоу", "\ue201д\ue205но\ue20dѧдъ"
                            ),
                            var_alt={
                                Source("G"): Alternative(
                                    "\ue205но\ue20dедаго G", "\ue205но\ue20dѧдъ"
                                )
                            },
                        ),
                        Usage("gr", word="μονογενοῦς", lemmas=["μονογενής"]),
                        bold=True,
                        italic=True,
                    )
                ]
            )
        }
    }


def test_shestvie_last():
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
        LAST_LEMMA,
        Source("G"),
        "ὁδοιπορία",
    )
    assert result == {
        "ὁδοιπορία": {
            ("шьст\ue205ꙗ пꙋт\ue205 G", "ὁδοιπορίας"): SortedSet(
                [
                    Alignment(
                        Index("5/28d18"),
                        Usage(
                            "sl",
                            Source("G"),
                            "шьст\ue205ꙗ пꙋт\ue205 G",
                            ["шьст\ue205\ue201", "шьст\ue205\ue201 пѫт\ue205"],
                            main_alt=Alternative(
                                "поутошьств\ue205ꙗ", "пѫтошьств\ue205\ue201"
                            ),
                            var_alt={
                                Source("H"): Alternative(
                                    "шьств\ue205ꙗ пꙋт\ue205 H",
                                    "шьств\ue205\ue201 пѫт\ue205",
                                )
                            },
                        ),
                        Usage("gr", word="ὁδοιπορίας", lemmas=["ὁδοιπορία"]),
                    )
                ]
            )
        }
    }

    result = SortedDict()
    result = _agg_lemma(
        row,
        sl_sem.var,
        gr_sem,
        result,
        LAST_LEMMA,
        Source("H"),
        "ὁδοιπορία",
    )
    assert result == {
        "ὁδοιπορία": {
            ("шьств\ue205ꙗ пꙋт\ue205 H", "ὁδοιπορίας"): SortedSet(
                [
                    Alignment(
                        Index("5/28d18"),
                        Usage(
                            "sl",
                            Source("H"),
                            "шьств\ue205ꙗ пꙋт\ue205 H",
                            ["шьств\ue205\ue201", "шьств\ue205\ue201 пѫт\ue205"],
                            main_alt=Alternative(
                                "поутошьств\ue205ꙗ", "пѫтошьств\ue205\ue201"
                            ),
                            var_alt={
                                Source("G"): Alternative(
                                    "шьст\ue205ꙗ пꙋт\ue205 G",
                                    "шьст\ue205\ue201 пѫт\ue205",
                                )
                            },
                        ),
                        Usage("gr", word="ὁδοιπορίας", lemmas=["ὁδοιπορία"]),
                    )
                ]
            )
        }
    }


def test_put():
    row = (
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "пѫть GH",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/028d18",
            "поутошьств\ue205ꙗ",
            "",
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
        row, sl_sem.var, gr_sem, result, LAST_LEMMA, Source("H"), "ὁδοιπορία"
    )
    assert result == {
        "ὁδοιπορία": {
            (
                "шьств\ue205ꙗ пꙋт\ue205 H",
                "ὁδοιπορίας",
            ): SortedSet(
                [
                    Alignment(
                        Index("5/28d18"),
                        Usage(
                            "sl",
                            Source("H"),
                            "шьств\ue205ꙗ пꙋт\ue205 H",
                            ["пѫть", "шьств\ue205\ue201 пѫт\ue205"],
                            main_alt=Alternative(
                                "поутошьств\ue205ꙗ", "пѫтошьств\ue205\ue201"
                            ),
                            var_alt={
                                Source("G"): Alternative(
                                    "шьст\ue205ꙗ пꙋт\ue205 G",
                                    "шьст\ue205\ue201 пѫт\ue205",
                                ),
                            },
                        ),
                        Usage("gr", word="ὁδοιπορίας", lemmas=["ὁδοιπορία"]),
                    )
                ]
            )
        }
    }
