from config import FROM_LANG, TO_LANG
from model import Source
from semantics import MainLangSemantics, VarLangSemantics
from setup import sl_sem, gr_sem


def test_VarLangSemantics_multiword():
    sem = VarLangSemantics(FROM_LANG, 0, [1])
    result = sem.multiword(["ноедаго G  днородоу H", "днородъ H / ноѧдъ G"])
    assert len(result) == 2
    assert result["G"] == ("\ue205но\ue20dедаго")
    assert result["H"] == ("\ue201д\ue205нородоу")

    result = sem.multiword(["ноедаго G", "днородъ H / ноѧдъ G"])
    assert result == {"G": ("\ue205но\ue20dедаго")}

    result = sem.multiword(["", ""])
    assert result == {Source("WGH"): ("")}

    result = sem.multiword(["дноеды WH Ø G", "дноѧдъ"])
    assert result == {Source("WH"): ("дноеды"), Source("G"): ("Ø")}

    result = sem.multiword(["дноеды", "дноѧдъ"])
    assert result == {Source("WGH"): "дноеды"}

    gr_sem = VarLangSemantics(TO_LANG, 0, [1])
    result = gr_sem.multiword(["με C", "ἐγώ"])
    assert result == {"C": "με"}


def test_repeated():
    sem = VarLangSemantics(FROM_LANG, 0, [1])
    result = sem.multiword(["ноедаго G  днородоу H", "днородъ H / ноѧдъ G"])
    assert len(result) == 2
    assert result["G"] == "\ue205но\ue20dедаго"
    assert result["H"] == "\ue201д\ue205нородоу"


def test_greek_paris():
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


def test_bozhii():
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


def test_gr_variant():
    row = (
        [""] * 4
        + ["16/80a08", "хлѣбꙑ•", "ре\ue20dе хлѣбꙑ• не", "хлѣбъ"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 3
        + ["ἄρτους Ch", "ἄρτος"]
        + [""] * 9
        + ["1"] * 4
    )
    result = gr_sem.var.multiword(row)
    assert result == {Source("Ch"): "ἄρτους"}


def test_multiword_puteshestive():
    assert sl_sem.var.multiword(
        ["шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H"]
    ) == {Source("G"): "шьст\ue205ꙗ пꙋт\ue205", Source("H"): "шьств\ue205ꙗ пꙋт\ue205"}

    assert sl_sem.var.multiword(["шьст\ue205ꙗ G шьств\ue205ꙗ H пꙋт\ue205 GH"]) == {
        Source("G"): "шьст\ue205ꙗ пꙋт\ue205",
        Source("H"): "шьств\ue205ꙗ пꙋт\ue205",
    }


def test_collect_multiword_puteshestive():
    rows = [
        [
            "шьст\ue205ꙗ G шьств\ue205ꙗ H",
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
            "пꙋт\ue205 GH",
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

    assert (
        sl_sem.var.collect_word(rows)
        == "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H"
    )


def test_collect_multiword_prichatnik_biti():
    rows = [
        [
            "пр\ue205\ue20dестьн\ue205ц\ue205 б• G  пр\ue205\ue20dестн\ue205ц\ue205 б• H",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/28c21",
            "пр\ue205\ue20dьтьн\ue205ц\ue205",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
            "",
            "",
            "ποιῆσαι",
            "ποιέω",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05|hl11"],
        ["боудемь W"]
        + ["бꙑт"]
        + [""] * 2
        + ["05/28d01", "боудоуть", "боудоуть• \ue201же", "бꙑт\ue205"]
        + [""] * 3
        + ["κοινωνοὺς", "κοινωνός"]
        + [""] * 13
        + ["hl05|hl11"],
    ]

    assert (
        sl_sem.var.collect_word(rows)
        == "пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H боудемь W"
    )
