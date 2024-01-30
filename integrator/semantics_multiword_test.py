from config import FROM_LANG, TO_LANG
from model import Source
from semantics import VarLangSemantics
from setup import sl_sem, gr_sem


def test_basic():
    sem = VarLangSemantics(FROM_LANG, 0, [1])
    result = sem.multiword(["ноедаго G  днородоу H", "днородъ H / ноѧдъ G"])
    assert result == {
        Source("H"): "\ue201д\ue205нородоу",
        Source("G"): "\ue205но\ue20dедаго",
    }

    result = sem.multiword(["ноедаго G", "днородъ H / ноѧдъ G"])
    assert result == {"G": ("\ue205но\ue20dедаго")}

    result = sem.multiword(["", ""])
    assert result == {Source("WGH"): ("")}

    result = sem.multiword(["дноеды WH Ø G", "дноѧдъ"])
    assert result == {Source("WH"): ("дноеды"), Source("G"): ("Ø")}

    result = sem.multiword(["дноеды", "дноѧдъ"])
    assert result == {Source("WGH"): "дноеды"}

    gr_sem = VarLangSemantics(TO_LANG, 0, [1])
    result = gr_sem.multiword(["με Cs", "ἐγώ"])
    assert result == {"Cs": "με"}


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
    assert result == {Source("MPaPb"): "τιμᾷ"}

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
        + ["ἀνάκλησιν CsMPcPa"]
        + [""] * 10
    )
    result = gr_sem.var.multiword(row)
    assert result == {Source("CsMPcPa"): "ἀνάκλησιν"}


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


def test_puteshestive():
    assert sl_sem.var.multiword(
        ["шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H"]
    ) == {Source("G"): "шьст\ue205ꙗ пꙋт\ue205", Source("H"): "шьств\ue205ꙗ пꙋт\ue205"}

    assert sl_sem.var.multiword(["шьст\ue205ꙗ G шьств\ue205ꙗ H пꙋт\ue205 GH"]) == {
        Source("G"): "шьст\ue205ꙗ пꙋт\ue205",
        Source("H"): "шьств\ue205ꙗ пꙋт\ue205",
    }


def test_iako_obrazom():
    row = (
        [
            "om. WG",
            "\ue205 conj. H",
            "\ue205 H",
            "",
            "51/232d03",
            "\ue205",
            "ꙗкоже \ue205 обра-",
            "\ue205 conj.",
        ]
        + [""] * 3
        + ["μὲν", "μέν"]
        + [""] * 13
        + ["hl05:FFFCD5B4"]
    )
    result = sl_sem.var.multiword(row)
    # assert result == {Source("H"): ""}
    assert result == {Source("WG"): "om."}


def test_gr_dat():
    row = (
        ["к WGH", "къ"]
        + [""] * 2
        + ["13/69a30"]
        + ["om.", ""] * 2
        + [""] * 2
        + ["om."]
        + [""] * 4
        + ["Dat. Nt", "Dat."]
        + [""] * 8
        + ["bold|italic"]
        + ["1"] * 4
    )
    result = gr_sem.var.multiword(row)
    assert result == {Source("Nt"): "Dat."}
