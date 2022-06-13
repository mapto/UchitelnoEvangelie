from sortedcontainers import SortedDict, SortedSet, SortedSet  # type: ignore

from const import STYLE_COL
from config import FROM_LANG, TO_LANG
from model import Alternative, Counter, Index, Source, Usage, UsageContent

from aggregator import aggregate
from setup import MainLangSemantics, VarLangSemantics


def test_dict_ipercliso():
    d = SortedDict(
        {
            "ὑπερβλύω": SortedDict(
                {
                    "прѣ\ue205сто\ue20d\ue205т\ue205": {
                        ("ὑπερβλύζων", "прѣ\ue205сто\ue20dе",): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/W168c17"),
                                    UsageContent(
                                        TO_LANG,
                                        Source("C"),
                                        alt=Alternative("ὑπερκλύζω"),
                                        word="ὑπερβλύζων",
                                        lemmas=["ὑπερβλύω"],
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        word="прѣ\ue205сто\ue20dе",
                                        lemmas=["прѣ\ue205сто\ue20d\ue205т\ue205"]
                                    )
                                )
                            ]
                        )
                    },
                    "\ue205сто\ue20dен\ue205\ue201": {
                        ("ὑπερβλύσαι", "\ue205сто\ue20dен\ue205\ue205",): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/W168c17"),
                                    UsageContent(
                                        TO_LANG,
                                        Source("C"),
                                        alt=Alternative("ὑπερκλύζω"),
                                        word="ὑπερβλύσαι",
                                        lemmas=["ὑπερβλύω"],
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        word="\ue205сто\ue20dен\ue205\ue205",
                                        lemmas=["\ue205сто\ue20dен\ue205\ue201"]
                                    )
                                )
                            ]
                        )
                    },
                }
            ),
            "ὑπερκλύζω": SortedDict(
                {
                    "прѣ\ue205сто\ue20d\ue205т\ue205": {
                        ("ὑπερκλύζων", "прѣ\ue205сто\ue20dе",): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/W168c17"),
                                    UsageContent(
                                        TO_LANG,
                                        alt=Alternative(var_lemmas={"C": "ὑπερβλύω"}),
                                        word="ὑπερκλύζων",
                                        lemmas=["ὑπερκλύζω"],
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        word="прѣ\ue205сто\ue20dе",
                                        lemmas=["прѣ\ue205сто\ue20d\ue205т\ue205"]
                                    )
                                )
                            ]
                        )
                    },
                    "\ue205сто\ue20dен\ue205\ue201": {
                        ("ὑπερκλύσαι", "\ue205сто\ue20dен\ue205\ue205",): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/W168c17"),
                                    UsageContent(
                                        TO_LANG,
                                        alt=Alternative(var_lemmas={"C": "ὑπερβλύω"}),
                                        word="ὑπερκλύσαι",
                                        lemmas=["ὑπερκλύζω"],
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        word="\ue205сто\ue20dен\ue205\ue205",
                                        lemmas=["\ue205сто\ue20dен\ue205\ue201"]
                                    )
                                )
                            ]
                        )
                    },
                }
            ),
        }
    )
    c = Counter.get_dict_counts(d)
    # assert (4, 0) == c.get_counts(True)
    assert (2, 2) == c.get_counts(False)


def test_dict_monogenis():
    """
    d = {
        "μονογενής": {
            "": {
                "": {
                    "\ue201д\ue205нородъ": {
                        ("μονογενοῦς", "\ue201д\ue205нородоу"): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/W168a25"),
                                    UsageContent(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        Source("H"),
                                        alt=Alternative(
                                            "\ue201д\ue205но\ue20dѧдъ",
                                            {"G": "\ue205но\ue20dѧдъ"},
                                        ),
                                    ),
                                )
                            ]
                        )
                    },
                    "\ue201д\ue205но\ue20dѧдъ": {
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедаго"): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/W168a28"),
                                    UsageContent(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедоу"): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/W168a25"),
                                    UsageContent(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        alt=Alternative(
                                            var_lemmas={
                                                "H": "\ue201д\ue205нородъ",
                                                "G": "\ue205но\ue20dѧдъ",
                                            }
                                        ),
                                    ),
                                    bold=True,
                                    italic=True,
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедѣмь"): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/4c15"),
                                    UsageContent(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        Source("WH"),
                                        alt=Alternative(
                                            "\ue205но\ue20dѧдъ",
                                            {"G": "\ue205но\ue20dѧдъ"},
                                        ),
                                    ),
                                )
                            ]
                        ),
                        ("μονογενὴς", "\ue201д\ue205но\ue20dеды"): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/5a4"),
                                    UsageContent(
                                        TO_LANG,
                                        word="μονογενὴς",
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        Source("WH"),
                                        alt=Alternative(
                                            "\ue205но\ue20dѧдъ ",
                                            {"G": "\ue205но\ue20dѧдъ "},
                                        ),
                                    ),
                                )
                            ]
                        ),
                    },
                    "\ue205но\ue20dѧдъ": {
                        ("μονογενοῦς", "Ø"): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/4c15"),
                                    UsageContent(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        Source("G"),
                                        alt=Alternative(
                                            var_lemmas={
                                                "WH": "\ue201д\ue205но\ue20dѧдъ"
                                            }
                                        ),
                                    ),
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue205но\ue20dадѣмь"): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/4c15"),
                                    UsageContent(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        alt=Alternative(
                                            var_lemmas={
                                                "WH": "\ue201д\ue205но\ue20dѧдъ"
                                            }
                                        ),
                                    ),
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue205но\ue20dедаго"): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/W168a25"),
                                    UsageContent(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        Source("G"),
                                        alt=Alternative(
                                            "\ue201д\ue205но\ue20dѧдъ",
                                            {"H": "\ue201д\ue205нородъ"},
                                        ),
                                    ),
                                )
                            ]
                        ),
                        ("μονογενὴς", "\ue205но\ue20dадꙑ\ue205"): SortedSet(
                            [
                                Usage(
                                    Index.unpack("1/5a4"),
                                    UsageContent(
                                        TO_LANG,
                                        word="μονογενὴς",
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        alt=Alternative(
                                            var_lemmas={
                                                "WH": "\ue201д\ue205но\ue20dѧдъ"
                                            }
                                        ),
                                    ),
                                )
                            ]
                        ),
                    },
                }
            }
        }
    }
    """ 
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

    rows = [['\ue201д\ue205нородоу H', '\ue201д\ue205нородъ', '', '', '1/W168a34', '\ue201д\ue205но\ue20dедоу', 'бѣ \ue205мѣт\ue205 \ue201д\ue205но\ue20dедоу', '\ue201д\ue205но\ue20dѧдъ', '', '', '', 'μονογενῆ', 'μονογενής', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '1', '1', '1'],
    ['', '', '', '', '1/W168a28', '\ue201д\ue205но\ue20dедаго', 'цⷭ҇ре \ue201д\ue205но\ue20dедаго ѡтрока ѡ\ue010\ue20dа•', '\ue201д\ue205но\ue20dѧдъ', '', '', '', 'μονογενοῦς', 'μονογενής', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '1', '1', '1'],
    ['\ue205но\ue20dедаго G  \ue201д\ue205нородоу H', '\ue201д\ue205нородъ H / \ue205но\ue20dѧдъ G', '', '', '1/W168a25', '\ue201д\ue205но\ue20dедоу', 'вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу', '\ue201д\ue205но\ue20dѧдъ', '', '', '', 'μονογενοῦς', 'μονογενής', '', '', '', '', '', '', '', '', '', '', '', '', '', 'bold|italic', '1', '1', '1', '1'],
    ['\ue201д\ue205но\ue20dеды WH Ø G', '\ue201д\ue205но\ue20dѧдъ', '', '', '1/5a4', '\ue205но\ue20dадꙑ\ue205', 'нъ ꙗко б\ue010ъ• а \ue205но\ue20dадꙑ\ue205', '\ue205но\ue20dѧдъ', '', '', '', 'μονογενὴς', 'μονογενής', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '1', '1', '1'],
    ['\ue201д\ue205но\ue20dедѣмь WH Ø G', '\ue201д\ue205но\ue20dѧдъ', '', '', '1/4c15', '\ue205но\ue20dадѣмь', 'о \ue205но\ue20dадѣмь', '\ue205но\ue20dѧдъ', '', '', '', 'μονογενοῦς', 'μονογενής', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '1', '1', '1'],
    ]
    d = SortedDict()
    d = aggregate(rows, gr_sem, sl_sem, d)
    c = Counter.get_dict_counts(d)
    assert (5, 0) == c.get_counts(False)
    assert (5, 4) == c.get_counts(True)

"""
def test_dict_prichatnik_biti():
    d = {
        "бꙑт\ue205": {
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205": {
                "": {
                    "": {
                        "ποιέω κοινωνόν → ποιέω & κοινωνός": {
                            (
                                "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                "ποιῆσαι κοινωνοὺς",
                            ): SortedSet(
                                [
                                    Usage(
                                        Index.unpack("5/28c21-d1"),
                                        UsageContent("sl",
                                            alt=Alternative(
                                                var_lemmas={
                                                    Source(
                                                        "GH"
                                                    ): "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205"
                                                },
                                                var_words={
                                                    Source("GH"): (
                                                        "пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                                        1,
                                                    )
                                                },
                                            ),
                                            word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                        )
                                    )
                                ]
                            )
                        }
                    }
                }
            },
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205": {
                "": {
                    "": {
                        "ποιέω κοινωνόν → ποιέω & κοινωνός": {
                            (
                                "пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                "ποιῆσαι κοινωνοὺς",
                            ): SortedSet(
                                [
                                    Usage(
                                        Index.unpack("5/28c21-d1"),
                                        UsageContent("sl",
                                            Source("GH"),
                                            alt=Alternative(
                                                main_lemma="пр\ue205\ue20dьтьн\ue205къ быт\ue205",
                                                main_word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            ),
                                            word="пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                        )
                                    )
                                ]
                            )
                        }
                    }
                }
            },
        }
    }

    c = Counter.get_dict_counts(d)
    assert (1, 0) == c.get_counts(False)
"""