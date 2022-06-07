from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import FROM_LANG, TO_LANG
from config import FROM_LANG
from const import IDX_COL, STYLE_COL

from model import Index, Usage, Source, Alternative
from semantics import MainLangSemantics, VarLangSemantics
from aggregator import aggregate

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
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "бꙑт\ue205": {
            "": {
                "gramm.": {
                    "": {
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
                }
            }
        }
    }


def test_prichatnik_biti_sl():
    rows = [
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H "
            "боудемь W",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + [
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H "
            "боудемь W",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "боудоуть• \ue201же",
            "бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
            "",
            "",
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
    ]

    result = SortedDict()
    result = aggregate([rows[0]], sl_sem, gr_sem, result)
    assert result == {
        "пр\ue205\ue20dьтьн\ue205къ": {
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
                                                lemma="пр\ue205\ue20dьтьн\ue205къ",
                                            ),
                                            word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            lemma="пр\ue205\ue20dьтьн\ue205къ",
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
            }
        }
    }
    result = SortedDict()
    result = aggregate([rows[1]], sl_sem, gr_sem, result)
    assert result == {
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
                                                lemma="бꙑт\ue205",
                                            ),
                                            word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            lemma="бꙑт\ue205",
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
            }
        }
    }


def test_prichatnik_biti_sl_var():
    rows = [
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H боудемь W"
            "",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + ["ποιῆσαι κοινωνοὺς", "ποιέω & κοινωνός", "ποιέω κοινωνόν"]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H боудемь W",
            "бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "боудоуть• \ue201же",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + ["ποιῆσαι κοινωνοὺς", "ποιέω & κοινωνός", "ποιέω κοινωνόν"]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
    ]

    result = SortedDict()
    result = aggregate([rows[0]], sl_sem.var, gr_sem, result)
    assert result == {
        "пр\ue205\ue20dѧстьн\ue205къ": {
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
                                                lemma="пр\ue205\ue20dѧстьн\ue205къ",
                                            ),
                                            word="пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                            lemma="пр\ue205\ue20dѧстьн\ue205къ",
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
            }
        }
    }

    result = SortedDict()
    result = aggregate([rows[1]], sl_sem.var, gr_sem, result)
    assert result == {
        "бꙑт\ue205": {
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
                                                lemma="бꙑт\ue205",
                                            ),
                                            word="пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                            lemma="бꙑт\ue205",
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
            }
        }
    }


def test_prichatnik_biti_combined():
    rows = [
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H "
            "боудемь W",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + [
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H "
            "боудемь W",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "боудоуть• \ue201же",
            "бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
            "",
            "",
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
    ]

    result = SortedDict()
    result = aggregate([rows[1]], sl_sem, gr_sem, result)
    assert result == {
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
                                                lemma="бꙑт\ue205",
                                            ),
                                            word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            lemma="бꙑт\ue205",
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
            }
        }
    }

    rows_var = [
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H боудемь W"
            "",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + ["ποιῆσαι κοινωνοὺς", "ποιέω & κοινωνός", "ποιέω κοινωνόν"]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H боудемь W",
            "бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "боудоуть• \ue201же",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + ["ποιῆσαι κοινωνοὺς", "ποιέω & κοινωνός", "ποιέω κοινωνόν"]
        + [""] * 12
        + ["hl05|hl11"]
        + ["1"] * 4,
    ]

    result = aggregate([rows_var[1]], sl_sem.var, gr_sem, result)
    assert result == {
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
                                                lemma="бꙑт\ue205",
                                            ),
                                            word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                            lemma="бꙑт\ue205",
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
                                                lemma="бꙑт\ue205",
                                            ),
                                            word="пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G",
                                            lemma="бꙑт\ue205",
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


def test_monogenes():
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
    result = aggregate([row], sl_sem.var, gr_sem, result)
    assert result == {
        "\ue201д\ue205нородъ": {
            "": {
                "": {
                    "": {
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
                                            var_lemmas={
                                                Source("G"): "\ue205но\ue20dѧдъ"
                                            },
                                            main_word="\ue201д\ue205но\ue20dедоу",
                                            var_words={
                                                Source("G"): (
                                                    "\ue205но\ue20dедаго G",
                                                    1,
                                                )
                                            },
                                        ),
                                    )
                                ]
                            ),
                        }
                    }
                }
            }
        },
        "\ue205но\ue20dѧдъ": {
            "": {
                "": {
                    "": {
                        "μονογενής": {
                            ("\ue205но\ue20dедаго G", "μονογενοῦς"): SortedSet(
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
                                            word="\ue205но\ue20dедаго G",
                                            lemma="\ue205но\ue20dѧдъ",
                                        ),
                                        lang="sl",
                                        var=Source("G"),
                                        orig_alt=Alternative(
                                            main_lemma="\ue201д\ue205но\ue20dѧдъ",
                                            var_lemmas={
                                                Source("H"): "\ue201д\ue205нородъ"
                                            },
                                            main_word="\ue201д\ue205но\ue20dедоу",
                                            var_words={
                                                Source("H"): (
                                                    "\ue201д\ue205нородоу H",
                                                    1,
                                                )
                                            },
                                        ),
                                    )
                                ]
                            ),
                        }
                    }
                }
            }
        },
    }


def test_puteshestvie_sl_var():
    rows = [
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
        + ["1"] * 4,
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
        + ["1"] * 4,
    ]

    result = SortedDict()
    result = aggregate([rows[0]], sl_sem.var, gr_sem, result)
    assert result == {
        "шьств\ue205\ue201": {
            "шьств\ue205\ue201 пѫт\ue205": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            ("шьств\ue205ꙗ пꙋт\ue205 H", "ὁδοιπορίας"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="d",
                                            row=18,
                                            word="шьств\ue205ꙗ пꙋт\ue205 H",
                                            lemma="шьств\ue205\ue201",
                                        ),
                                        lang="sl",
                                        var=Source("H"),
                                        orig_alt=Alternative(
                                            main_lemma="пѫтошьств\ue205\ue201",
                                            var_lemmas={
                                                Source(
                                                    "G"
                                                ): "шьст\ue205\ue201 пѫт\ue205"
                                            },
                                            main_word="поутошьств\ue205ꙗ",
                                            var_words={
                                                Source("G"): (
                                                    "шьст\ue205ꙗ пꙋт\ue205 G",
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
        },
        "шьст\ue205\ue201": {
            "шьст\ue205\ue201 пѫт\ue205": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            ("шьст\ue205ꙗ пꙋт\ue205 G", "ὁδοιπορίας"): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="d",
                                            row=18,
                                            word="шьст\ue205ꙗ пꙋт\ue205 G",
                                            lemma="шьст\ue205\ue201",
                                        ),
                                        lang="sl",
                                        var=Source("G"),
                                        orig_alt=Alternative(
                                            main_lemma="пѫтошьств\ue205\ue201",
                                            var_lemmas={
                                                Source(
                                                    "H"
                                                ): "шьств\ue205\ue201 пѫт\ue205"
                                            },
                                            main_word="поутошьств\ue205ꙗ",
                                            var_words={
                                                Source("H"): (
                                                    "шьств\ue205ꙗ пꙋт\ue205 H",
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
        },
    }

    result = SortedDict()
    result = aggregate([rows[1]], sl_sem.var, gr_sem, result)
    assert result == {
        "пѫть": {
            "шьств\ue205\ue201 пѫт\ue205": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            (
                                "шьств\ue205ꙗ пꙋт\ue205 H шьст\ue205ꙗ пꙋт\ue205 G",
                                "ὁδοιπορίας",
                            ): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="d",
                                            row=18,
                                            word="шьств\ue205ꙗ пꙋт\ue205 H шьст\ue205ꙗ пꙋт\ue205 G",
                                            lemma="пѫть",
                                        ),
                                        lang="sl",
                                        var=Source("GH"),
                                        orig_alt=Alternative(
                                            main_lemma="пѫтошьств",
                                            var_lemmas={
                                                Source(
                                                    "H"
                                                ): "шьств\ue205\ue201 пѫт\ue205",
                                                Source(
                                                    "G"
                                                ): "шьст\ue205\ue201 пѫт\ue205",
                                            },
                                            main_word="поутошьствꙗ",
                                            var_words={
                                                Source("G"): (
                                                    "шьст\ue205ꙗ пꙋт\ue205 G",
                                                    1,
                                                ),
                                                Source("H"): (
                                                    "шьств\ue205ꙗ пꙋт\ue205 H",
                                                    1,
                                                ),
                                            },
                                        ),
                                    )
                                ]
                            )
                        }
                    }
                }
            },
            "шьст\ue205\ue201 пѫт\ue205": {
                "": {
                    "": {
                        "ὁδοιπορία": {
                            (
                                "шьств\ue205ꙗ пꙋт\ue205 H шьст\ue205ꙗ пꙋт\ue205 G",
                                "ὁδοιπορίας",
                            ): SortedSet(
                                [
                                    Usage(
                                        idx=Index(
                                            ch=5,
                                            alt=False,
                                            page=28,
                                            col="d",
                                            row=18,
                                            word="шьств\ue205ꙗ пꙋт\ue205 H шьст\ue205ꙗ пꙋт\ue205 G",
                                            lemma="пѫть",
                                        ),
                                        lang="sl",
                                        var=Source("GH"),
                                        orig_alt=Alternative(
                                            main_lemma="пѫтошьств",
                                            var_lemmas={
                                                Source(
                                                    "H"
                                                ): "шьств\ue205\ue201 пѫт\ue205",
                                                Source(
                                                    "G"
                                                ): "шьст\ue205\ue201 пѫт\ue205",
                                            },
                                            main_word="поутошьствꙗ",
                                            var_words={
                                                Source("G"): (
                                                    "шьст\ue205ꙗ пꙋт\ue205 G",
                                                    1,
                                                ),
                                                Source("H"): (
                                                    "шьств\ue205ꙗ пꙋт\ue205 H",
                                                    1,
                                                ),
                                            },
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
