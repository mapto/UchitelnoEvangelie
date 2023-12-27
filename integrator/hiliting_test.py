from setup import sl_sem, gr_sem
from hiliting import Hiliting, _hilited_irrelevant


def test_hilited_gram():
    rows = [
        ["распетоу WG", "распѧт\ue205"]
        + [""] * 2
        + ["18/89c21", "пропѧтоу", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"],
        [""] * 4
        + ["18/89c21-d01", "бꙑт\ue205•", "же пропѧтоу бꙑ-", "бꙑт\ue205", "", "gramm."]
        + [""] * 2
        + ["pass."]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"],
    ]
    h = Hiliting(rows, gr_sem, sl_sem)
    assert h.merge_rows == {0}


def test_gram_merge_rows():
    rows = [
        [""] * 4
        + ["19/94d08"]
        + ["ₓ", ""] * 2
        + [""] * 7
        + ["τῶν Ch", "ὁ"]
        + [""] * 8
        + ["hl16:AAAAAAAA|hl19:AAAAAAAA"],
        [""] * 4
        + ["19/94d08", "ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["ἐπὶ Ch", "ἐπί", "ἐπί + Gen.", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16:AAAAAAAA|hl18:AAAAAAAA"],
        [""] * 4
        + ["19/94d08"]
        + [""] * 11
        + ["γῆς Ch", "γῆ"]
        + [""] * 8
        + ["hl16:AAAAAAAA"],
    ]

    h = Hiliting(rows, sl_sem, gr_sem)
    assert h.merge_rows == {1, 2}


def test_raspatu():
    rows = [
        ["распетоу WG", "распѧт\ue205"]
        + [""] * 2
        + ["18/89c21", "пропѧтоу", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"],
        [""] * 4
        + ["18/89c21-d01", "бꙑт\ue205•", "же пропѧтоу бꙑ-", "бꙑт\ue205", "", "gramm."]
        + [""] * 2
        + ["pass."]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"],
    ]

    h = Hiliting(rows, sl_sem, gr_sem)
    assert h.merge_rows == {0}

    h = Hiliting(rows, gr_sem, sl_sem)
    assert h.merge_rows == {0}


def test_biti():
    g1 = (
        [""] * 4
        + [
            "1/W168a14",
            "вьꙁмогл\ue205",
            "мы брьньн\ue205 \ue205 ꙁемⷧ҇ьн\ue205\ue205• вьꙁмогл\ue205",
            "въꙁмощ\ue205",
        ]
        + [""] * 3
        + [
            "ἠδυνήθημεν",
            "δύναμαι",
        ]
        + [""] * 13
        + [
            "hl05:AAAAAAAA",
        ]
    )
    g2 = (
        [""] * 4
        + [
            "1/W168a15",
            "б\ue205хомь",
            "б\ue205хомь стрьпѣтї• ",
            "бꙑт\ue205 ",
            "",
            "gramm.",
        ]
        + [""] * 2
        + [
            "pass.",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    group = [g1.copy(), g2.copy()]

    h = Hiliting(group, sl_sem, gr_sem)
    assert h.merge_rows == {0}


def test_avramov_chad():
    r1 = (
        [""] * 4
        + ["05/24b21"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τοὺς", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"]
    )
    r2 = (
        [""] * 4
        + ["05/24b21", "авраамовоу", "н\ue205ша сѧ• авраа-", "авраамовъ"]
        + [""] * 3
        + ["περὶ", "περί", "περί + Acc.", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl13:FF92D050"]
    )
    r3 = (
        [""] * 4
        + ["", "ₓ"] * 2
        + [""] * 3
        + ["τὸν", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"]
    )
    r4 = (
        [""] * 4
        + [
            "05/24c01",
            "\ue20dадь",
            "мовоу \ue20dадь г\ue010лю-",
            "\ue20dѧдь",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["Ἀβραὰμ", "Ἀβραάμ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4"]
    )

    rows = [r1, r2, r3, r4]

    h = Hiliting(rows, sl_sem, gr_sem)

    assert h.non_local_group == [r2, r4]
    assert h.relevant_group(sl_sem) == [r2, r4]
    assert h.relevant_group(gr_sem) == [r4]
    assert h.group == rows

    h = Hiliting(rows, gr_sem, sl_sem)

    assert h.non_local_group == [r2, r4]
    assert h.relevant_group(sl_sem) == [r2, r4]
    assert h.relevant_group(gr_sem) == [r4]
    assert h.group == rows


def test_hilited_irrelevant():
    rows = [
        [""] * 4
        + ["05/24c01"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τοὺς", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + ["05/24b21", "авраамовоу", "н\ue205ша сѧ• авраа-", "авраамовъ"]
        + [""] * 3
        + ["περὶ", "περί", "περί + Acc.", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl13:FF92D050"],
        [""] * 4
        + ["", "ₓ"] * 2
        + [""] * 3
        + ["τὸν", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + [
            "05/24c01",
            "\ue20dадь",
            "мовоу \ue20dадь г\ue010лю-",
            "\ue20dѧдь",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["Ἀβραὰμ", "Ἀβραάμ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4"],
    ]

    for i, r in enumerate(rows):
        assert _hilited_irrelevant(gr_sem, r) == (i == 1)
        assert not _hilited_irrelevant(sl_sem, r)
        assert not _hilited_irrelevant(sl_sem.var, r)
        assert not _hilited_irrelevant(gr_sem.var, r)
