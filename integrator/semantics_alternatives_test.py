from model import Alternative, Source
from semantics import MainLangSemantics, VarLangSemantics


def test_LangSemantics_alternatives():
    # old semantics
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )

    row = (
        ["ю G", "\ue205 pron.", "", "1/W168b6", "om.", "", "om."]
        + [""] * 3
        + ["ταύτην", "οὗτος"]
        + [""] * 12
    )
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == Alternative(
        var_lemmas={Source("G"): "\ue205 pron."},
        var_words={Source("G"): "ю G"},
    )

    row = (
        ([""] * 3)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με C", "ἐγώ"]
        + ([""] * 7)
    )
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == Alternative()
    result == gr_sem.var.alternatives(row, Source("C"))
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
    )
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == Alternative(
        var_lemmas={
            Source("H"): "\ue201д\ue205нородъ",
            Source("G"): "\ue205но\ue20dѧдъ",
        },
        var_words={
            Source("G"): "\ue205но\ue20dедаго G",
            Source("H"): "\ue201д\ue205нородоу H",
        },
    )
    result = sl_sem.var.alternatives(row, Source("G"))
    assert result == Alternative(
        main_lemma="\ue201д\ue205но\ue20dѧдъ",
        var_lemmas={Source("H"): "\ue201д\ue205нородъ"},
        main_word="\ue201д\ue205но\ue20dедоу",
        var_words={Source("H"): "\ue201д\ue205нородоу H"},
    )
    result = sl_sem.var.alternatives(row, Source("H"))
    assert result == Alternative(
        main_lemma="\ue201д\ue205но\ue20dѧдъ",
        var_lemmas={Source("G"): "\ue205но\ue20dѧдъ"},
        main_word="\ue201д\ue205но\ue20dедоу",
        var_words={Source("G"): "\ue205но\ue20dедаго G"},
    )

    # semantics update from September 2021
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )

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
    )
    result = sl_sem.var.alternatives(row, Source("WH"))
    assert result == Alternative(
        "\ue205но\ue20dѧдъ", main_word="\ue205но\ue20dадꙑ\ue205"
    )
    r1 = sl_sem.alternatives(row, "*IGNORED*")
    assert r1 == Alternative(
        var_lemmas={Source("WH"): "\ue201д\ue205но\ue20dѧдъ"},
        var_words={Source("WH"): "\ue201д\ue205но\ue20dеды WH"},
    )


def test_bozhii():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )

    row = (
        ["б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H", "бож\ue205\ue205"]
        + [""] * 2
        + ["1/7a4", "боꙁѣ", "о боꙁѣ словес\ue205•", "богъ", "Dat."]
        + [""] * 2
        + ["Θεοῦ", "θεός", "Gen."]
        + [""] * 13
    )
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == Alternative(
        var_lemmas={Source("WGH"): "бож\ue205\ue205"},
        var_words={
            Source("WGH"): "б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G"
        },
    )

    result = sl_sem.var.alternatives(row, Source("G"))
    assert result == Alternative("богъ", {}, "боꙁѣ")

    result = sl_sem.var.alternatives(row, Source("GHW"))
    assert result == Alternative("богъ", {}, "боꙁѣ")


def test_MainLangSemantics_ot():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    row = (
        ["ѿ WG  ѡ H", "отъ"]
        + [""] * 2
        + ["1/5d11"]
        + ["om.", ""] * 2
        + [""] * 2
        + ["ἐπὶ", "ἐπί", "ἐπί + Gen."]
        + [""] * 13
    )

    result = sl_sem.alternatives(row, Source())
    assert result == Alternative(
        var_lemmas={Source("WGH"): "отъ"}, var_words={Source("WGH"): "ѡ H ѿ WG"}
    )
