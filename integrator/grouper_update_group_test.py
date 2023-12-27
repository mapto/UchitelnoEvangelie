from setup import sl_sem, gr_sem
from hiliting import Hiliting
from grouper import _update_group

# INFO:root:Събиране на многоредови преводи от славянски основен към гръцки...
raw = [
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
    + ["hl05:FFFCD5B4|hl09:FFB8CCE4"],
]


def test_raspetou_inverse():
    rows = [r.copy() for r in raw]
    h = Hiliting(rows, gr_sem, sl_sem)
    line = (
        ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 3
        + ["пропѧтоу бꙑт\ue205•", "", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι"]
        + [""] * 14
    )

    result = _update_group(rows, gr_sem, sl_sem, line, h)

    assert result == [
        ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 2
        + ["18/089c21", "пропѧтоу бꙑт\ue205•", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"],
        ["распетоу WG"]
        + [""] * 3
        + [
            "18/89c21-d01",
            "пропѧтоу бꙑт\ue205•",
            "же пропѧтоу бꙑ-",
            "бꙑт\ue205",
            "",
            "gramm.",
            "",
            "σταυρωθῆναι",
            "pass.",
        ]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl09:FFB8CCE4"],
    ]


def test_sloves_inverse():
    rows = [
        [""] * 4
        + ["38/178c06"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τῶν", "ὁ"]
        + [""] * 13
        + ["hl11:FFFCD5B4|hl14:FFB8CCE4"],
        [""] * 4
        + ["38/178c06", "словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
        + [""] * 3
        + ["εἰρημένων", "λέγω", "τὸ εἰρημένον"]
        + [""] * 12
        + ["hl11:FFFCD5B4"],
    ]

    h = Hiliting(rows, gr_sem, sl_sem)
    line = (
        [""] * 5
        + ["ₓ словесъ", "", "слово"]
        + [""] * 3
        + ["τῶν εἰρημένων", "", "τὸ εἰρημένον"]
        + [""] * 12
    )

    result = _update_group(rows, gr_sem, sl_sem, line, h)

    assert result == [
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "", "ₓ"]
        + [""] * 3
        + ["τῶν εἰρημένων", "ὁ"]
        + [""] * 13
        + ["hl11:FFFCD5B4|hl14:FFB8CCE4"],
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
        + [""] * 3
        + ["τῶν εἰρημένων", "λέγω", "τὸ εἰρημένον"]
        + [""] * 12
        + ["hl11:FFFCD5B4"],
    ]


def test_zemen():
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

    line = (
        [""] * 5
        + ["ₓ ꙁемьнꙑ\ue205"]
        + [""] * 10
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ", "", "ὁ ἐπὶ γῆς"]
        + [""] * 6
    )

    res = _update_group(rows, sl_sem, gr_sem, line, h)
    assert res == [
        [""] * 4
        + ["19/94d08", "ₓ ꙁемьнꙑ\ue205", "", "ₓ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "ὁ"]
        + [""] * 8
        + ["hl16:AAAAAAAA|hl19:AAAAAAAA"],
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ", "", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16:AAAAAAAA|hl18:AAAAAAAA"],
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205"]
        + [""] * 10
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ", "", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16:AAAAAAAA"],
    ]


def test_puteshestvie():
    rows = [
        [
            "шьст\ue205ꙗ G шьств\ue205ꙗ H",
            "шьст\ue205\ue201 G / шьств\ue205\ue201 H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/28d18",
            "поутошьств\ue205ꙗ",
            "поутошьств\ue205-",
            "пѫтошьств\ue205\ue201",
        ]
        + [""] * 3
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00:AAAAAAAA"],
        ["пꙋт\ue205 GH", "пѫть GH"] + [""] * 24 + ["hl00:AAAAAAAA"],
    ]
    merge = (
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст\ue205\ue201 пѫть G шьств\ue205\ue201 пѫть H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
        ]
        + [""] * 2
        + ["поутошьств\ue205ꙗ"]
        + [""] * 5
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
    )
    h = Hiliting(rows, sl_sem, gr_sem)
    result = _update_group(rows, sl_sem, gr_sem, merge, h)
    assert result == [
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст\ue205\ue201 пѫть G шьств\ue205\ue201 пѫть H",
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
        + ["hl00:AAAAAAAA"],
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст\ue205\ue201 пѫть G шьств\ue205\ue201 пѫть H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/028d18",
            "поутошьств\ue205ꙗ",
        ]
        + [""] * 5
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00:AAAAAAAA"],
    ]


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

    line = (
        [""] * 5
        + ["вьꙁмогл\ue205 б\ue205хомь"]
        + [""] * 5
        + ["ἠδυνήθημεν", "δύναμαι"]
        + [""] * 13
    )

    h = Hiliting(group, sl_sem, gr_sem)
    res = _update_group(group, sl_sem, gr_sem, line, h)
    e1 = (
        [""] * 4
        + [
            "01/W168a14-15",
            "вьꙁмогл\ue205 б\ue205хомь",
            "мы брьньн\ue205 \ue205 ꙁемⷧ҇ьн\ue205\ue205• вьꙁмогл\ue205",
            "въꙁмощ\ue205",
        ]
        + [""] * 3
        + ["ἠδυνήθημεν", "δύναμαι"]
        + [""] * 13
        + ["hl05:AAAAAAAA"]
    )
    e2 = (
        [""] * 4
        + [
            "1/W168a15",
            "вьꙁмогл\ue205 б\ue205хомь",
            "б\ue205хомь стрьпѣтї• ",
            "бꙑт\ue205 ",
            "",
            "gramm.",
            "",
            "ἠδυνήθημεν",
            "pass.",
        ]
        + [""] * 13
        + [
            "hl05:AAAAAAAA|hl09:AAAAAAAA",
        ]
    )
    expected = [e1, e2]
    assert res == expected


def test_avramov_chad():
    rows = [
        [""] * 4
        + ["05/24b21"]
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

    line = (
        [""] * 5
        + ["ₓ авраамовоу ₓ \ue20dадь"]
        + [""] * 2
        + ["авраамова \ue20dѧдь"]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "περί & Ἀβραάμ", "", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
    )

    h = Hiliting(rows, sl_sem, gr_sem)
    res = _update_group(rows, sl_sem, gr_sem, line, h)

    assert res == [
        [""] * 4
        + ["05/24b21", "ₓ авраамовоу ₓ \ue20dадь", "", "ₓ"]
        + [""] * 3
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + [
            "05/024b21-c01",
            "ₓ авраамовоу ₓ \ue20dадь",
            "н\ue205ша сѧ• авраа-",
            "авраамовъ",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "περί & Ἀβραάμ", "", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl13:FF92D050"],
        [""] * 5
        + ["ₓ авраамовоу ₓ \ue20dадь", "", "ₓ"]
        + [""] * 3
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + [
            "05/024b21-c01",
            "ₓ авраамовоу ₓ \ue20dадь",
            "мовоу \ue20dадь г\ue010лю-",
            "\ue20dѧдь",
            "авраамова \ue20dѧдь",
            "",
            "",
            "τοὺς περὶ τὸν Ἀβραὰμ",
            "περί & Ἀβραάμ",
            "",
            "ὁ περὶ τὸν Ἀβραάμ",
        ]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4"],
    ]


def test_avramov_chad_inv():
    rows = [
        [""] * 4
        + ["05/24b21"]
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

    h = Hiliting(rows, gr_sem, sl_sem)
    """
    from grouper import _collect_group
    line = _collect_group(rows, gr_sem, sl_sem, h)
    assert line == (
        [""] * 5
        + ["ₓ авраамовоу ₓ \ue20dадь", "", "авраамовъ & \ue20dѧдь"]
        + ["авраамова \ue20dѧдь"]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "", "", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
    )
    """
    line = (
        [""] * 5
        + ["ₓ авраамовоу ₓ \ue20dадь", "", "авраамовъ & \ue20dѧдь"]
        + ["авраамова \ue20dѧдь"]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "", "", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
    )

    res = _update_group(rows, gr_sem, sl_sem, line, h)

    assert res == [
        [""] * 4
        + ["05/24b21", "ₓ авраамовоу ₓ \ue20dадь", "", "ₓ"]
        + [""] * 3
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "ὁ", "", ""]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + [
            "05/024b21-c01",
            "ₓ авраамовоу ₓ \ue20dадь",
            "н\ue205ша сѧ• авраа-",
            "авраамовъ & \ue20dѧдь",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "περί", "περί + Acc.", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl13:FF92D050"],
        [""] * 5
        + ["ₓ авраамовоу ₓ \ue20dадь", "", "ₓ"]
        + [""] * 3
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "ὁ", "", ""]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + [
            "05/024b21-c01",
            "ₓ авраамовоу ₓ \ue20dадь",
            "мовоу \ue20dадь г\ue010лю-",
            "авраамовъ & \ue20dѧдь",
            "авраамова \ue20dѧдь",
            "",
            "",
            "τοὺς περὶ τὸν Ἀβραὰμ",
            "Ἀβραάμ",
            "",
            "ὁ περὶ τὸν Ἀβραάμ",
        ]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4"],
    ]
