from const import IDX_COL
from setup import sl_sem, gr_sem
from merger import merge, _close, _close_group

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


def test_i_az_sla():
    rows = [r.copy() for r in raw[:2]]
    result = merge(rows, sl_sem, gr_sem)

    assert result == [
        [""] * 4
        + ["19/94d08", "\ue205", "", "\ue205 conj."]
        + [""] * 3
        + ["κάγω", "καί"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["19/94d08", "аꙁ", "", "аꙁъ"]
        + [""] * 3
        + ["κάγω", "ἐγώ"]
        + [""] * 14
        + ["1"] * 4,
    ]


def test_miren_sla():
    rows = [r.copy() for r in raw[2:]]
    result = merge(rows, sl_sem, gr_sem)

    assert result == [
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


def test_same_and_hilited():
    rows = [r.copy() for r in raw]
    res = merge(rows, sl_sem, gr_sem)

    assert res == [
        [""] * 4
        + ["19/94d08", "\ue205", "", "\ue205 conj."]
        + [""] * 3
        + ["κάγω", "καί"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["19/94d08", "аꙁ", "", "аꙁъ"]
        + [""] * 3
        + ["κάγω", "ἐγώ"]
        + [""] * 14
        + ["1"] * 4,
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


def test_hilited_and_same():
    rows = [r.copy() for r in raw[2:] + raw[:2]]
    res = merge(rows, sl_sem, gr_sem)

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
        [""] * 4
        + ["19/94d08", "\ue205", "", "\ue205 conj."]
        + [""] * 3
        + ["κάγω", "καί"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["19/94d08", "аꙁ", "", "аꙁъ"]
        + [""] * 3
        + ["κάγω", "ἐγώ"]
        + [""] * 14
        + ["1"] * 4,
    ]


def test_close():
    group = [r.copy() + ["1"] * 4 for r in raw[2:]]
    for r in group:
        r[IDX_COL] = "02/W169a17"

    res = _close(group, sl_sem, gr_sem)
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


def test_close_group():
    group = [r.copy() + ["1"] * 4 for r in raw[2:]]
    for r in group:
        r[IDX_COL] = "02/W169a17"

    res = _close_group(group, sl_sem, gr_sem)
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


def test_merge_sloves_inverse():
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
    result = merge(rows, gr_sem, sl_sem)

    assert result == [
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "", "ₓ"]
        + [""] * 3
        + ["τῶν εἰρημένων", "ὁ"]
        + [""] * 13
        + ["hl11:FFFCD5B4|hl14:FFB8CCE4"]
        + ["1"] * 4,
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
        + [""] * 3
        + ["τῶν εἰρημένων", "λέγω", "τὸ εἰρημένον"]
        + [""] * 12
        + ["hl11:FFFCD5B4"]
        + ["1"] * 4,
    ]


def test_close_sloves_inverse():
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
    result = _close(rows, gr_sem, sl_sem)

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
        + ["hl00:FFF8CBAD|hl03:FFBDD7EE"],
        ["рекл\ue205 H"]
        + [""] * 3
        + ["25/123b05", "рѣша", "ко г\ue010лще рѣша• ꙗ-", "рещ\ue205"]
        + [""] * 3
        + ["φασὶν", "φημί"]
        + [""] * 13
        + ["hl00:FFF8CBAD"],
    ]

    res = merge(group, sl_sem, gr_sem)

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
            "",
        ]
        + [""] * 2
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


def test_sumeromadrost():
    group = [
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
        ["моудрост\ue205 H", "мѫдрость H"] + [""] * 24 + ["hl00:FFFCD5B4"],
    ]

    res = merge(group, sl_sem, gr_sem)

    assert res == [
        [
            "смѣроумоудрост\ue205 WG смѣрены\ue201 моудрост\ue205 H",
            "съмѣрѹмѫдрость WG / съмѣр\ue201нъ мѫдрость H",
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
            "съмѣрѹмѫдрость WG / съмѣр\ue201нъ мѫдрость H",
            "съмѣр\ue201наꙗ мѫдрость H",
            "",
            "25/125a03",
            "съмѣромоудрост\ue205",
        ]
        + [""] * 5
        + ["om."]
        + [""] * 4
        + ["ταπεινοφροσύνην Ch", "ταπεινοφροσύνη Ch"]
        + [""] * 8
        + [
            "hl00:FFFCD5B4",
        ]
        + ["1"] * 4,
    ]
