from sortedcontainers.sorteddict import SortedDict, SortedSet  # type: ignore

from model import Alternative, Index, Path, Source, Usage
from semantics import MainLangSemantics, VarLangSemantics
from semantics import _is_variant_lemma, _add_usage


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


def test_LangSemantics_alternatives_bozhii():
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


def test_MainLangSemantics_alternatives_ot():
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


def test_VarLangSemantics_multiword():
    sem = VarLangSemantics("sl", 0, [1])
    result = sem.multiword(["ноедаго G  днородоу H", "днородъ H / ноѧдъ G"])
    assert len(result) == 2
    assert result["G"] == "\ue205но\ue20dедаго"
    assert result["H"] == "\ue201д\ue205нородоу"

    result = sem.multiword(["ноедаго G", "днородъ H / ноѧдъ G"])
    assert result == {"G": "\ue205но\ue20dедаго"}

    result = sem.multiword(["", ""])
    assert result == {Source("WGH"): ""}

    result = sem.multiword(["дноеды WH Ø G", "дноѧдъ"])
    assert result == {Source("WH"): "дноеды", "G": "Ø"}

    result = sem.multiword(["дноеды", "дноѧдъ"])
    assert result == {Source("WGH"): "дноеды"}

    gr_sem = VarLangSemantics("gr", 0, [1])
    result = gr_sem.multiword(["με C", "ἐγώ"])
    assert result == {"C": "με"}


def test_VarLangSemantics_multiword_greek_paris():
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    row = (
        [""] * 4
        + ["12/67d19", "\ue20dьтеть•", "\ue20dьтеть• въꙁлѣга-", "\ue20d\ue205ст\ue205"]
        + [""] * 3
        + ["τιμὰς"]
        + [""] * 4
        + ["τιμᾷ MPaPb", "τιμάω"]
        + [""] * 9
    )
    result = gr_sem.var.multiword(row)
    assert result == {"MPaPb": "τιμᾷ"}

    row = (
        [""] * 4
        + [
            "12/67d19",
            "въꙁлѣган\ue205е",
            "\ue20dьтеть• въꙁлѣга-",
            "въꙁлѣган\ue205\ue201",
        ]
        + [""] * 3
        + ["ἀνάκλισιν", "ἀνάκλισις"]
        + [""] * 3
        + ["ἀνάκλησιν CMPcPa"]
        + [""] * 10
    )
    result = gr_sem.var.multiword(row)
    assert result == {Source("CMPcPa"): "ἀνάκλησιν"}


def test_VarLangSemantics_multiword_bozhii():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )

    r = (
        ["б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H", "бож\ue205\ue205"]
        + [""] * 2
        + ["1/7a4", "боꙁѣ", "о боꙁѣ словес\ue205•", "богъ", "Dat."]
        + [""] * 2
        + ["Θεοῦ", "θεός", "Gen."]
        + [""] * 13
    )
    result = sl_sem.var.multiword(r)
    assert result == {
        "G": "б\ue010ж\ue205\ue205",
        "H": "б\ue010жї\ue205",
        "W": "б\ue010ж\ue205",
    }


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
    assert result == {Source("WGH"): "въ"}
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
    assert result == {Source("WH"): "дноѧдъ"}

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
    assert result == {Source("WH"): "\ue201д\ue205но\ue20dѧдъ"}

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


def test_LangSemantics_multilemma_sub():
    # old semantics
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )
    row = (
        ["вь WGH", "въ", "въ + Loc.", "1/7d1", "оу", "оу насъ", "ѹ"]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["παρ’ C", "παρά ", "παρά + Acc."]
        + [""] * 6
    )
    result = gr_sem.var.multilemma(row, 1)
    assert result == {"C": "παρά + Acc."}

    result = sl_sem.var.multilemma(row, 1)
    assert result == {Source("WGH"): "въ + Loc."}

    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    row = (
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "",
            "себе• по поут\ue205 хо-",
            "ход\ue205т\ue205 спѣт\ue205",
            "ход\ue205т\ue205 спѣѭще ≠",
        ]
        + [""] * 2
        + ["προβαίνοντες", "προβαίνω"]
        + [""] * 13
        + ["hl05|hl00"]
    )
    result = sl_sem.var.multilemma(row, 1)
    assert result == {Source("WG"): "ходомь спѣт\ue205"}
    result = sl_sem.var.multilemma(row)
    assert result == {Source("WG"): "ходъ"}


def test_LangSemantics_multilemma_paris():
    """Greek opies held in Paris library are indicated by P?"""
    # old semantics, so that variants are in word, not lemma
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )

    row = (
        [""] * 4
        + ["12/67d19", "\ue20dьтеть•", "\ue20dьтеть• въꙁлѣга-", "\ue20d\ue205ст\ue205"]
        + [""] * 3
        + ["τιμὰς"]
        + [""] * 4
        + ["τιμᾷ MPaPb", "τιμάω"]
        + [""] * 9
    )
    result = gr_sem.var.multilemma(row)
    assert result == {"MPaPb": "τιμᾷ"}

    row = (
        [""] * 4
        + [
            "12/67d19",
            "въꙁлѣган\ue205е",
            "\ue20dьтеть• въꙁлѣга-",
            "въꙁлѣган\ue205\ue201",
        ]
        + [""] * 3
        + ["ἀνάκλισιν", "ἀνάκλισις"]
        + [""] * 3
        + ["ἀνάκλησιν CMPcPa"]
        + [""] * 10
    )
    result = gr_sem.var.multilemma(row)
    assert result == {Source("CMPcPa"): "ἀνάκλησιν"}


def test_LangSemantics_multiword_bozhii():
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
    result = sl_sem.var.multilemma(row)
    assert result == {Source("GHW"): "бож\ue205\ue205"}


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
        _is_variant_lemma(row, gr_sem, Source("C"), "ὑπερκλύζω")
    except AssertionError:
        exception = True
    assert exception

    assert _is_variant_lemma(row, gr_sem, Source(""), "ὑπερκλύζω")
    assert _is_variant_lemma(row, gr_sem.var, Source("C"), "ὑπερβλύω")

    assert not _is_variant_lemma(row, gr_sem.var, Source("D"), "ὑπερβλύω")

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
    assert _is_variant_lemma(row, sl_sem.var, Source("HW"), "\ue201д\ue205но\ue20dѧдъ")
    assert not _is_variant_lemma(
        row, sl_sem.var, Source("G"), "\ue201д\ue205но\ue20dѧдъ"
    )
    assert not _is_variant_lemma(row, sl_sem.var, Source("G"), "\ue205но\ue20dѧдъ")
    assert _is_variant_lemma(row, sl_sem, Source(""), "\ue205но\ue20dѧдъ")
    assert _is_variant_lemma(row, gr_sem, Source(""), "μονογενής")
    assert not _is_variant_lemma(row, gr_sem.var, Source(""), "μονογενής")


def test_is_variant_lemma_bozhii():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )
    row = (
        ["б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H", "бож\ue205\ue205"]
        + [""] * 2
        + ["1/7a4", "боꙁѣ", "о боꙁѣ словес\ue205•", "богъ", "Dat."]
        + [""] * 2
        + ["Θεοῦ", "θεός", "Gen."]
        + [""] * 13
    )
    assert _is_variant_lemma(row, sl_sem.var, Source("W"), "бож\ue205\ue205")


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


def test_build_paths_special():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

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
        + ["1/4b16", "на\ue20dатъ", "семоу на\ue20dатъ", "на\ue20dѧт\ue205", "≠"]
        + [""] * 2
        + ["ᾐνίξατο", "αἰνίσσομαι"]
        + [""] * 14
    )
    res = sl_sem.build_paths(row)
    assert [str(p) for p in res] == ["≠ на\ue20dѧт\ue205"]
    assert res == [Path(parts=["на\ue20dѧт\ue205", "≠"])]


def test_add_usage():
    usages = [
        Usage(
            idx=Index(
                ch=1,
                alt=True,
                page=168,
                col="a",
                row=25,
                word="μονογενοῦς",
            ),
            lang="gr",
            var="G",
            trans_alt=Alternative(
                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                var_lemmas={"H": "\ue201д\ue205нородъ"},
            ),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=False,
                page=5,
                col="a",
                row=4,
                word="μονογενὴς",
            ),
            lang="gr",
            trans_alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=False,
                page=4,
                col="c",
                row=15,
                word="μονογενοῦς",
            ),
            lang="gr",
            trans_alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=True,
                page=168,
                col="a",
                row=25,
                word="μονογενοῦς",
            ),
            lang="gr",
            var="H",
            trans_alt=Alternative(
                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                var_lemmas={"G": "\ue205но\ue20dѧдъ"},
            ),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=True,
                page=168,
                col="a",
                row=28,
                word="μονογενοῦς",
            ),
            lang="gr",
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=True,
                page=168,
                col="a",
                row=25,
                word="μονογενοῦς",
            ),
            lang="gr",
            trans_alt=Alternative(
                var_lemmas={
                    "H": "\ue201д\ue205нородъ",
                    "G": "\ue205но\ue20dѧдъ",
                }
            ),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=False,
                page=5,
                col="a",
                row=4,
                word="μονογενὴς",
            ),
            lang="gr",
            var="WH",
            trans_alt=Alternative(main_lemma="\ue205но\ue20dѧдъ "),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=False,
                page=4,
                col="c",
                row=15,
                word="μονογενοῦς",
            ),
            lang="gr",
            var="WH",
            trans_alt=Alternative(main_lemma="\ue205но\ue20dѧдъ"),
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
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=False,
                                page=4,
                                col="c",
                                row=15,
                                word="μονογενοῦς",
                            ),
                            lang="gr",
                            trans_alt=Alternative(
                                var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}
                            ),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=False,
                                page=4,
                                col="c",
                                row=15,
                                word="μονογενοῦς",
                            ),
                            lang="gr",
                            var="WH",
                            trans_alt=Alternative(main_lemma="\ue205но\ue20dѧдъ"),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=False,
                                page=5,
                                col="a",
                                row=4,
                                word="μονογενὴς",
                            ),
                            lang="gr",
                            trans_alt=Alternative(
                                var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}
                            ),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=False,
                                page=5,
                                col="a",
                                row=4,
                                word="μονογενὴς",
                            ),
                            lang="gr",
                            var="WH",
                            trans_alt=Alternative(main_lemma="\ue205но\ue20dѧдъ "),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                word="μονογενοῦς",
                            ),
                            lang="gr",
                            trans_alt=Alternative(
                                var_lemmas={
                                    "H": "\ue201д\ue205нородъ",
                                    "G": "\ue205но\ue20dѧдъ",
                                }
                            ),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=28,
                                word="μονογενοῦς",
                            ),
                            lang="gr",
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                word="μονογενοῦς",
                            ),
                            lang="gr",
                            var="G",
                            trans_alt=Alternative(
                                "\ue201д\ue205но\ue20dѧдъ",
                                var_lemmas={"H": "\ue201д\ue205нородъ"},
                            ),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                word="μονογενοῦς",
                            ),
                            lang="gr",
                            var="H",
                            trans_alt=Alternative(
                                "\ue201д\ue205но\ue20dѧдъ",
                                var_lemmas={"G": "\ue205но\ue20dѧдъ"},
                            ),
                        ),
                    ]
                )
            }
        }
    )


def test_LangSemantics_compile_words_by_lemma():
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

    result = sl_sem.var.compile_words_by_lemma(row, "WGH")
    assert result == "б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G"

    row = (
        ["ѿ WG  ѡ H", "отъ"]
        + [""] * 2
        + ["1/5d11"]
        + ["om.", ""] * 2
        + [""] * 2
        + ["ἐπὶ", "ἐπί", "ἐπί + Gen."]
        + [""] * 13
    )

    result = sl_sem.var.compile_words_by_lemma(row, "WGH")
    assert result == "ѡ H ѿ WG"

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
        + [""] * 14
    )
    result = sl_sem.var.compile_words_by_lemma(row, "H")
    assert result == "днородоу H"
