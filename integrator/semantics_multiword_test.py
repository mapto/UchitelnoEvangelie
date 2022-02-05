from model import Source
from semantics import MainLangSemantics, VarLangSemantics


def test_VarLangSemantics_multiword():
    sem = VarLangSemantics("sl", 0, [1])
    result = sem.multiword(["ноедаго G  днородоу H", "днородъ H / ноѧдъ G"])
    assert len(result) == 2
    assert result["G"] == ("\ue205но\ue20dедаго", 1)
    assert result["H"] == ("\ue201д\ue205нородоу", 1)

    result = sem.multiword(["ноедаго G", "днородъ H / ноѧдъ G"])
    assert result == {"G": ("\ue205но\ue20dедаго", 1)}

    result = sem.multiword(["", ""])
    assert result == {Source("WGH"): ("", 1)}

    result = sem.multiword(["дноеды WH Ø G", "дноѧдъ"])
    assert result == {Source("WH"): ("дноеды", 1), Source("G"): ("Ø", 1)}

    result = sem.multiword(["дноеды", "дноѧдъ"])
    assert result == {Source("WGH"): ("дноеды", 1)}

    gr_sem = VarLangSemantics("gr", 0, [1])
    result = gr_sem.multiword(["με C", "ἐγώ"])
    assert result == {"C": ("με", 1)}


def test_repeated():
    sem = VarLangSemantics("sl", 0, [1])
    result = sem.multiword(
        ["ноедаго\u2083 G  днородоу\u2084 H", "днородъ H / ноѧдъ G"]
    )
    assert len(result) == 2
    assert result["G"] == ("\ue205но\ue20dедаго", 3)
    assert result["H"] == ("\ue201д\ue205нородоу", 4)


def test_greek_paris():
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
    assert result == {"MPaPb": ("τιμᾷ", 1)}

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
    assert result == {Source("CMPcPa"): ("ἀνάκλησιν", 1)}


def test_bozhii():
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
        "G": ("б\ue010ж\ue205\ue205", 1),
        "H": ("б\ue010жї\ue205", 1),
        "W": ("б\ue010ж\ue205", 1),
    }
