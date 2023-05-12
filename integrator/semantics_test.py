from sortedcontainers.sorteddict import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL
from model import Alternative, Index, Path, Source, Alignment, Usage
from semantics import MainLangSemantics, VarLangSemantics
from semantics import _add_usage, _build_content
from setup import sl_sem, gr_sem


def test_post_init():
    sem = MainLangSemantics(
        FROM_LANG, 4, [6, 7, 8, 9], VarLangSemantics(FROM_LANG, 0, [1, 2])
    )
    assert len(sem.lemmas) == len(sem.var.lemmas) == 4
    sem = MainLangSemantics(
        FROM_LANG, 4, [6, 7], VarLangSemantics(FROM_LANG, 0, [1, 2, 8, 9])
    )
    assert len(sem.lemmas) == len(sem.var.lemmas) == 4


def test_build_paths():
    res = sl_sem.build_paths([""] * 7 + ["боудеть", "бꙑт\ue205 ", "", "gram."])
    res = [str(r) for r in res]
    assert res == ["бꙑт\ue205 → боудеть gram."]

    res = sl_sem.build_paths([""] * 7 + ["едно", "две", "три", "четири"])
    res = [str(r) for r in res]
    assert res == ["четири → три → две → едно"]

    res = sl_sem.build_paths([""] * 7 + ["едно", "две", "три", "gram."])
    res = [str(r) for r in res]
    assert res == ["три → две → едно gram."]

    res = sl_sem.build_paths(
        [""] * 4
        + ["1/4b17"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["ὁ", "ὁ"]
        + [""] * 13
        + ["bold|italic"]
    )
    res = [str(r) for r in res]
    assert res == ["ₓ"]

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
    )
    res = sl_sem.var.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["\ue201д\ue205нородъ", "\ue205но\ue20dѧдъ"]

    row = (
        [""] * 4
        + ["1/8a13"]
        + ["Instr.", ""] * 2
        + [""] * 2
        + ["παρὰ", "παρά", "παρά + Acc."]
        + [""] * 13
    )
    res = sl_sem.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["Instr."]

    res = gr_sem.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["παρά + Acc. → παρά"]

    assert not gr_sem.var.build_paths(row)[0]
    assert not sl_sem.var.build_paths(row)[0]

    row = (
        ["вь WGH", "въ", "въ + Loc.", "", "1/7d1", "оу", "оу насъ", "ѹ"]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["παρ’ Cs", "παρά", "παρά + Acc."]
        + [""] * 8
    )
    res = sl_sem.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["ѹ"]

    res = sl_sem.var.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["въ + Loc. → въ"]

    res = gr_sem.build_paths(row)
    res = [str(r) for r in res]
    assert res == [""]

    res = gr_sem.var.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["παρά + Acc. → παρά"]


def test_build_paths_special():
    row = (
        ["свѣть WH"]
        + [""] * 3
        + ["1/6c8", "всѣмъ", "всѣмъ \ue20dл\ue010вкомъ•", "вьсь", "≈ вьсѣмъ"]
        + [""] * 2
        + ["καθόλου", "καθόλου"]
        + [""] * 14
    )
    res = sl_sem.build_paths(row)
    assert [str(p) for p in res] == ["≈ вьсѣмъ → вьсь"]
    assert res == [Path(parts=["вьсь", "≈ вьсѣмъ"])]

    row = (
        [""] * 4
        + [
            "1/4b16",
            "на\ue20dатъ",
            "семоу на\ue20dатъ",
            "на\ue20dѧт\ue205",
            "≠ на\ue20dѧт\ue205",
        ]
        + [""] * 2
        + ["ᾐνίξατο", "αἰνίσσομαι"]
        + [""] * 14
    )
    res = sl_sem.build_paths(row)
    assert [str(p) for p in res] == ["≠ на\ue20dѧт\ue205"]
    assert res == [Path(parts=["на\ue20dѧт\ue205", "≠ на\ue20dѧт\ue205"])]


def test_build_paths_puteshestive():
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

    rows = [
        [
            "шьст\ue205ꙗ G шьств\ue205ꙗ H пꙋт\ue205 GH",
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
            "шьст\ue205ꙗ G шьств\ue205ꙗ H пꙋт\ue205 GH",
            "пѫть",
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

    res = sl_sem.var.build_paths(rows[0])
    assert res == [
        Path(parts=["шьств\ue205\ue201", "шьств\ue205\ue201 пѫт\ue205"]),
        Path(parts=["шьст\ue205\ue201", "шьст\ue205\ue201 пѫт\ue205"]),
    ]


def test_add_usage():
    usages = [
        Alignment(
            Index("1/W168a25"),
            Usage("gr", word="μονογενοῦς"),
            Usage(
                "sl",
                Source("G"),
                alt=Alternative(
                    main_lemma="\ue201д\ue205но\ue20dѧдъ",
                    var_lemmas={"H": "\ue201д\ue205нородъ"},
                ),
            ),
        ),
        Alignment(
            Index("1/5a4"),
            Usage("gr", word="μονογενὴς"),
            Usage(
                "sl",
                alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
            ),
        ),
        Alignment(
            Index("1/4c15"),
            Usage("gr", word="μονογενοῦς"),
            Usage(
                "sl",
                alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
            ),
        ),
        Alignment(
            Index("1/W168a25"),
            Usage("gr", word="μονογενοῦς"),
            Usage(
                "sl",
                Source("H"),
                alt=Alternative(
                    main_lemma="\ue201д\ue205но\ue20dѧдъ",
                    var_lemmas={"G": "\ue205но\ue20dѧдъ"},
                ),
            ),
        ),
        Alignment(
            Index("1/W168a28"),
            Usage("gr", word="μονογενοῦς"),
        ),
        Alignment(
            Index("1/W168a25"),
            Usage("gr", word="μονογενοῦς"),
            Usage(
                "sl",
                alt=Alternative(
                    var_lemmas={
                        "H": "\ue201д\ue205нородъ",
                        "G": "\ue205но\ue20dѧдъ",
                    }
                ),
            ),
        ),
        Alignment(
            Index("1/5a4"),
            Usage("gr", word="μονογενὴς"),
            Usage(
                "sl",
                Source("WH"),
                alt=Alternative(main_lemma="\ue205но\ue20dѧдъ "),
            ),
        ),
        Alignment(
            Index("1/4c15"),
            Usage("gr", word="μονογενοῦς"),
            Usage(
                "sl",
                Source("WH"),
                alt=Alternative(main_lemma="\ue205но\ue20dѧдъ"),
            ),
        ),
    ]

    d = SortedDict()
    for u in usages:
        _add_usage(u, "", ("", ""), d)
    assert d == SortedDict(
        {
            "": {
                ("", ""): SortedSet(
                    [
                        Alignment(
                            Index("1/4c15"),
                            Usage("gr", word="μονογενοῦς"),
                            Usage(
                                "sl",
                                alt=Alternative(
                                    var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}
                                ),
                            ),
                        ),
                        Alignment(
                            Index("1/4c15"),
                            Usage("gr", word="μονογενοῦς"),
                            Usage(
                                "sl",
                                Source("WH"),
                                alt=Alternative(main_lemma="\ue205но\ue20dѧдъ"),
                            ),
                        ),
                        Alignment(
                            Index("1/5a4"),
                            Usage("gr", word="μονογενὴς"),
                            Usage(
                                "sl",
                                alt=Alternative(
                                    var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}
                                ),
                            ),
                        ),
                        Alignment(
                            Index("1/5a4"),
                            Usage("gr", word="μονογενὴς"),
                            Usage(
                                "sl",
                                Source("WH"),
                                alt=Alternative(main_lemma="\ue205но\ue20dѧдъ "),
                            ),
                        ),
                        Alignment(
                            Index("1/W168a25"),
                            Usage("gr", word="μονογενοῦς"),
                            Usage(
                                "sl",
                                alt=Alternative(
                                    var_lemmas={
                                        "H": "\ue201д\ue205нородъ",
                                        "G": "\ue205но\ue20dѧдъ",
                                    }
                                ),
                            ),
                        ),
                        Alignment(
                            Index("1/W168a28"),
                            Usage("gr", word="μονογενοῦς"),
                        ),
                        Alignment(
                            Index("1/W168a25"),
                            Usage("gr", word="μονογενοῦς"),
                            Usage(
                                "sl",
                                Source("G"),
                                alt=Alternative(
                                    "\ue201д\ue205но\ue20dѧдъ",
                                    var_lemmas={"H": "\ue201д\ue205нородъ"},
                                ),
                            ),
                        ),
                        Alignment(
                            Index("1/W168a25"),
                            Usage("gr", word="μονογενοῦς"),
                            Usage(
                                "sl",
                                Source("H"),
                                alt=Alternative(
                                    "\ue201д\ue205но\ue20dѧдъ",
                                    var_lemmas={"G": "\ue205но\ue20dѧдъ"},
                                ),
                            ),
                        ),
                    ]
                )
            }
        }
    )


def test_add_usage_puteshestvie():
    usages = [
        Alignment(
            Index("5/28d18"),
            Usage(
                "sl",
                Source("G"),
                alt=Alternative(
                    var_lemmas={Source("H"): "шьств\ue205\ue201 пѫт\ue205"},
                    main_word="поутошьств\ue205ꙗ",
                    var_words={Source("H"): ("пꙋт\ue205 GH шьств\ue205ꙗ H", 1)},
                ),
                word="пꙋт\ue205 GH шьст\ue205ꙗ G",
            ),
        ),
        Alignment(
            Index("5/28d18"),
            Usage(
                "sl",
                Source("H"),
                alt=Alternative(
                    var_lemmas={Source("G"): "шьст\ue205\ue201 пѫт\ue205"},
                    main_word="поутошьств\ue205ꙗ",
                    var_words={Source("G"): ("пꙋт\ue205 GH шьст\ue205ꙗ G", 1)},
                ),
                word="пꙋт\ue205 GH шьств\ue205ꙗ H",
            ),
        ),
    ]
    d = SortedDict()
    for u in usages:
        _add_usage(u, "ὁδοιπορία", ("пꙋт\ue205 GH шьст\ue205ꙗ G", "ὁδοιπορίας"), d)
    assert d == {
        "ὁδοιπορία": {
            ("пꙋт\ue205 GH шьст\ue205ꙗ G", "ὁδοιπορίας"): SortedSet(
                [
                    Alignment(
                        Index("5/28d18"),
                        Usage(
                            "sl",
                            Source("G"),
                            Alternative(
                                var_lemmas={Source("H"): "шьств\ue205\ue201 пѫт\ue205"},
                                main_word="поутошьств\ue205ꙗ",
                                var_words={
                                    Source("H"): ("пꙋт\ue205 GH шьств\ue205ꙗ H", 1)
                                },
                            ),
                            word="пꙋт\ue205 GH шьст\ue205ꙗ G",
                        ),
                    ),
                    Alignment(
                        Index("5/28d18"),
                        Usage(
                            "sl",
                            Source("H"),
                            Alternative(
                                var_lemmas={Source("G"): "шьст\ue205\ue201 пѫт\ue205"},
                                main_word="поутошьств\ue205ꙗ",
                                var_words={
                                    Source("G"): ("пꙋт\ue205 GH шьст\ue205ꙗ G", 1)
                                },
                            ),
                            word="пꙋт\ue205 GH шьств\ue205ꙗ H",
                        ),
                    ),
                ]
            )
        }
    }


def test_add_count():
    sem = MainLangSemantics(FROM_LANG, 5, [7], VarLangSemantics(FROM_LANG, 0, [1]))
    counts = {}
    rows = [[""] * 5 + ["om.", ""] * 2, [""] * 4 + ["1/1a1"] + ["om.", ""] * 2]
    for r in rows:
        counts = sem.add_count(r, counts)
    assert not counts
    assert rows == [
        [""] * 5 + ["om.", ""] * 2 + ["1"],
        [""] * 4 + ["1/1a1"] + ["om.", ""] * 2 + ["1"],
    ]

    counts = {}
    rows = [["om."] * 2] * 3
    for r in rows:
        counts = sem.var.add_count(r, counts)
    assert not counts
    assert rows == [["om.", "om.", "1"]] * 3

    counts = {}
    rows = [["om. WH"] * 2] * 3
    for r in rows:
        counts = sem.var.add_count(r, counts)
    assert not counts
    assert rows == [["om. WH", "om. WH", "1"]] * 3


def test_add_count_mulitvariant():
    sem = MainLangSemantics(FROM_LANG, 5, [7], VarLangSemantics(FROM_LANG, 0, [1]))
    counts = {}
    rows = [["om. WH om. G", "om. WH / om. G"]] * 3
    for r in rows:
        counts = sem.var.add_count(r, counts)
    assert not counts
    assert rows == [["om. WH om. G", "om. WH / om. G", "1"]] * 3

    # TODO: Counting with multivariants is messed up
    # rows = [["а WH б G", "а WH / б G"]] * 3
    # for r in rows:
    #     counts = sem.var.add_count(r, counts)
    # assert rows == [
    #     ["а WH б G", "а WH / б G", "1"],
    #     ["а WH б G", "а WH / б G", "2"],
    #     ["а WH б G", "а WH / б G", "3"],
    # ]


def test_build_content():
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
    result = _build_content(row, sl_sem.var, Source("GH"), "\ue201сть GH", 1)
    assert result == Usage(
        lang="sl",
        var=Source("GH"),
        alt=Alternative(main_lemma="om.", main_word="om."),
        word="\ue201сть GH",
        lemmas=["бꙑт\ue205", "", "gramm."],
    )
