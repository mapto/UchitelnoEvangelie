from sortedcontainers import SortedDict, SortedSet, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from model import Alternative, Counter, Index, Source, Usage, UsageContent


def test_dict_ipercliso():
    d = SortedDict(
        {
            "ὑπερβλύω": SortedDict(
                {
                    "прѣ\ue205сто\ue20d\ue205т\ue205": {
                        ("ὑπερβλύζων", "прѣ\ue205сто\ue20dе",): SortedSet(
                            [
                                Usage(
                                    Index("1/W168c17"),
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
                                        lemmas=["прѣ\ue205сто\ue20d\ue205т\ue205"],
                                    ),
                                )
                            ]
                        )
                    },
                    "\ue205сто\ue20dен\ue205\ue201": {
                        ("ὑπερβλύσαι", "\ue205сто\ue20dен\ue205\ue205",): SortedSet(
                            [
                                Usage(
                                    Index("1/W168c17"),
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
                                        lemmas=["\ue205сто\ue20dен\ue205\ue201"],
                                    ),
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
                                    Index("1/W168c17"),
                                    UsageContent(
                                        TO_LANG,
                                        alt=Alternative(var_lemmas={"C": "ὑπερβλύω"}),
                                        word="ὑπερκλύζων",
                                        lemmas=["ὑπερκλύζω"],
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        word="прѣ\ue205сто\ue20dе",
                                        lemmas=["прѣ\ue205сто\ue20d\ue205т\ue205"],
                                    ),
                                )
                            ]
                        )
                    },
                    "\ue205сто\ue20dен\ue205\ue201": {
                        ("ὑπερκλύσαι", "\ue205сто\ue20dен\ue205\ue205",): SortedSet(
                            [
                                Usage(
                                    Index("1/W168c17"),
                                    UsageContent(
                                        TO_LANG,
                                        alt=Alternative(var_lemmas={"C": "ὑπερβλύω"}),
                                        word="ὑπερκλύσαι",
                                        lemmas=["ὑπερκλύζω"],
                                    ),
                                    UsageContent(
                                        FROM_LANG,
                                        word="\ue205сто\ue20dен\ue205\ue205",
                                        lemmas=["\ue205сто\ue20dен\ue205\ue201"],
                                    ),
                                )
                            ]
                        )
                    },
                }
            ),
        }
    )
    c = Counter.get_dict_counts(d)
    assert str(c) == "(2, 2, 4, 0)"
    assert (4, 0) == c.get_counts(True)
    assert (2, 2) == c.get_counts(False)


def test_dict_monogenis():
    d = {
        "μονογενής": {
            "": {
                "": {
                    "\ue201д\ue205нородъ": {
                        ("μονογενοῦς", "\ue201д\ue205нородоу"): SortedSet(
                            [
                                Usage(
                                    Index("1/W168a25"),
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
                                    Index("1/W168a28"),
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
                                    Index("1/W168a25"),
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
                                    Index("1/4c15"),
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
                                    Index("1/5a4"),
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
                                    Index("1/4c15"),
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
                                    Index("1/4c15"),
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
                                    Index("1/W168a25"),
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
                                    Index("1/5a4"),
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
    c = Counter.get_dict_counts(d)
    assert str(c) == "(9, 0, 4, 5)"
    assert (4, 3) == c.get_counts(True)
    assert (4, 0) == c.get_counts(False)

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
                                        Index("5/28c21-d1"),
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
                                        Index("5/28c21-d1"),
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
