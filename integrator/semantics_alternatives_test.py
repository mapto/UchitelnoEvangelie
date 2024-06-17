from config import FROM_LANG, TO_LANG
from const import STYLE_COL
from model import Alternative, Source
from semantics import MainLangSemantics, VarLangSemantics


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


def test_base_1():
    row = (
        ["ю G", "\ue205 pron.", "", "", "1/W168b6", "om.", "", "om."]
        + [""] * 3
        + ["ταύτην", "οὗτος"]
        + [""] * 13
        + ["1"] * 4
    )
    result = sl_sem.alternatives(row)
    assert result == (
        Alternative(),
        {Source("G"): Alternative("ю G", ["\ue205 pron."])},
    )


def test_base_2():
    # style_col = 24
    # # old semantics
    # sl_sem = MainLangSemantics(
    #     FROM_LANG,
    #     4,
    #     [6, 7, 8, 9],
    #     VarLangSemantics(FROM_LANG, 0, [1, 2], cnt_col=style_col + 2),
    #     cnt_col=style_col + 1,
    # )
    # gr_sem = MainLangSemantics(
    #     TO_LANG,
    #     10,
    #     [11, 12, 13],
    #     VarLangSemantics(TO_LANG, 15, [16, 17], cnt_col=style_col + 4),
    #     cnt_col=style_col + 3,
    # )

    row = (
        ([""] * 4)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με Cs", "ἐγώ"]
        + ([""] * 9)
        + ["1"] * 4
    )
    # print(len(row), STYLE_COL, STYLE_COL+4,row[STYLE_COL:STYLE_COL+4])
    result = sl_sem.alternatives(row)
    assert result == (Alternative(), {})
    result == gr_sem.var.alternatives(row, Source("Cs"))
    # assert result == ("μὲν", {})


def test_base_3():
    style_col = 24
    # old semantics
    sl_sem = MainLangSemantics(
        FROM_LANG,
        4,
        [6, 7, 8, 9],
        VarLangSemantics(FROM_LANG, 0, [1, 2], cnt_col=style_col + 2),
        cnt_col=style_col + 1,
    )
    gr_sem = MainLangSemantics(
        TO_LANG,
        10,
        [11, 12, 13],
        VarLangSemantics(TO_LANG, 15, [16, 17], cnt_col=style_col + 4),
        cnt_col=style_col + 3,
    )

    row = (
        [
            "\ue205но\ue20dедаго G  \ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ H / \ue205но\ue20dѧдъ G",
            "",
            "1/W168a25",
            "\ue201д\ue205но\ue20dедоу",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 12
        + ["bold|italic"]
        + ["1"] * 4
    )
    result = sl_sem.alternatives(row)
    assert result == (
        Alternative(),
        {
            Source("H"): Alternative("\ue201д\ue205нородоу H", ["\ue201д\ue205нородъ"]),
            Source("G"): Alternative("\ue205но\ue20dедаго G", ["\ue205но\ue20dѧдъ"]),
        },
    )

    result = sl_sem.var.alternatives(row, Source("G"))
    assert result == (
        Alternative("\ue201д\ue205но\ue20dедоу", ["\ue201д\ue205но\ue20dѧдъ"]),
        {Source("H"): Alternative("\ue201д\ue205нородоу H", ["\ue201д\ue205нородъ"])},
    )

    result = sl_sem.var.alternatives(row, Source("H"))
    assert result == (
        Alternative("\ue201д\ue205но\ue20dедоу", ["\ue201д\ue205но\ue20dѧдъ"]),
        {Source("G"): Alternative("\ue205но\ue20dедаго G", ["\ue205но\ue20dѧдъ"])},
    )


def test_std_sem():
    row = (
        ["\ue201д\ue205но\ue20dеды WH Ø G", "\ue201д\ue205но\ue20dѧдъ"]
        + [""] * 2
        + [
            "1/5a4",
            "\ue205но\ue20dадꙑ\ue205",
            "нъ ꙗко б\ue010ъ• а \ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενὴς", "μονογενής"]
        + [""] * 14
        + ["1"] * 2
    )
    result = sl_sem.var.alternatives(row, Source("WH"))
    assert result == (Alternative("\ue205но\ue20dадꙑ\ue205", ["\ue205но\ue20dѧдъ"]), {})
    r1 = sl_sem.alternatives(row)
    assert r1 == (
        Alternative(),
        {
            Source("WH"): Alternative(
                "\ue201д\ue205но\ue20dеды WH", ["\ue201д\ue205но\ue20dѧдъ"]
            ),
        },
    )


def test_bozhii():
    row = (
        ["б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H", "бож\ue205\ue205"]
        + [""] * 2
        + ["1/7a4", "боꙁѣ", "о боꙁѣ словес\ue205•", "богъ", "Dat."]
        + [""] * 2
        + ["Θεοῦ", "θεός", "Gen."]
        + [""] * 13
        + ["1"] * 2
    )
    result = sl_sem.alternatives(row)
    assert result == (
        Alternative(),
        {
            Source("WGH"): Alternative(
                word="б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H",
                lemmas=["бож\ue205\ue205"],
            ),
        },
    )

    result = sl_sem.var.alternatives(row, Source("G"))
    assert result == (Alternative("боꙁѣ", ["богъ", "Dat."]), {})

    result = sl_sem.var.alternatives(row, Source("GHW"))
    assert result == (Alternative("боꙁѣ", ["богъ", "Dat."]), {})


def test_ot():
    row = (
        ["ѿ WG  ѡ H", "отъ"]
        + [""] * 2
        + ["1/5d11"]
        + ["om.", ""] * 2
        + [""] * 2
        + ["ἐπὶ", "ἐπί", "ἐπί + Gen."]
        + [""] * 13
        + ["1"] * 2
    )

    result = sl_sem.alternatives(row, Source())
    assert result == (
        Alternative(),
        {
            Source("WGH"): Alternative("ѡ H ѿ WG", ["отъ"]),
        },
    )


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

    result = sl_sem.var.alternatives(row, Source("G"))
    assert result == (
        Alternative("поутошьств\ue205ꙗ", ["пѫтошьств\ue205\ue201"]),
        {
            Source("H"): Alternative(
                "шьств\ue205ꙗ пꙋт\ue205 H", ["пѫть", "шьств\ue205\ue201 пѫт\ue205"]
            ),
        },
    )

    result = sl_sem.var.alternatives(row, Source("H"))
    assert result == (
        Alternative("поутошьств\ue205ꙗ", ["пѫтошьств\ue205\ue201"]),
        {
            Source("G"): Alternative(
                "шьст\ue205ꙗ пꙋт\ue205 G", ["пѫть", "шьст\ue205\ue201 пѫт\ue205"]
            ),
        },
    )


def test_main_var_alternatives_trans_gram():
    row = (
        [
            "сть GH",
            "бꙑт",
            "",
            "gramm.",
            "06/50a06",
        ]
        + ["om."] * 3
        + [""] * 3
        + ["Ø"] * 2
        + [""] * 13
        + ["hl03"]
        + ["1"] * 4
    )

    result = sl_sem.alternatives(row)
    assert result == (
        Alternative(),
        {
            Source("GH"): Alternative("\ue201сть GH", ["бꙑт", "gramm."]),
        },
    )


def test_main_sumeromadrost():
    rows = [
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
            "съмѣрѹмѫдрость WG / съмѣр\ue201нъ мѫдрость H",
            "съмѣр\ue201наꙗ мѫдрость H",
            "",
            "25/125a03",
            "съмѣромоудрост\ue205",
            "съмѣромоудро-",
            "съмѣромѫдрость",
        ]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
        + ["hl00:FFFCD5B4"]
        + ["1"] * 4,
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
            "съмѣрѹмѫдрость WG / съмѣр\ue201нъ мѫдрость H",
            "съмѣр\ue201наꙗ мѫдрость H",
            "",
            "25/125a03",
            "съмѣромоудрост\ue205",
        ]
        + [""] * 5
        + ["om."]
        + [""] * 4
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
        + ["hl00:FFFCD5B4"]
        + ["1"] * 4,
    ]

    result = sl_sem.alternatives(rows[0])
    assert result == (
        Alternative(),
        {
            Source("WG"): Alternative("смѣроумоудрост\ue205 WG", ["съмѣрѹмѫдрость"]),
            Source("H"): Alternative(
                "смѣрены\ue201 моудрост\ue205 H",
                ["съмѣр\ue201нъ мѫдрость", "съмѣр\ue201наꙗ мѫдрость"],
            ),
        },
    )


def test_nechuvstven():
    row = (
        [
            "не\ue20dю\ue205но W  не\ue20dю\ue205нь G  не\ue20dювьствьнь H",
            "не\ue20dѹ\ue205нъ WG / не\ue20dѹвьствьнъ H",
        ]
        + [""] * 2
        + ["04/17d20", "не\ue20dювьнъ", "кою ꙗко не\ue20dю-", "не\ue20dѹвьнъ"]
        + [""] * 3
        + ["ἀναίσθητος", "ἀναίσθητος"]
        + [""] * 14
        + [1] * 4
    )
    result = sl_sem.var.alternatives(row, Source("H"))
    assert result == (
        Alternative("не\ue20dювьнъ", ["не\ue20dѹвьнъ"]),
        {
            Source("WG"): Alternative(
                "не\ue20dю\ue205но W не\ue20dю\ue205нь G", ["не\ue20dѹ\ue205нъ"]
            )
        },
    )
