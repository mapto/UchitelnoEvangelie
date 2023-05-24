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


def test_base():
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
        ["ю G", "\ue205 pron.", "", "1/W168b6", "om.", "", "om."]
        + [""] * 3
        + ["ταύτην", "οὗτος"]
        + [""] * 14
        + ["1"] * 4
    )
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == Alternative(
        var_lemmas={Source("G"): "\ue205 pron."},
        var_words={Source("G"): ("ю G", 1)},
    )

    row = (
        ([""] * 3)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με Cs", "ἐγώ"]
        + ([""] * 7)
        + ["1"] * 4
    )
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == Alternative()
    result == gr_sem.var.alternatives(row, Source("Cs"))
    # assert result == ("μὲν", {})

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
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == Alternative(
        var_lemmas={
            Source("H"): "\ue201д\ue205нородъ",
            Source("G"): "\ue205но\ue20dѧдъ",
        },
        var_words={
            Source("G"): ("\ue205но\ue20dедаго G", 1),
            Source("H"): ("\ue201д\ue205нородоу H", 1),
        },
    )
    result = sl_sem.var.alternatives(row, Source("G"))
    assert result == Alternative(
        main_lemma="\ue201д\ue205но\ue20dѧдъ",
        var_lemmas={Source("H"): "\ue201д\ue205нородъ"},
        main_word="\ue201д\ue205но\ue20dедоу",
        var_words={Source("H"): ("\ue201д\ue205нородоу H", 1)},
    )
    result = sl_sem.var.alternatives(row, Source("H"))
    assert result == Alternative(
        main_lemma="\ue201д\ue205но\ue20dѧдъ",
        var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
        main_word="\ue201д\ue205но\ue20dедоу",
        var_words={Source("G"): ("\ue205но\ue20dедаго G", 1)},
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
    assert result == Alternative(
        "\ue205но\ue20dѧдъ", main_word="\ue205но\ue20dадꙑ\ue205"
    )
    r1 = sl_sem.alternatives(row, "*IGNORED*")
    assert r1 == Alternative(
        var_lemmas={Source("WH"): "\ue201д\ue205но\ue20dѧдъ"},
        var_words={Source("WH"): ("\ue201д\ue205но\ue20dеды WH", 1)},
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
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == Alternative(
        var_lemmas={Source("WGH"): "бож\ue205\ue205"},
        var_words={
            Source("WGH"): (
                "б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G",
                1,
            )
        },
    )

    result = sl_sem.var.alternatives(row, Source("G"))
    assert result == Alternative("богъ", {}, "боꙁѣ")

    result = sl_sem.var.alternatives(row, Source("GHW"))
    assert result == Alternative("богъ", {}, "боꙁѣ")


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
    assert result == Alternative(
        var_lemmas={Source("WGH"): "отъ"}, var_words={Source("WGH"): ("ѡ H ѿ WG", 1)}
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

    result = sl_sem.var.alternatives(row, Source("GH"))
    assert result == Alternative(
        main_lemma="пѫтошьств\ue205\ue201",
        var_lemmas={
            Source("H"): "шьств\ue205\ue201 пѫт\ue205",
            Source("G"): "шьст\ue205\ue201 пѫт\ue205",
        },
        main_word="поутошьств\ue205ꙗ",
        var_words={
            Source("G"): ("шьст\ue205ꙗ пꙋт\ue205 G", 1),
            Source("H"): ("шьств\ue205ꙗ пꙋт\ue205 H", 1),
        },
        main_cnt=1,
    )


def test_var_main_level_alternatives_put():
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

    m = len(sl_sem.var.lemmas) - 1
    for l in range(m, 0, -1):  # does not reach 0
        alt = sl_sem.var.level_main_alternatives(row, Source("GH"), l)
        assert not alt[0] and not alt[1]

    result = sl_sem.var.level_main_alternatives(row, Source("GH"))
    assert result == ("пѫтошьств\ue205\ue201", "поутошьств\ue205ꙗ", 1)


def test_var_var_level_alternatives_put():
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

    m = len(sl_sem.var.lemmas) - 1
    for l in range(m, 1, -1):  # does not reach 1
        alt = sl_sem.var.level_var_alternatives(row, Source("GH"), l)
        assert not alt[0] and not alt[1]

    result = sl_sem.var.level_var_alternatives(row, Source("GH"), 1)
    assert result == (
        {
            Source("H"): "шьств\ue205\ue201 пѫт\ue205",
            Source("G"): "шьст\ue205\ue201 пѫт\ue205",
        },
        {
            Source("H"): ("шьств\ue205ꙗ пꙋт\ue205 H", 1),
            Source("G"): ("шьст\ue205ꙗ пꙋт\ue205 G", 1),
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

    result = sl_sem.alternatives(row, Source())
    assert result == Alternative(
        var_lemmas={Source("HG"): "бꙑт"}, var_words={Source("HG"): ("\ue201сть GH", 1)}
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
    assert result == Alternative(
        var_lemmas={
            Source("H"): "съмѣр\ue201наꙗ мѫдрость",
            Source("WG"): "съмѣрѹмѫдрость",
        },
        var_words={
            Source("H"): ("смѣрены\ue201 моудрост\ue205 H", 1),
            Source("WG"): ("смѣроумоудрост\ue205 WG", 1),
        },
    )


def test_main_level_alternatives_sumeromadrost():
    row = (
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
        + ["1"] * 4
        + [""]
    )

    alt = sl_sem.level_var_alternatives(row, Source(), 1)
    assert alt == (
        {Source("H"): "съмѣр\ue201наꙗ мѫдрость"},
        {Source("H"): ("смѣрены\ue201 моудрост\ue205 H", 1)},
    )
    alt = sl_sem.level_var_alternatives(row, Source(), 0)
    assert alt == (
        {Source("H"): "съмѣр\ue201нъ мѫдрость", Source("WG"): "съмѣрѹмѫдрость"},
        {
            Source("H"): ("смѣрены\ue201 моудрост\ue205 H", 1),
            Source("WG"): ("смѣроумоудрост\ue205 WG", 1),
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
    assert result == Alternative(
        main_lemma="не\ue20dѹвьнъ",
        var_lemmas={Source("WG"): "не\ue20dѹ\ue205нъ"},
        main_word="не\ue20dювьнъ",
        var_words={
            Source("WG"): (
                "не\ue20dю\ue205но W не\ue20dю\ue205нь G",
                1,
            )
        },
    )
