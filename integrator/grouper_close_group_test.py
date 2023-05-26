from const import IDX_COL

from setup import sl_sem, gr_sem
from hiliting import Hiliting

from grouper import _close_group


def test_mireni():
    raw = [
        [""] * 4
        + ["19/94d08", "\ue205", "", "\ue205 conj."]
        + [""] * 3
        + ["κάγω", "καί"]
        + [""] * 14,
        [""] * 5 + ["аꙁ", "", "аꙁъ"] + [""] * 3 + ["=", "ἐγώ"] + [""] * 14,
        [""] * 4
        + [
            "02/W169a17",
            "м\ue205рно\ue201•",
            "да\ue201 бран\ue205• ꙋтѣшен\ue205\ue201 м\ue205-",
            "м\ue205рьнъ",
        ]
        + [""] * 3
        + ["ἐκ", "ἐκ", "ἐκ τῆς εἰρήνης"]
        + [""] * 12
        + ["hl11:AAAAAAAA"],
        [""] * 5
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τῆς", "ὁ"]
        + [""] * 13
        + ["hl11:AAAAAAAA|hl14:AAAAAAAA"],
        [""] * 11 + ["εἰρήνης", "εἰρήνη"] + [""] * 13 + ["hl11:AAAAAAAA"],
    ]
    group = [r.copy() + ["1"] * 4 for r in raw[2:]]
    for r in group:
        r[IDX_COL] = "02/W169a17"

    h = Hiliting(group, sl_sem, gr_sem)
    res = _close_group(group, sl_sem, gr_sem, h)
    assert res == [
        [""] * 4
        + [
            "02/W169a17",
            "м\ue205рно\ue201• ₓ",
            "да\ue201 бран\ue205• ꙋтѣшен\ue205\ue201 м\ue205-",
            "м\ue205рьнъ",
        ]
        + [""] * 3
        + ["ἐκ τῆς εἰρήνης", "ἐκ & εἰρήνη", "ἐκ τῆς εἰρήνης"]
        + [""] * 12
        + ["hl11:AAAAAAAA"]
        + ["1"] * 4,
        [""] * 4
        + ["02/W169a17", "м\ue205рно\ue201• ₓ", "", "ₓ"]
        + [""] * 3
        + ["ἐκ τῆς εἰρήνης", "ὁ"]
        + [""] * 13
        + ["hl11:AAAAAAAA|hl14:AAAAAAAA"]
        + ["1"] * 4,
        [""] * 4
        + ["02/W169a17", "м\ue205рно\ue201• ₓ"]
        + [""] * 5
        + ["ἐκ τῆς εἰρήνης", "ἐκ & εἰρήνη", "ἐκ τῆς εἰρήνης"]
        + [""] * 12
        + ["hl11:AAAAAAAA"]
        + ["1"] * 4,
    ]


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
    + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"],
]


def test_raspetou_inverse():
    rows = [r.copy() for r in raw]
    h = Hiliting(rows, gr_sem, sl_sem)
    result = _close_group(rows, gr_sem, sl_sem, h)

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
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"],
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
    result = _close_group(rows, gr_sem, sl_sem, h)

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


def test_rechi():
    group = [
        ["бꙑше H", "бꙑт\ue205", "", "gramm.", "25/123b05"]
        + ["om.", ""] * 2
        + [""] * 3
        + ["gramm."]
        + [""] * 13
        + ["hl00:FFF8CBAD|hl03:FFBDD7EE"]
        + ["1"] * 4,
        ["рекл\ue205 H"]
        + [""] * 3
        + ["25/123b05", "рѣша", "ко г\ue010лще рѣша• ꙗ-", "рещ\ue205"]
        + [""] * 3
        + ["φασὶν", "φημί"]
        + [""] * 13
        + ["hl00:FFF8CBAD"]
        + ["1"] * 4,
    ]

    h = Hiliting(group, sl_sem, gr_sem)
    res = _close_group(group, sl_sem, gr_sem, h)

    assert res == [
        [
            "бꙑше рекл\ue205 H",
            "бꙑт\ue205",
            "",
            "gramm.",
            "25/123b05",
            "om. рѣша",
            "",
            "om.",
        ]
        + [""] * 3
        + ["φασὶν", "gramm."]
        + [""] * 13
        + ["hl00:FFF8CBAD|hl03:FFBDD7EE"]
        + ["1"] * 4,
        [
            "бꙑше рекл\ue205 H",
            "бꙑт\ue205 H",
            "",
            "",
            "25/123b05",
            "om. рѣша",
            "ко г\ue010лще рѣша• ꙗ-",
            "рещ\ue205",
        ]
        + [""] * 3
        + ["φασὶν", "φημί"]
        + [""] * 13
        + ["hl00:FFF8CBAD"]
        + ["1"] * 4,
    ]


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
    result = _close_group(rows, sl_sem.var, gr_sem, h)
    assert result == [
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
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
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
        + ["hl00:FFFCD5B4"],
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
            "съмѣрѹмѫдрость WG / мѫдрость H",
            "съмѣр\ue201наꙗ мѫдрость H",
            "",
            "25/125a03",
            "съмѣромоудрост\ue205",
            "",
            "съмѣромѫдрость",
        ]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
        + ["hl00:FFFCD5B4"],
    ]


def test_i_procii():
    rows = [
        [""] * 4
        + ["05/029d09"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["om."]
        + [""] * 4
        + ["τὰ MiPcPdPePgPhPiPkPpTVaVbVdYZaBSpPaLAVPoFd", "ὁ"]
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
        + ["ἑξῆς MiPcPdPePgPhPiPkPpTVaVbVdYZaBSpPaLAVPoFd", "ἑξῆς", "ὁ ἑξῆς"]
        + [""] * 7
        + ["hl16:FFFCD5B4"],
    ]
    h = Hiliting(rows, sl_sem.var, gr_sem)
    result = _close_group(rows, gr_sem.var, sl_sem, h)
    assert result == [
        [""] * 4
        + ["05/029d09", "ₓ про\ue20dе\ue201•", "", "ₓ"]
        + [""] * 3
        + ["om. om."]
        + [""] * 4
        + [
            "τὰ ἑξῆς MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp",
            "ὁ MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp",
        ]
        + [""] * 8
        + ["hl16:FFFCD5B4|hl19:FFB8CCE4"],
        [""] * 4
        + ["05/029d09"]
        + [
            "ₓ про\ue20dе\ue201•",
            "\ue205 жьнѧ\ue205 • \ue205 про-",
            "про\ue20d\ue205\ue205",
        ]
        + [""] * 3
        + ["om. om."]
        + [""] * 4
        + [
            "τὰ ἑξῆς MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp",
            "ἑξῆς MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp",
            "ὁ ἑξῆς MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp",
        ]
        + [""] * 7
        + ["hl16:FFFCD5B4"],
    ]
