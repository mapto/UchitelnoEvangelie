from const import V_LEMMA_SEP
from setup import sl_sem, gr_sem


def test_collect_puteshestvie():
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
        sl_sem.var.collect_lemma(rows, separator=V_LEMMA_SEP)
        == "шьст & пѫть G / шьств & пѫть H"
    )


def test_zemenu():
    rows = [
        [""] * 4
        + ["19/94d08", "ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["ἐπὶ Ch", "ἐπί", "ἐπί + Gen.", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16|hl18"],
        [""] * 4 + ["19/94d08"] + [""] * 11 + ["γῆς Ch", "γῆ"] + [""] * 8 + ["hl16"],
    ]

    assert (
        gr_sem.var.collect_lemma(rows, gr_sem.var.lemmas[0], V_LEMMA_SEP)
        == "ἐπί & γῆ Ch"
    )


def test_tyam_ili():
    rows = [
        [
            "тѣмь WH",
            "",
            "тѣмь \ue205л\ue205",
            "",
            "1/6a10",
            "тѣмь",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь",
            "тѣмь л\ue205",
            "",
            "",
            "κἂν",
            "κἄν",
        ]
        + [""] * 13
        + ["hl05"],
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "",
            "1/6a10",
            "л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "л\ue205",
        ]
        + [""] * 18
        + ["hl05"],
    ]

    assert gr_sem.collect_lemma(rows, gr_sem.lemmas[0]) == "κἄν"
    assert (
        sl_sem.var.collect_lemma(rows, sl_sem.var.lemmas[1]) == "тѣмь \ue205л\ue205 WH"
    )


def test_iako_obrazom():
    rows = [
        ["ꙗко WGH"]
        + ["ꙗко"] * 2
        + ["", "51/232d03"]
        + ["ꙗкоже", "ꙗкоже \ue205 обраꙁомь"] * 2
        + [""] * 2
        + ["προσχήματι", "πρόσχημα", "προσχήματι μέν"]
        + [""] * 12
        + ["hl05:FFFCD5B4"],
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
        + ["hl05:FFFCD5B4"],
        [
            "обраꙁомь WGH",
            "обраꙁъ",
            "обраꙁомь",
            "",
            "51/232d03",
            "обраꙁъмь",
            "ꙗкоже \ue205 обра-",
            "обраꙁъ",
        ]
        + [""] * 18
        + ["hl05:FFFCD5B4"],
    ]

    assert (
        sl_sem.var.collect_lemma(rows, sl_sem.var.lemmas[0])
        == "ꙗко обраꙁъ WG / ꙗко \ue205 conj. обраꙁъ H"
    )
    assert (
        sl_sem.var.collect_lemma(rows, sl_sem.var.lemmas[1])
        == "ꙗко обраꙁомь WG / ꙗко \ue205 обраꙁомь H"
    )
