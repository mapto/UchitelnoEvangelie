from semantics import MainLangSemantics, VarLangSemantics
from semantics import _is_variant_lemma


def test_post_init():
    sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    assert len(sem.lemmas) == len(sem.var.lemmas) == 4
    sem = MainLangSemantics("sl", 4, [6, 7], VarLangSemantics("sl", 0, [1, 2, 8, 9]))
    assert len(sem.lemmas) == len(sem.var.lemmas) == 4


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
    assert result == ("", {"G": "\ue205 pron."})

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
    assert result == ("", {})
    result == gr_sem.var.alternatives(row, "C")
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
        + [""] * 11
        + ["bold|italic"]
    )
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == ("", {"G": "\ue205но\ue20dѧдъ", "H": "\ue201д\ue205нородъ"})
    result = sl_sem.var.alternatives(row, "G")
    assert result == ("\ue201д\ue205но\ue20dѧдъ", {"H": "\ue201д\ue205нородъ"})
    result = sl_sem.var.alternatives(row, "H")
    assert result == ("\ue201д\ue205но\ue20dѧдъ", {"G": "\ue205но\ue20dѧдъ"})

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
    result = sl_sem.var.alternatives(row, "WH")
    assert result == ("\ue205но\ue20dѧдъ", {})
    r1 = sl_sem.alternatives(row, "*IGNORED*")
    assert r1 == ("", {"WH": "\ue201д\ue205но\ue20dѧдъ"})


def test_VarLangSemantics_multiword():
    sem = VarLangSemantics("sl", 0, [1])
    result = sem.multiword(["ноедаго G  днородоу H", "днородъ H / ноѧдъ G"])
    assert len(result) == 2
    assert result["G"] == "\ue205но\ue20dедаго"
    assert result["H"] == "\ue201д\ue205нородоу"

    result = sem.multiword(["ноедаго G", "днородъ H / ноѧдъ G"])
    assert result == {"G": "\ue205но\ue20dедаго"}

    result = sem.multiword(["", ""])
    assert result == {"WGH": ""}

    result = sem.multiword(["дноеды WH Ø G", "дноѧдъ"])
    assert result == {"WH": "дноеды", "G": "Ø"}

    result = sem.multiword(["дноеды", "дноѧдъ"])
    assert result == {"WGH": "дноеды"}

    gr_sem = VarLangSemantics("gr", 0, [1])
    result = gr_sem.multiword(["με C", "ἐγώ"])
    assert result == {"C": "με"}


def test_LangSemantics_multilemma():
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
    result = sl_sem.var.multilemma(row)
    assert result == {"G": "\ue205 pron."}

    row = (
        ["вь WGH", "въ", "въ + Loc.", "1/7d1", "оу", "оу насъ", "ѹ"]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["παρ’ C", "παρά ", "παρά + Acc."]
        + [""] * 6
    )
    result = sl_sem.var.multilemma(row)
    assert result == {"WGH": "въ"}
    result = gr_sem.var.multilemma(row)
    assert result == {"C": "παρά"}

    row = (
        ([""] * 3)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με C", "ἐγώ"]
        + ([""] * 7)
    )
    result = sl_sem.multilemma(row)
    assert result == {"": "аꙁъ"}
    result = gr_sem.var.multilemma(row)
    assert result == {"C": "ἐγώ"}

    dummy_sem = MainLangSemantics("sl", 2, [3], VarLangSemantics("sl", 0, [1]))

    result = dummy_sem.var.multilemma(
        ["ноедаго G  днородоу H", "днородъ H & ноѧдъ G", "", ""]
    )
    assert len(result) == 2
    assert result["H"] == "\ue201д\ue205нородъ"
    assert result["G"] == "\ue205но\ue20dѧдъ"

    result = dummy_sem.var.multilemma(["", "", "", ""])
    assert len(result) == 0

    result = dummy_sem.var.multilemma(
        [
            "дноеды WH Ø G",
            "дноѧдъ",
            "\ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ",
        ]
    )
    assert result == {"WH": "дноѧдъ"}

    dummy_sem2 = VarLangSemantics("gr", 0, [1])
    result = dummy_sem2.multilemma(["με C", "ἐγώ"])
    assert result == {"C": "ἐγώ"}

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
    result = sl_sem.var.multilemma(row)
    assert result == {"WH": "\ue201д\ue205но\ue20dѧдъ"}

    row = (
        [
            "\ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ",
        ]
        + [""] * 2
        + [
            "1/W168a34",
            "\ue201д\ue205но\ue20dедоу",
            "бѣ \ue205мѣт\ue205 \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ ",
        ]
        + [""] * 3
        + ["μονογενῆ", "μονογενής"]
        + [""] * 14
    )
    result = sl_sem.multilemma(row)
    assert result == {"": "\ue201д\ue205но\ue20dѧдъ"}
    result = sl_sem.var.multilemma(row)
    assert result == {"H": "\ue201д\ue205нородъ"}


def test__is_variant_lemma():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    row = (
        [""] * 4
        + [
            "1/W168c17",
            "прѣ\ue205сто\ue20dе",
            "всѣмь прѣ\ue205сто\ue20dе\ue201• \ue205 по \ue205сто\ue20dен\ue205\ue205",
            "прѣ\ue205сто\ue20d\ue205т\ue205",
        ]
        + [""] * 3
        + ["ὑπερκλύζων", "ὑπερκλύζω"]
        + [""] * 3
        + ["ὑπερβλύζων C", "ὑπερβλύω"]
        + [""] * 9
    )
    exception = False
    try:
        _is_variant_lemma(row, gr_sem, "C", "ὑπερκλύζω")
    except AssertionError:
        exception = True
    assert exception

    assert _is_variant_lemma(row, gr_sem, "", "ὑπερκλύζω")
    assert _is_variant_lemma(row, gr_sem.var, "C", "ὑπερβλύω")

    assert not _is_variant_lemma(row, gr_sem.var, "D", "ὑπερβλύω")

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
    assert _is_variant_lemma(row, sl_sem.var, "WH", "\ue201д\ue205но\ue20dѧдъ")
    assert not _is_variant_lemma(row, sl_sem.var, "G", "\ue201д\ue205но\ue20dѧдъ")
    assert not _is_variant_lemma(row, sl_sem.var, "G", "\ue205но\ue20dѧдъ")
    assert _is_variant_lemma(row, sl_sem, "", "\ue205но\ue20dѧдъ")
    assert _is_variant_lemma(row, gr_sem, "", "μονογενής")
    assert not _is_variant_lemma(row, gr_sem.var, "", "μονογενής")


def test_build_paths():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

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
        + ["παρ’ C", "παρά", "παρά + Acc."]
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
