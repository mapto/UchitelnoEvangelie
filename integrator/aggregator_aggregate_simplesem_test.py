from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import FROM_LANG, TO_LANG
from config import FROM_LANG
from const import STYLE_COL

from model import Alternative, Index, Source, Alignment, Usage
from semantics import MainLangSemantics, VarLangSemantics
from aggregator import aggregate


def test_monogenis():
    # simplified semantics
    sl_sem = MainLangSemantics(
        FROM_LANG,
        5,
        [7],
        VarLangSemantics(FROM_LANG, 0, [1], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        TO_LANG,
        11,
        [12],
        VarLangSemantics(TO_LANG, 16, [17, 18], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

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
        + [""] * 14
        + ["1"] * 4
    )

    result = SortedDict()
    result = aggregate([row], sl_sem, gr_sem, result)
    assert result == {
        "\ue201д\ue205но\ue20dѧдъ": {
            "μονογενής": {
                ("\ue201д\ue205но\ue20dедоу", "μονογενοῦς"): SortedSet(
                    [
                        Alignment(
                            Index("1/W168a25"),
                            Usage(
                                FROM_LANG,
                                alt=Alternative(
                                    var_lemmas={
                                        Source("H"): "\ue201д\ue205нородъ",
                                        Source("G"): "\ue205но\ue20dѧдъ",
                                    },
                                    var_words={
                                        Source("H"): ("\ue201д\ue205нородоу H", 1),
                                        Source("G"): ("\ue205но\ue20dедаго G", 1),
                                    },
                                ),
                                word="\ue201д\ue205но\ue20dедоу",
                                lemmas=["\ue201д\ue205но\ue20dѧдъ"],
                            ),
                            Usage(lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]),
                        )
                    ]
                )
            }
        }
    }

    result = SortedDict()
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "\ue201д\ue205нородъ": {
            "μονογενής": {
                ("\ue201д\ue205нородоу H", "μονογενοῦς"): SortedSet(
                    [
                        Alignment(
                            Index("1/W168a25"),
                            Usage(
                                "sl",
                                var=Source("H"),
                                alt=Alternative(
                                    main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                    var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
                                    main_word="\ue201д\ue205но\ue20dедоу",
                                    var_words={
                                        Source("G"): ("\ue205но\ue20dедаго G", 1)
                                    },
                                ),
                                word="\ue201д\ue205нородоу H",
                                lemmas=["\ue201д\ue205нородъ"],
                            ),
                            Usage(lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]),
                        )
                    ]
                )
            }
        },
        "\ue205но\ue20dѧдъ": {
            "μονογενής": {
                ("\ue205но\ue20dедаго G", "μονογενοῦς"): SortedSet(
                    [
                        Alignment(
                            Index("1/W168a25"),
                            Usage(
                                "sl",
                                var=Source("G"),
                                alt=Alternative(
                                    main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                    var_lemmas={Source("H"): "\ue201д\ue205нородъ"},
                                    main_word="\ue201д\ue205но\ue20dедоу",
                                    var_words={
                                        Source("H"): ("\ue201д\ue205нородоу H", 1)
                                    },
                                ),
                                word="\ue205но\ue20dедаго G",
                                lemmas=["\ue205но\ue20dѧдъ"],
                            ),
                            Usage(lang="gr", word="μονογενοῦς", lemmas=["μονογενής"]),
                        )
                    ]
                )
            }
        },
    }
