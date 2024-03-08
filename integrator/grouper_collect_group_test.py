from setup import sl_sem, gr_sem
from hiliting import Hiliting

from grouper import _collect_group


def test_zemenu():
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
    res = _collect_group(rows, sl_sem, gr_sem, h)
    assert (
        res
        == [""] * 5
        + ["ₓ ꙁемьнꙑ\ue205"]
        + [""] * 10
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ Ch", "", "ὁ ἐπὶ γῆς Ch"]
        + [""] * 6
    )


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
        + ["hl00"],
        ["пꙋт\ue205 GH", "пѫть GH"] + [""] * 24 + ["hl00:AAAAAAAA"],
    ]
    h = Hiliting(rows, sl_sem, gr_sem)
    result = _collect_group(rows, sl_sem, gr_sem, h)
    assert result == (
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст\ue205\ue201 & пѫть G / шьств\ue205\ue201 & пѫть H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
        ]
        + [""] * 2
        + ["поутошьств\ue205ꙗ"]
        + [""] * 5
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
    )


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
    result = _collect_group(rows, gr_sem, sl_sem, h)

    assert (
        result
        == ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 3
        + ["пропѧтоу бꙑт\ue205•", "", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι"]
        + [""] * 14
    )


def test_sloves_inverse():
    rows = [
        [""] * 5
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

    result = _collect_group(rows, gr_sem, sl_sem, h)

    assert (
        result
        == [""] * 5
        + ["ₓ словесъ", "", "слово"]
        + [""] * 3
        + ["τῶν εἰρημένων", "", "τὸ εἰρημένον"]
        + [""] * 12
    )


def test_rechi():
    group = [
        ["бꙑше H", "бꙑт\ue205", "", "gramm.", "25/123b05"]
        + ["om.", ""] * 2
        + [""] * 3
        + ["gramm."]
        + [""] * 13
        + ["hl00:FFF8CBAD|hl03:FFBDD7EE"]
        + ["1"] * 4,
        ["рекл\ue205 H", "рещ\ue205"]
        + [""] * 2
        + ["25/123b05", "рѣша", "ко г\ue010лще рѣша• ꙗ-", "рещ\ue205"]
        + [""] * 3
        + ["φασὶν", "φημί"]
        + [""] * 13
        + ["hl00:FFF8CBAD"]
        + ["1"] * 4,
    ]

    h = Hiliting(group, sl_sem, gr_sem)
    res = _collect_group(group, sl_sem, gr_sem, h)

    assert res == (
        [
            "бꙑше рекл\ue205 H",
            "бꙑт\ue205 & рещ\ue205 H",
            "",
            "",
            "",
            "om. рѣша",
            "",
            "",
            "",
        ]
        + [""] * 2
        + ["φασὶν", "φημί"]
        + [""] * 13
    )


def test_smeromoudrost():
    rows = [
        [
            "смѣроумоудрост\ue205 WG  смѣрены\ue201 H",
            "съмѣрѹмѫдрость WG / съмѣр\ue201нъ H",
            "съмѣр\ue201наꙗ мѫдрость H",
            "",
            "25/125a03",
            "съмѣромоудрост\ue205",
            "съмѣромоудро-",
            "съмѣромѫдрость",
        ]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη"]
        + [""] * 8
        + ["hl00:FFFCD5B4"],
        ["моудрост H", "мѫдрость"] + [""] * 24 + ["hl00:FFFCD5B4"],
    ]
    h = Hiliting(rows, sl_sem.var, gr_sem)
    result = _collect_group(rows, sl_sem.var, gr_sem, h)
    assert result == (
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
            "",
            "съмѣр\ue201наꙗ мѫдрость H",
            "",
            "",
            "съмѣромоудрост\ue205",
            "",
            "съмѣромѫдрость",
        ]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
    )


def test_i_procii():
    rows = [
        [""] * 4
        + ["05/029d09"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["om."]
        + [""] * 4
        + [
            "τὰ MiPcPdPePgPhPiPkPpTVaVbVdYZaBSpPaLAVPoFd",
            "ὁ MiPcPdPePgPhPiPkPpTVaVbVdYZaBSpPaLAVPoFd",
        ]
        + [""] * 8
        + ["hl16:FFFCD5B4|hl19:FFB8CCE4"],
        [""] * 4
        + [
            "05/29d09",
            "про\ue20dе\ue201•",
            "\ue205 жьнѧ\ue205 • \ue205 про-",
            "про\ue20d\ue205\ue205",
        ]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + [
            "ἑξῆς MiPcPdPePgPhPiPkPpTVaVbVdYZaBSpPaLAVPoFd",
            "ἑξῆς MiPcPdPePgPhPiPkPpTVaVbVdYZaBSpPaLAVPoFd",
            "ὁ ἑξῆς",
        ]
        + [""] * 7
        + ["hl16:FFFCD5B4"],
    ]
    h = Hiliting(rows, gr_sem.var, sl_sem)
    result = _collect_group(rows, gr_sem.var, sl_sem, h)
    assert (
        result
        == [""] * 5
        + ["ₓ про\ue20dе\ue201•", "", "про\ue20d\ue205\ue205"]
        + [""] * 3
        + ["om. om."]
        + [""] * 4
        + [
            "τὰ ἑξῆς MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp",
            "",
            "ὁ ἑξῆς MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp",
        ]
        + [""] * 7
    )


def test_gen_lemma2():
    rows = [
        [""] * 4
        + ["14/71c11", "въ\ue205ноу", "ща въ\ue205ноу• по-", "въ\ue205нѫ"]
        + [""] * 3
        + ["διηνεκῶς"] * 2
        + [""] * 3
        + ["διὰ MVPa", "διά", "διά + Gen", "διὰ παντός"]
        + [""] * 6
        + ["hl16:FFFCD5B5|hl18:FF92D050"],
        [""] * 16 + ["παντός MVPa", "πᾶς"] + [""] * 8 + ["hl16:FFFCD5B5"],
    ]

    h = Hiliting(rows, gr_sem.var, sl_sem)
    result = _collect_group(rows, gr_sem.var, sl_sem, h)

    assert (
        result
        == [""] * 5
        + ["въ\ue205ноу", "", "въ\ue205нѫ"]
        + [""] * 3
        + ["διηνεκῶς"] * 2
        + [""] * 3
        + ["διὰ παντός MVPa", "", "", "διὰ παντός MVPa"]
        + [""] * 6
    )


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

    h = Hiliting(rows, sl_sem, gr_sem)
    res = _collect_group(rows, sl_sem, gr_sem, h)
    assert (
        res
        == [""] * 5
        + ["ₓ авраамовоу ₓ \ue20dадь"]
        + [""] * 2
        + ["авраамова \ue20dѧдь"]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "περί & Ἀβραάμ", "", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
    )


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
    res = _collect_group(rows, gr_sem, sl_sem, h)
    assert (
        res
        == [""] * 5
        + ["ₓ авраамовоу ₓ \ue20dадь"]
        + ["", "авраамовъ & \ue20dѧдь"]
        + ["авраамова \ue20dѧдь"]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "", "", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
    )
