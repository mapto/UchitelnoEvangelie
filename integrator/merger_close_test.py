from setup import sl_sem, gr_sem
from merger import _close


def test_close():
    group = [
        ["все WH", "вьсь"]
        + [""] * 2
        + ["1/7c12", "въ", "въ сел\ue205ко", "въ", "въ + Acc."]
        + [""] * 2
        + [
            "εἰς",
            "εἰς",
        ]
        + [""] * 13
        + ["hl04:AAAAAAAA|hl00:AAAAAAAA|hl10:AAAAAAAA"],
        ["\ue201л\ue205ко WH", "\ue201л\ue205къ"]
        + [""] * 2
        + [
            "1/7c12",
            "сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
        ]
        + [""] * 3
        + [
            "τοῦτο",
            "οὗτος",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        ["все WH \ue201л\ue205ко WH", "вьсь & \ue201л\ue205къ"]
        + [""] * 2
        + [
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "въ & сел\ue205къ",
            "въ + Acc.",
        ]
        + [""] * 2
        + [
            "εἰς τοῦτο",
            "εἰς",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
        ["все WH \ue201л\ue205ко WH", "вьсь & \ue201л\ue205къ"]
        + [""] * 2
        + [
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "въ & сел\ue205къ",
            "въ + Acc.",
        ]
        + [""] * 2
        + [
            "εἰς τοῦτο",
            "οὗτος",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
    ]

    group = [
        [""] * 4
        + ["1/5a10", "беꙁ", "ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ", "беꙁ ", "беꙁ вѣдѣн\ue205ꙗ"]
        + [""] * 2
        + [
            "ἀπείρως",
            "ἀπείρως",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
        [""] * 4
        + [
            "1/5a10",
            "вѣдѣн\ue205ꙗ",
            "ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ",
            "вѣдѣн\ue205\ue201",
        ]
        + [""] * 18
        + ["hl05:AAAAAAAA"],
    ]
    res = _close(group, sl_sem, gr_sem)
    expected = [
        [""] * 4
        + [
            "01/005a10",
            "беꙁ вѣдѣн\ue205ꙗ",
            "ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ",
            "беꙁ ",
            "беꙁ вѣдѣн\ue205ꙗ",
        ]
        + [""] * 2
        + [
            "ἀπείρως",
            "ἀπείρως",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
        [""] * 4
        + [
            "01/005a10",
            "беꙁ вѣдѣн\ue205ꙗ",
            "ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ",
            "вѣдѣн\ue205\ue201",
            "беꙁ вѣдѣн\ue205ꙗ",
        ]
        + [""] * 2
        + [
            "ἀπείρως",
            "ἀπείρως",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
    ]
    assert res == expected

    group = [
        ["все WH", "вьсь"]
        + [""] * 2
        + ["1/7c12", "въ", "въ сел\ue205ко", "въ", "въ + Acc."]
        + [""] * 2
        + [
            "εἰς",
            "εἰς",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
        ["\ue201л\ue205ко WH", "\ue201л\ue205къ"]
        + [""] * 2
        + [
            "1/7c12",
            "сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
        ]
        + [""] * 3
        + [
            "τοῦτο",
            "οὗτος",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        ["все \ue201л\ue205ко WH", "вьсь & \ue201л\ue205къ WH"]
        + [""] * 2
        + [
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "въ & сел\ue205къ",
            "въ + Acc.",
        ]
        + [""] * 2
        + [
            "εἰς τοῦτο",
            "εἰς",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
        ["все \ue201л\ue205ко WH", "вьсь & \ue201л\ue205къ WH"]
        + [""] * 2
        + [
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "въ & сел\ue205къ",
            "въ + Acc.",
        ]
        + [""] * 2
        + [
            "εἰς τοῦτο",
            "οὗτος",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
    ]
    assert res == expected

    group = [
        [""] * 4
        + [
            "1/5a16",
            "ꙁан\ue201",
            "еще же \ue205 ꙁан\ue201 въꙁвѣст\ue205лъ",
            "ꙁан\ue201",
        ]
        + [""] * 3
        + [
            "διὰ",
            "διά ",
            "διά + Acc.",
            "διὰ τό",
        ]
        + [""] * 11
        + ["hl05:AAAAAAAA"],
        [""] * 4 + ["1/5a16"] + [""] * 6 + ["τὸ", "ὁ"] + [""] * 13 + ["hl05:AAAAAAAA"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        [""] * 4
        + [
            "01/005a16",
            "ꙁан\ue201",
            "еще же \ue205 ꙁан\ue201 въꙁвѣст\ue205лъ",
            "ꙁан\ue201",
        ]
        + [""] * 3
        + [
            "διὰ τὸ",
            "διά ",
            "διά + Acc.",
            "διὰ τό",
        ]
        + [""] * 11
        + ["hl05:AAAAAAAA"],
        [""] * 4
        + [
            "01/005a16",
            "ꙁан\ue201",
            "",
            "ꙁан\ue201",
        ]
        + [""] * 3
        + [
            "διὰ τὸ",
            "ὁ",
            "διά + Acc.",
            "διὰ τό",
        ]
        + [""] * 11
        + ["hl05:AAAAAAAA"],
    ]
    assert res == expected

    group = [
        ["все WH", "вьсь"]
        + [""] * 2
        + ["1/7c12", "въ", "въ сел\ue205ко", "въ", "въ + Acc."]
        + [""] * 2
        + [
            "εἰς",
            "εἰς",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
        ["\ue201л\ue205ко WH", "\ue201л\ue205къ"]
        + [""] * 2
        + [
            "1/7c12",
            "сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
        ]
        + [""] * 3
        + [
            "τοῦτο",
            "οὗτος",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
    ]
    res = _close(group, sl_sem, gr_sem)
    expected = [
        ["все \ue201л\ue205ко WH", "вьсь \ue201л\ue205къ WH"]
        + [""] * 2
        + [
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "въ",
            "въ + Acc.",
        ]
        + [""] * 2
        + [
            "εἰς τοῦτο",
            "εἰς & οὗτος",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
        [
            "все \ue201л\ue205ко WH",
            "вьсь \ue201л\ue205къ WH",
        ]
        + [""] * 2
        + [
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
            "въ + Acc.",
        ]
        + [""] * 2
        + [
            "εἰς τοῦτο",
            "εἰς & οὗτος",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"],
    ]
    assert res == expected

    g1 = (
        [""] * 4
        + ["1/W168a13"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["ταῖς", "ὁ"]
        + [""] * 13
        + ["hl11:AAAAAAAA"]
    )
    g2 = (
        [""] * 4
        + [
            "1/W168a13",
            "вышьн\ue205\ue205мь",
            "вышьн\ue205\ue205мь с\ue205ламь•",
            "вꙑшьнь",
        ]
        + [""] * 3
        + ["ἄνω", "ἄνω", "ὁ ἄνω"]
        + [""] * 12
        + ["hl11:AAAAAAAA"]
    )
    group = [g1, g2]

    res = _close(group, gr_sem, sl_sem)
    e1 = (
        [""] * 4
        + ["01/W168a13", "ₓ вышьн\ue205\ue205мь", "", "вꙑшьнь"]
        + [""] * 3
        + ["ταῖς ἄνω", "ὁ", "ὁ ἄνω"]
        + [""] * 12
        + ["hl11:AAAAAAAA"]
    )
    e2 = (
        [""] * 4
        + [
            "01/W168a13",
            "ₓ вышьн\ue205\ue205мь",
            "вышьн\ue205\ue205мь с\ue205ламь•",
            "вꙑшьнь",
        ]
        + [""] * 3
        + ["ταῖς ἄνω", "ἄνω", "ὁ ἄνω"]
        + [""] * 12
        + ["hl11:AAAAAAAA"]
    )
    expected = [e1, e2]
    assert res == expected


def test_tyam_li():
    group = [
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "",
            "1/6a11",
            "л\ue205 ",
            "\ue201сть л\ue205 раꙁѹмьно",
            "л\ue205 ",
        ]
        + [""] * 3
        + [
            "κἂν",
            "καί",
            "κἄν",
        ]
        + [""] * 12
        + ["hl11:AAAAAAAA"],
        [""] * 4 + ["1/6a11"] + [""] * 7 + ["ἀν"] + [""] * 13 + ["hl11:AAAAAAAA"],
    ]
    res = _close(group, sl_sem, gr_sem)
    expected = [
        ["\ue205л\ue205 WH", "\ue205л\ue205 WH"]
        + [""] * 2
        + [
            "01/006a11",
            "л\ue205 ",
            "\ue201сть л\ue205 раꙁѹмьно",
            "л\ue205 ",
        ]
        + [""] * 3
        + ["κἂν", "καί & ἀν", "κἄν"]
        + [""] * 12
        + ["hl11:AAAAAAAA"],
        ["\ue205л\ue205 WH", "\ue205л\ue205 WH"]
        + [""] * 2
        + ["01/006a11", "л\ue205 "]
        + [""] * 5
        + ["κἂν", "καί & ἀν", "κἄν"]
        + [""] * 12
        + ["hl11:AAAAAAAA"],
    ]
    assert res == expected

    group = [
        ["\ue205л\ue205 WH", "\ue205л\ue205"]
        + [""] * 2
        + [
            "1/6a11",
            "л\ue205 ",
            "\ue201сть л\ue205 раꙁѹмьно",
            "л\ue205 ",
        ]
        + [""] * 3
        + ["κἂν", "καί", "κἄν"]
        + [""] * 12
        + ["hl11:AAAAAAAA"],
        [""] * 4 + ["1/6a11"] + [""] * 7 + ["ἀν"] + [""] * 13 + ["hl11:AAAAAAAA"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        ["\ue205л\ue205 WH", "\ue205л\ue205 WH"]
        + [""] * 2
        + [
            "01/006a11",
            "л\ue205 ",
            "\ue201сть л\ue205 раꙁѹмьно",
            "л\ue205 ",
        ]
        + [""] * 3
        + [
            "κἂν",
            "καί",
            "κἄν",
        ]
        + [""] * 12
        + ["hl11:AAAAAAAA"],
        ["\ue205л\ue205 WH", "\ue205л\ue205 WH"]
        + [""] * 2
        + [
            "01/006a11",
            "л\ue205 ",
            "",
            "л\ue205 ",
        ]
        + [""] * 3
        + [
            "κἂν",
            "ἀν",
            "κἄν",
        ]
        + [""] * 12
        + ["hl11:AAAAAAAA"],
    ]
    assert res == expected

    group = [
        [""] * 4
        + ["1/6a10", "тѣмь", "тѣмь л\ue205 в\ue205д\ue205мо", "тѣмь", "тѣмь л\ue205"]
        + [""] * 2
        + [
            "κἂν",
            "καί",
            "κἄν",
        ]
        + [""] * 12
        + ["hl05:AAAAAAAA"],
        ["\ue205л\ue205 WH", "\ue205л\ue205"]
        + [""] * 2
        + [
            "1/6a10",
            "л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "л\ue205",
        ]
        + [""] * 4
        + ["ἀν"]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        ["\ue205л\ue205 WH", "\ue205л\ue205 WH"]
        + [""] * 2
        + [
            "01/006a10",
            "тѣмь л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь & л\ue205",
            "тѣмь л\ue205",
        ]
        + [""] * 2
        + [
            "κἂν",
            "καί",
            "κἄν",
        ]
        + [""] * 12
        + ["hl05:AAAAAAAA"],
        ["\ue205л\ue205 WH", "\ue205л\ue205 WH"]
        + [""] * 2
        + [
            "01/006a10",
            "тѣмь л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь & л\ue205",
            "тѣмь л\ue205",
        ]
        + [""] * 2
        + [
            "κἂν",
            "ἀν",
            "κἄν",
        ]
        + [""] * 12
        + ["hl05:AAAAAAAA"],
    ]
    assert res == expected


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
        + ["hl05:AAAAAAAA"],
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
        + ["hl05:AAAAAAAA"],
    ]

    res = _close([rows[0].copy(), rows[1].copy()], gr_sem, sl_sem)
    assert res == [
        [
            "тѣмь \ue205л\ue205 WH",
            "\ue205л\ue205 WH",
            "тѣмь \ue205л\ue205 WH",
            "",
            "01/006a10",
            "тѣмь л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь & л\ue205",
            "тѣмь л\ue205",
            "",
            "",
            "κἂν",
            "κἄν",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
        [
            "тѣмь \ue205л\ue205 WH",
            "\ue205л\ue205 WH",
            "тѣмь \ue205л\ue205 WH",
            "",
            "01/006a10",
            "тѣмь л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь & л\ue205",
            "тѣмь л\ue205",
            "",
            "",
            "κἂν",
        ]
        + [""] * 14
        + ["hl05:AAAAAAAA"],
    ]

    res = _close([rows[0].copy(), rows[1].copy()], sl_sem.var, gr_sem)
    assert res == [
        [
            "тѣмь \ue205л\ue205 WH",
            "",
            "тѣмь \ue205л\ue205 WH",
            "",
            "01/006a10",
            "тѣмь л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь л\ue205",
            "тѣмь л\ue205",
            "",
            "",
            "κἂν",
            "κἄν",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
        [
            "тѣмь \ue205л\ue205 WH",
            "\ue205л\ue205",
            "тѣмь \ue205л\ue205 WH",
            "",
            "01/006a10",
            "тѣмь л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь л\ue205",
            "тѣмь л\ue205",
            "",
            "",
            "κἂν",
            "κἄν",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
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
        + [
            "hl05:AAAAAAAA|hl09:AAAAAAAA",
        ]
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
        + [
            "hl05:AAAAAAAA|hl09:AAAAAAAA",
        ]
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


def test_vidit():
    r1 = (
        ["вѣдѣл\ue205 WG оувѣдѣл\ue205 H", "ѹвѣдѣт\ue205 H"]
        + [""] * 2
        + ["12/67c10", "в\ue205дѣл\ue205", "в\ue205дѣл\ue205 бꙑхо-", "в\ue205дѣт\ue205"]
        + [""] * 3
        + ["ἔγνωμεν", "γιγνώσκω"]
        + [""] * 13
        + ["hl05:AAAAAAAA"]
    )
    r2 = (
        [""] * 4
        + ["12/67c10", "бꙑхомъ•", "в\ue205дѣл\ue205 бꙑхо-", "бꙑт\ue205"]
        + ["", "gramm.", ""] * 2
        + [""] * 12
        + ["hl03:AAAAAAAA|hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )

    group = [r1.copy(), r2.copy()]
    res = _close(group, sl_sem, gr_sem)
    e1 = (
        ["вѣдѣл\ue205 WG оувѣдѣл\ue205 H", "ѹвѣдѣт\ue205 H"]
        + [""] * 2
        + [
            "12/067c10",
            "в\ue205дѣл\ue205 бꙑхомъ•",
            "в\ue205дѣл\ue205 бꙑхо-",
            "в\ue205дѣт\ue205",
        ]
        + [""] * 3
        + ["ἔγνωμεν", "γιγνώσκω"]
        + [""] * 13
        + ["hl05:AAAAAAAA"]
    )
    e2 = (
        ["вѣдѣл\ue205 WG оувѣдѣл\ue205 H"]
        + [""] * 3
        + [
            "12/67c10",
            "в\ue205дѣл\ue205 бꙑхомъ•",
            "в\ue205дѣл\ue205 бꙑхо-",
            "бꙑт\ue205",
            "",
            "gramm.",
            "",
            "ἔγνωμεν",
            "gramm.",
        ]
        + [""] * 13
        + ["hl03:AAAAAAAA|hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    assert res == [e1, e2]

    group = [r1.copy(), r2.copy()]
    res = _close(group, sl_sem.var, gr_sem)
    e1 = (
        ["вѣдѣл\ue205 WG оувѣдѣл\ue205 H", "ѹвѣдѣт\ue205 H"]
        + [""] * 2
        + [
            "12/067c10",
            "в\ue205дѣл\ue205 бꙑхомъ•",
            "в\ue205дѣл\ue205 бꙑхо-",
            "в\ue205дѣт\ue205 бꙑт\ue205",
        ]
        + [""] * 3
        + ["ἔγνωμεν", "γιγνώσκω"]
        + [""] * 13
        + ["hl05:AAAAAAAA"]
    )
    e2 = (
        ["вѣдѣл\ue205 WG оувѣдѣл\ue205 H"]
        + [""] * 3
        + [
            "12/67c10",
            "в\ue205дѣл\ue205 бꙑхомъ•",
            "в\ue205дѣл\ue205 бꙑхо-",
            "бꙑт\ue205",
            "",
            "gramm.",
            "",
            "ἔγνωμεν",
            "gramm.",
        ]
        + [""] * 13
        + ["hl03:AAAAAAAA|hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    assert res == [e1, e2]

    group = [r1.copy(), r2.copy()]
    res = _close(group, gr_sem, sl_sem)
    e1 = (
        ["вѣдѣл\ue205 WG оувѣдѣл\ue205 H", "ѹвѣдѣт\ue205 H"]
        + [""] * 2
        + [
            "12/067c10",
            "в\ue205дѣл\ue205 бꙑхомъ•",
            "в\ue205дѣл\ue205 бꙑхо-",
            "в\ue205дѣт\ue205",
        ]
        + [""] * 3
        + ["ἔγνωμεν", "γιγνώσκω"]
        + [""] * 13
        + ["hl05:AAAAAAAA"]
    )
    e2 = (
        ["вѣдѣл\ue205 WG оувѣдѣл\ue205 H"]
        + [""] * 3
        + [
            "12/67c10",
            "в\ue205дѣл\ue205 бꙑхомъ•",
            "в\ue205дѣл\ue205 бꙑхо-",
            "бꙑт\ue205",
        ]
        + ["", "gramm.", "", "ἔγνωμεν", "gramm."]
        + [""] * 13
        + ["hl03:AAAAAAAA|hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    assert res == [e1, e2]

    group = [r1.copy(), r2.copy()]
    res = _close(group, gr_sem.var, sl_sem)
    e1 = (
        ["вѣдѣл\ue205 WG оувѣдѣл\ue205 H", "ѹвѣдѣт\ue205 H"]
        + [""] * 2
        + [
            "12/067c10",
            "в\ue205дѣл\ue205 бꙑхомъ•",
            "в\ue205дѣл\ue205 бꙑхо-",
            "в\ue205дѣт\ue205",
        ]
        + [""] * 3
        + ["ἔγνωμεν", "γιγνώσκω gramm."]
        + [""] * 13
        + ["hl05:AAAAAAAA"]
    )
    e2 = (
        ["вѣдѣл\ue205 WG оувѣдѣл\ue205 H"]
        + [""] * 3
        + [
            "12/67c10",
            "в\ue205дѣл\ue205 бꙑхомъ•",
            "в\ue205дѣл\ue205 бꙑхо-",
            "бꙑт\ue205",
            "",
            "gramm.",
            "",
            "ἔγνωμεν",
            "gramm.",
        ]
        + [""] * 13
        + ["hl03:AAAAAAAA|hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )

    assert res == [e1, e2]


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
        + ["τῶν ἐπὶ γῆς Ch", "ὁ"]
        + [""] * 8
        + ["hl16:AAAAAAAA|hl19:AAAAAAAA"],
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί", "ἐπί + Gen.", "ὁ ἐπὶ γῆς Ch"]
        + [""] * 6
        + ["hl16:AAAAAAAA|hl18:AAAAAAAA"],
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205", "", "ꙁемьнъ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "γῆ", "", "ὁ ἐπὶ γῆς Ch"]
        + [""] * 6
        + ["hl16:AAAAAAAA"],
    ]

    # res = _close(rows.copy(), sl_sem, gr_sem)
    # TODO
    """
    assert res == [
        [""] * 4
        + ["19/94d08", "ₓ ꙁемьнꙑ\ue205", "", "ₓ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "ὁ"]
        + [""] * 8
        + ["hl16|hl19"],
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ", "ἐπί + Gen.", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16|hl18"],
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205"]
        + [""] * 10
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ", "", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16"],
    ]
    """


def test_prichatnik_biti():
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
        ]
        + [""] * 2
        + ["ποιῆσαι", "ποιέω", "ποιέω κοινωνόν"]
        + [""] * 12
        + ["hl05:AAAAAAAA|hl11:AAAAAAAA"],
        ["боудемь W", "бꙑт\ue205 GH"]
        + [""] * 2
        + ["05/28d01", "боудоуть", "боудоуть• \ue201же", "бꙑт\ue205"]
        + [""] * 3
        + ["κοινωνοὺς", "κοινωνός"]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl11:AAAAAAAA"],
    ]

    res = _close([rows[0].copy(), rows[1].copy()], sl_sem.var, gr_sem)
    assert res == [
        [
            "боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H"
            "",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + ["ποιῆσαι κοινωνοὺς", "ποιέω & κοινωνός", "ποιέω κοινωνόν"]
        + [""] * 12
        + ["hl05:AAAAAAAA|hl11:AAAAAAAA"],
        [
            "боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H",
            "бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "боудоуть• \ue201же",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + ["ποιῆσαι κοινωνοὺς", "ποιέω & κοινωνός", "ποιέω κοινωνόν"]
        + [""] * 12
        + ["hl05:AAAAAAAA|hl11:AAAAAAAA"],
    ]

    res = _close([rows[0].copy(), rows[1].copy()], sl_sem, gr_sem)
    assert res == [
        [
            "боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
        ]
        + [""] * 2
        + [
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05:AAAAAAAA|hl11:AAAAAAAA"],
        [
            "боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "боудоуть• \ue201же",
            "бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
            "",
            "",
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05:AAAAAAAA|hl11:AAAAAAAA"],
    ]

    res = _close([rows[0].copy(), rows[1].copy()], gr_sem, sl_sem)
    assert res == [
        [
            "боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H",
            "пр\ue205\ue20dѧстьн\ue205къ & бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ & бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
            "",
            "",
            "ποιῆσαι κοινωνοὺς",
            "ποιέω",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05:AAAAAAAA|hl11:AAAAAAAA"],
        [
            "боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 б• G пр\ue205\ue20dестн\ue205ц\ue205 б• H",
            "пр\ue205\ue20dѧстьн\ue205къ & бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "боудоуть• \ue201же",
            "пр\ue205\ue20dьтьн\ue205къ & бꙑт\ue205",
            "пр\ue205\ue20dьтьн\ue205къ быт\ue205",
            "",
            "",
            "ποιῆσαι κοινωνοὺς",
            "κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05:AAAAAAAA|hl11:AAAAAAAA"],
    ]


def test_hoditi_spiti():
    rows = [
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/72d18",
            "ход\ue205мъ",
            "себе• по поут\ue205 хо-",
            "ход\ue205т\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
            "",
            "",
            "προβαίνοντες",
            "προβαίνω",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
        [""] * 4
        + ["14/72d19", "спѣюще•", "д\ue205мъ спѣюще•", "спѣт\ue205"]
        + [""] * 18
        + ["hl05:AAAAAAAA"],
    ]

    res = _close([rows[0].copy(), rows[1].copy()], sl_sem, gr_sem)
    assert res == [
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "себе• по поут\ue205 хо-",
            "ход\ue205т\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
        ]
        + [""] * 2
        + ["προβαίνοντες", "προβαίνω"]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "д\ue205мъ спѣюще•",
            "спѣт\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
        ]
        + [""] * 2
        + ["προβαίνοντες", "προβαίνω"]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
    ]

    res = _close([rows[0].copy(), rows[1].copy()], sl_sem.var, gr_sem)
    assert res == [
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "себе• по поут\ue205 хо-",
            "ход\ue205т\ue205 спѣт\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
            "",
            "",
            "προβαίνοντες",
            "προβαίνω",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "д\ue205мъ спѣюще•",
            "ход\ue205т\ue205 спѣт\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
            "",
            "",
            "προβαίνοντες",
            "προβαίνω",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
    ]

    res = _close([rows[0].copy(), rows[1].copy()], gr_sem, sl_sem)
    assert res == [
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "себе• по поут\ue205 хо-",
            "ход\ue205т\ue205 & спѣт\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
            "",
            "",
            "προβαίνοντες",
            "προβαίνω",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA"],
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "ход\ue205мъ спѣюще•",
            "д\ue205мъ спѣюще•",
            "ход\ue205т\ue205 & спѣт\ue205",
            "≈ ход\ue205т\ue205 спѣѭще",
            "",
            "",
            "προβαίνοντες",
        ]
        + [""] * 14
        + ["hl05:AAAAAAAA"],
    ]
