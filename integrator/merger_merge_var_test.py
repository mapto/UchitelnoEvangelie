from setup import sl_sem, gr_sem
from merger import merge

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


def test_raspetou():
    rows = [r.copy() for r in raw]
    result = merge(rows, sl_sem, gr_sem)

    assert result == [
        ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 2
        + ["18/089c21", "пропѧтоу бꙑт\ue205•", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"]
        + ["1"] * 4,
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
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"]
        + ["1"] * 4,
    ]


def test_raspetou_var():
    rows = [r.copy() for r in raw]
    result = merge(rows, sl_sem.var, gr_sem)

    assert result == [
        ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 2
        + [
            "18/089c21",
            "пропѧтоу бꙑт\ue205•",
            "же пропѧтоу бꙑ-",
            "пропѧт\ue205 бꙑт\ue205",
        ]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"]
        + ["1"] * 4,
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
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"]
        + ["1"] * 4,
    ]


def test_raspetou_inverse():
    rows = [r.copy() for r in raw]
    result = merge(rows, gr_sem, sl_sem)

    assert result == [
        ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 2
        + ["18/089c21", "пропѧтоу бꙑт\ue205•", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"]
        + ["1"] * 4,
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
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"]
        + ["1"] * 4,
    ]


def test_smeromoudroust():
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
    result = merge(rows, sl_sem.var, gr_sem)
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
        + ["hl00:FFFCD5B4"]
        + ["1"] * 4,
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
        + ["hl00:FFFCD5B4"]
        + ["1"] * 4,
    ]


def test_v():
    row = [
        "",
        "",
        "",
        "",
        "35/162a10",
        "въ",
        "въ \ue205ер\ue205хѫ• съвы-",
        "въ",
        "въ + Acc.",
        "",
        "",
        "om.",
        "om.",
        "",
        "",
        "",
        "εἰς MPePgPkR πρὸς PhPi",
        "εἰς MPePgPkR / πρός PhPi",
        "πρός + Acc. PhPi",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "bold|italic",
    ]
    result = merge([row], gr_sem.var, sl_sem)
    assert result == [
        [""] * 4
        + ["35/162a10", "въ", "въ \ue205ер\ue205хѫ• съвы-", "въ", "въ + Acc."]
        + [""] * 2
        + ["om."] * 2
        + [""] * 3
        + ["εἰς MPePgPkR πρὸς PhPi", "εἰς MPePgPkR / πρός PhPi", "πρός + Acc. PhPi"]
        + [""] * 7
        + ["bold|italic"]
        + ["1"] * 4
    ]


def test_i_procii():
    rows = [
        [""] * 4
        + ["05/29d09", "\ue205", "\ue205 жьнѧ\ue205 • \ue205 про-", "\ue205 conj."]
        + [""] * 3
        + ["om."]
        + [""] * 15,
        [""] * 4
        + ["05/29d09"]
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
    result = merge(rows, gr_sem.var, sl_sem)
    assert result == [
        # ['',  '',  '',  '',  '05/29d09',  '\ue205',  '\ue205 жьнѧ\ue205 • \ue205 про-',  '\ue205 conj.',  '',  '',  '',  'om.',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '1',  '1',  '1',  '1'],
        [""] * 4
        + ["05/29d09", "\ue205", "\ue205 жьнѧ\ue205 • \ue205 про-", "\ue205 conj."]
        + [""] * 3
        + ["om."]
        + [""] * 15
        + ["1"] * 4,
        # ['τὰ ἑξῆς MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp',  'ὁ MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp',  '',  '',  '',  '',  '',  '',  '',  '',  'hl16:FFFCD5B4|hl19:FFB8CCE4',  '1',  '1',  '1',  '1'],
        [""] * 4
        + ["05/29d09"]
        + ["ₓ про\ue20dе\ue201•", "", "ₓ"]
        + [""] * 3
        + ["om. om."]
        + [""] * 4
        + [
            "τὰ ἑξῆς MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp",
            "ὁ MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp",
        ]
        + [""] * 8
        + ["hl16:FFFCD5B4|hl19:FFB8CCE4"]
        + ["1"] * 4,
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
        + ["hl16:FFFCD5B4"]
        + ["1"] * 4,
    ]
