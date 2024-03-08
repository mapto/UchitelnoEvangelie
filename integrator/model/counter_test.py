from sortedcontainers import SortedDict, SortedSet, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from model import Alternative, Counter, Index, Source, Alignment, Usage


def test_dict_ipercliso():
    d = SortedDict(
        {
            "ὑπερβλύω": SortedDict(
                {
                    "прѣ\ue205сто\ue20d\ue205т\ue205": {
                        (
                            "ὑπερβλύζων",
                            "прѣ\ue205сто\ue20dе",
                        ): SortedSet(
                            [
                                Alignment(
                                    Index("1/W168c17"),
                                    Usage(
                                        TO_LANG,
                                        Source("Cs"),
                                        main_alt=Alternative(lemma="ὑπερκλύζω"),
                                        word="ὑπερβλύζων",
                                        lemmas=["ὑπερβλύω"],
                                    ),
                                    Usage(
                                        FROM_LANG,
                                        word="прѣ\ue205сто\ue20dе",
                                        lemmas=["прѣ\ue205сто\ue20d\ue205т\ue205"],
                                    ),
                                )
                            ]
                        )
                    },
                    "\ue205сто\ue20dен\ue205\ue201": {
                        (
                            "ὑπερβλύσαι",
                            "\ue205сто\ue20dен\ue205\ue205",
                        ): SortedSet(
                            [
                                Alignment(
                                    Index("1/W168c17"),
                                    Usage(
                                        TO_LANG,
                                        Source("Cs"),
                                        main_alt=Alternative(lemma="ὑπερκλύζω"),
                                        word="ὑπερβλύσαι",
                                        lemmas=["ὑπερβλύω"],
                                    ),
                                    Usage(
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
                        (
                            "ὑπερκλύζων",
                            "прѣ\ue205сто\ue20dе",
                        ): SortedSet(
                            [
                                Alignment(
                                    Index("1/W168c17"),
                                    Usage(
                                        TO_LANG,
                                        var_alt={"Cs": Alternative(lemma="ὑπερβλύω")},
                                        word="ὑπερκλύζων",
                                        lemmas=["ὑπερκλύζω"],
                                    ),
                                    Usage(
                                        FROM_LANG,
                                        word="прѣ\ue205сто\ue20dе",
                                        lemmas=["прѣ\ue205сто\ue20d\ue205т\ue205"],
                                    ),
                                )
                            ]
                        )
                    },
                    "\ue205сто\ue20dен\ue205\ue201": {
                        (
                            "ὑπερκλύσαι",
                            "\ue205сто\ue20dен\ue205\ue205",
                        ): SortedSet(
                            [
                                Alignment(
                                    Index("1/W168c17"),
                                    Usage(
                                        TO_LANG,
                                        var_alt={"Cs": Alternative("ὑπερβλύω")},
                                        word="ὑπερκλύσαι",
                                        lemmas=["ὑπερκλύζω"],
                                    ),
                                    Usage(
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
                                Alignment(
                                    Index("1/W168a25"),
                                    Usage(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    Usage(
                                        FROM_LANG,
                                        Source("H"),
                                        main_alt=Alternative(
                                            lemma="\ue201д\ue205но\ue20dѧдъ"
                                        ),
                                        var_alt={
                                            "G": Alternative(lemma="\ue205но\ue20dѧдъ")
                                        },
                                    ),
                                )
                            ]
                        )
                    },
                    "\ue201д\ue205но\ue20dѧдъ": {
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедаго"): SortedSet(
                            [
                                Alignment(
                                    Index("1/W168a28"),
                                    Usage(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедоу"): SortedSet(
                            [
                                Alignment(
                                    Index("1/W168a25"),
                                    Usage(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    Usage(
                                        FROM_LANG,
                                        var_alt={
                                            "H": Alternative(
                                                lemma="\ue201д\ue205нородъ"
                                            ),
                                            "G": Alternative(lemma="\ue205но\ue20dѧдъ"),
                                        },
                                    ),
                                    bold=True,
                                    italic=True,
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедѣмь"): SortedSet(
                            [
                                Alignment(
                                    Index("1/4c15"),
                                    Usage(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    Usage(
                                        FROM_LANG,
                                        Source("WH"),
                                        main_alt=Alternative(lemma="\ue205но\ue20dѧдъ"),
                                        var_alt={
                                            "G": Alternative(lemma="\ue205но\ue20dѧдъ")
                                        },
                                    ),
                                )
                            ]
                        ),
                        ("μονογενὴς", "\ue201д\ue205но\ue20dеды"): SortedSet(
                            [
                                Alignment(
                                    Index("1/5a4"),
                                    Usage(
                                        TO_LANG,
                                        word="μονογενὴς",
                                    ),
                                    Usage(
                                        FROM_LANG,
                                        Source("WH"),
                                        main_alt=Alternative(
                                            lemma="\ue205но\ue20dѧдъ "
                                        ),
                                        var_alt={
                                            "G": Alternative(lemma="\ue205но\ue20dѧдъ ")
                                        },
                                    ),
                                )
                            ]
                        ),
                    },
                    "\ue205но\ue20dѧдъ": {
                        ("μονογενοῦς", "Ø"): SortedSet(
                            [
                                Alignment(
                                    Index("1/4c15"),
                                    Usage(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    Usage(
                                        FROM_LANG,
                                        Source("G"),
                                        var_alt={
                                            "WH": Alternative(
                                                lemma="\ue201д\ue205но\ue20dѧдъ"
                                            )
                                        },
                                    ),
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue205но\ue20dадѣмь"): SortedSet(
                            [
                                Alignment(
                                    Index("1/4c15"),
                                    Usage(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    Usage(
                                        FROM_LANG,
                                        var_alt={
                                            "WH": Alternative(
                                                lemma="\ue201д\ue205но\ue20dѧдъ"
                                            )
                                        },
                                    ),
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue205но\ue20dедаго"): SortedSet(
                            [
                                Alignment(
                                    Index("1/W168a25"),
                                    Usage(
                                        TO_LANG,
                                        word="μονογενοῦς",
                                    ),
                                    Usage(
                                        FROM_LANG,
                                        Source("G"),
                                        main_alt=Alternative(
                                            lemma="\ue201д\ue205но\ue20dѧдъ"
                                        ),
                                        var_alt={
                                            "H": Alternative("\ue201д\ue205нородъ")
                                        },
                                    ),
                                )
                            ]
                        ),
                        ("μονογενὴς", "\ue205но\ue20dадꙑ\ue205"): SortedSet(
                            [
                                Alignment(
                                    Index("1/5a4"),
                                    Usage(
                                        TO_LANG,
                                        word="μονογενὴς",
                                    ),
                                    Usage(
                                        FROM_LANG,
                                        var_alt={
                                            "WH": Alternative(
                                                lemma="\ue201д\ue205но\ue20dѧдъ"
                                            )
                                        },
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
                                    Alignment(
                                        Index("5/28c21-d1"),
                                        Usage("sl",
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
                                    Alignment(
                                        Index("5/28c21-d1"),
                                        Usage("sl",
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
