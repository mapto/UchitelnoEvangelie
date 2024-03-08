from const import IDX_COL
from setup import sl_sem, gr_sem
from merger import _close


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
        + ["ἠδυνήθημεν", "δύναμαι"]
        + [""] * 13
        + ["hl05:AAAAAAAA"]
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
        + ["pass."]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    group = [g1.copy(), g2.copy()]

    res = _close(group, sl_sem, gr_sem)
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
        + ["hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    expected = [e1, e2]
    assert res == expected

    group = [g1, g2]
    res = _close(group, gr_sem, sl_sem)
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
        + ["hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    expected = [e1, e2]
    assert res == expected


def test_vetuhu():
    r1 = (
        [""] * 4
        + ["1/W168c20"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τῆς", "ὁ"]
        + [""] * 13
        + ["hl11:AAAAAAAA"]
    )
    r2 = (
        [""] * 4
        + ["1/W168c20", "ветьхоую", "пр\ue205\ue201хомь• ꙁа ветьхоую", "ветъхъ"]
        + [""] * 3
        + ["πάλαι", "πάλαι", "ὁ πάλαι"]
        + [""] * 2
        + ["παλαιᾶς Cs"]
        + [""] * 9
        + ["hl11:AAAAAAAA"]
    )
    group = [r1, r2]

    expected = [
        [""] * 4
        + ["01/W168c20", "ₓ ветьхоую", "", "ветъхъ"]
        + [""] * 3
        + ["τῆς πάλαι", "ὁ", "ὁ πάλαι"]
        + [""] * 2
        + ["παλαιᾶς Cs"]
        + [""] * 9
        + ["hl11:AAAAAAAA"],
        [""] * 4
        + ["01/W168c20", "ₓ ветьхоую", "пр\ue205\ue201хомь• ꙁа ветьхоую", "ветъхъ"]
        + [""] * 3
        + ["τῆς πάλαι", "πάλαι", "ὁ πάλαι"]
        + [""] * 2
        + ["παλαιᾶς Cs"]
        + [""] * 9
        + ["hl11:AAAAAAAA"],
    ]
    res = _close(group, gr_sem, sl_sem)
    assert res == expected


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

    res = _close(rows.copy(), gr_sem.var, sl_sem)
    assert res == [
        [""] * 4
        + ["19/94d08", "ₓ ꙁемьнꙑ\ue205", "", "ₓ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "ὁ Ch"]
        + [""] * 8
        + ["hl16:AAAAAAAA|hl19:AAAAAAAA"],
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί Ch", "ἐπί + Gen.", "ὁ ἐπὶ γῆς Ch"]
        + [""] * 6
        + ["hl16:AAAAAAAA|hl18:AAAAAAAA"],
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205", "", "ꙁемьнъ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "γῆ Ch", "ὁ ἐπὶ γῆς Ch"]
        + [""] * 7
        + ["hl16:AAAAAAAA"],
    ]


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


def test_i_az():
    group = [
        [""] * 4
        + [
            "02/W169a26",
            "\ue205",
            "сла ме ѿц҃ь• \ue205 аꙁь пос\ue205лаю",
            "\ue205 conj.",
        ]
        + [""] * 3
        + ["κἀγὼ", "καί"]
        + [""] * 13
        + ["bold|italic"],
        [""] * 4
        + ["02/W169a26", "аꙁь", "сла ме ѿц҃ь• \ue205 аꙁь пос\ue205лаю", "аꙁъ"]
        + [""] * 3
        + ["=", "ἐγώ"]
        + [""] * 13
        + ["bold|italic"],
    ]
    res = _close(group, sl_sem, gr_sem)
    assert res == [
        [""] * 4
        + ["02/W169a26", "аꙁь", "сла ме ѿц҃ь• \ue205 аꙁь пос\ue205лаю", "аꙁъ"]
        + [""] * 3
        + ["κἀγὼ", "ἐγώ"]
        + [""] * 13
        + ["bold|italic"],
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
