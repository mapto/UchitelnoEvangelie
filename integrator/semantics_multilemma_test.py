from model import Source
from semantics import MainLangSemantics, VarLangSemantics


from config import FROM_LANG, TO_LANG


def test_LangSemantics_multilemma():
    # old semantics
    sl_sem = MainLangSemantics(
        FROM_LANG, 4, [6, 7, 8, 9], VarLangSemantics(FROM_LANG, 0, [1, 2])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 10, [11, 12, 13], VarLangSemantics(TO_LANG, 15, [16, 17])
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

    dummy_sem = MainLangSemantics(
        FROM_LANG, 2, [3], VarLangSemantics(FROM_LANG, 0, [1])
    )

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

    dummy_sem2 = VarLangSemantics(TO_LANG, 0, [1])
    result = dummy_sem2.multilemma(["με C", "ἐγώ"])
    assert result == {"C": "ἐγώ"}

    # semantics update from September 2021
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
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


def test_sub():
    # old semantics
    sl_sem = MainLangSemantics(
        FROM_LANG, 4, [6, 7, 8, 9], VarLangSemantics(FROM_LANG, 0, [1, 2])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 10, [11, 12, 13], VarLangSemantics(TO_LANG, 15, [16, 17])
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
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
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


def test_paris():
    """Greek opies held in Paris library are indicated by P?"""
    # old semantics, so that variants are in word, not lemma
    gr_sem = MainLangSemantics(
        TO_LANG, 10, [11, 12, 13], VarLangSemantics(TO_LANG, 15, [16, 17])
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


def test_bozhii():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
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
