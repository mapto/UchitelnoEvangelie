from sortedcontainers import SortedDict, SortedSet, SortedSet  # type: ignore

from config import TO_LANG
from model import Alternative, Counter, Index, Source, Usage


def test_dict_counts_ipercliso():
    d = SortedDict(
        {
            "ὑπερβλύω": SortedDict(
                {
                    "прѣ\ue205сто\ue20d\ue205т\ue205": {
                        ("ὑπερβλύζων", "прѣ\ue205сто\ue20dе",): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        word="ὑπερβλύζων",
                                    ),
                                    lang=TO_LANG,
                                    var="C",
                                    orig_alt=Alternative("ὑπερκλύζω"),
                                )
                            ]
                        )
                    },
                    "\ue205сто\ue20dен\ue205\ue201": {
                        ("ὑπερβλύσαι", "\ue205сто\ue20dен\ue205\ue205",): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        word="ὑπερβλύσαι",
                                    ),
                                    lang=TO_LANG,
                                    var="C",
                                    orig_alt=Alternative("ὑπερκλύζω"),
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
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        word="ὑπερκλύζων",
                                    ),
                                    lang=TO_LANG,
                                    orig_alt=Alternative(var_lemmas={"C": "ὑπερβλύω"}),
                                )
                            ]
                        )
                    },
                    "\ue205сто\ue20dен\ue205\ue201": {
                        ("ὑπερκλύσαι", "\ue205сто\ue20dен\ue205\ue205",): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        word="ὑπερκλύσαι",
                                    ),
                                    lang=TO_LANG,
                                    orig_alt=Alternative(var_lemmas={"C": "ὑπερβλύω"}),
                                )
                            ]
                        )
                    },
                }
            ),
        }
    )
    c = Counter.get_dict_counts(d)
    assert (4, 0) == c.get_counts(True)
    assert (2, 2) == c.get_counts(False)


def test_dict_counts_monogenis():
    d = {
        "μονογενής": {
            "": {
                "": {
                    "\ue201д\ue205нородъ": {
                        ("μονογενοῦς", "\ue201д\ue205нородоу"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="a",
                                        row=25,
                                        word="μονογενοῦς",
                                    ),
                                    lang=TO_LANG,
                                    var="H",
                                    trans_alt=Alternative(
                                        "\ue201д\ue205но\ue20dѧдъ",
                                        {"G": "\ue205но\ue20dѧдъ"},
                                    ),
                                )
                            ]
                        )
                    },
                    "\ue201д\ue205но\ue20dѧдъ": {
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедаго"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="a",
                                        row=28,
                                        word="μονογενοῦς",
                                    ),
                                    lang=TO_LANG,
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедоу"): SortedSet(
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
                                        word="μονογενοῦς",
                                    ),
                                    lang=TO_LANG,
                                    trans_alt=Alternative(
                                        var_lemmas={
                                            "H": "\ue201д\ue205нородъ",
                                            "G": "\ue205но\ue20dѧдъ",
                                        }
                                    ),
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue201д\ue205но\ue20dедѣмь"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=False,
                                        page=4,
                                        col="c",
                                        row=15,
                                        word="μονογενοῦς",
                                    ),
                                    lang=TO_LANG,
                                    var="WH",
                                    trans_alt=Alternative(
                                        "\ue205но\ue20dѧдъ", {"G": "\ue205но\ue20dѧдъ"}
                                    ),
                                )
                            ]
                        ),
                        ("μονογενὴς", "\ue201д\ue205но\ue20dеды"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=False,
                                        page=5,
                                        col="a",
                                        row=4,
                                        word="μονογενὴς",
                                    ),
                                    lang=TO_LANG,
                                    var="WH",
                                    trans_alt=Alternative(
                                        "\ue205но\ue20dѧдъ ",
                                        {"G": "\ue205но\ue20dѧдъ "},
                                    ),
                                )
                            ]
                        ),
                    },
                    "\ue205но\ue20dѧдъ": {
                        ("μονογενοῦς", "Ø"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=False,
                                        page=4,
                                        col="c",
                                        row=15,
                                        word="μονογενοῦς",
                                    ),
                                    lang=TO_LANG,
                                    var="G",
                                    trans_alt=Alternative(
                                        var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}
                                    ),
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue205но\ue20dадѣмь"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=False,
                                        page=4,
                                        col="c",
                                        row=15,
                                        word="μονογενοῦς",
                                    ),
                                    lang=TO_LANG,
                                    trans_alt=Alternative(
                                        {"WH": "\ue201д\ue205но\ue20dѧдъ"}
                                    ),
                                )
                            ]
                        ),
                        ("μονογενοῦς", "\ue205но\ue20dедаго"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="a",
                                        row=25,
                                        word="μονογενοῦς",
                                    ),
                                    lang=TO_LANG,
                                    var="G",
                                    trans_alt=Alternative(
                                        "\ue201д\ue205но\ue20dѧдъ",
                                        {"H": "\ue201д\ue205нородъ"},
                                    ),
                                )
                            ]
                        ),
                        ("μονογενὴς", "\ue205но\ue20dадꙑ\ue205"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=False,
                                        page=5,
                                        col="a",
                                        row=4,
                                        word="μονογενὴς",
                                    ),
                                    lang=TO_LANG,
                                    trans_alt=Alternative(
                                        var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}
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
    assert (4, 3) == c.get_counts(True)
    assert (5, 0) == c.get_counts(False)

def test_dict_counts_prichatnik_biti():
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
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="c",
                                            row=21,
                                            end=Index(
                                                ch=5,
                                                alt=False,
                                                page=28,
                                                col="d",
                                                row=1,
                                                word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            ),
                                            word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                        ),
                                        lang="sl",
                                        orig_alt=Alternative(
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
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="c",
                                            row=21,
                                            end=Index(
                                                ch=5,
                                                alt=False,
                                                page=28,
                                                col="d",
                                                row=1,
                                                word="пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                            ),
                                            word="пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                        ),
                                        lang="sl",
                                        var=Source("GH"),
                                        orig_alt=Alternative(
                                            main_lemma="пр\ue205\ue20dьтьн\ue205къ быт\ue205",
                                            main_word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                        ),
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
    # assert (1, 0) == c.get_counts(True)
    assert (1, 0) == c.get_counts(False)
