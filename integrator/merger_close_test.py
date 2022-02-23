from typing import List

from config import FROM_LANG, TO_LANG
from semantics import MainLangSemantics, VarLangSemantics
from merger import _close, _grouped, _group_variants


def test_close():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )
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
        + ["hl04|hl00|hl10"],
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
        + ["hl05|hl00|hl11"],
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
        + ["hl05|hl00|hl11"],
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
        + ["hl05|hl00|hl11"],
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
        + [
            "hl05|hl11",
        ],
        [""] * 4
        + [
            "1/5a10",
            "вѣдѣн\ue205ꙗ",
            "ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ",
            "вѣдѣн\ue205\ue201",
        ]
        + [""] * 18
        + [
            "hl05|hl11",
        ],
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
        + ["hl05|hl11"],
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
        + ["hl05|hl11"],
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
        + ["hl05|hl00|hl11"],
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
        + ["hl05|hl00|hl11"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        ["все \ue201л\ue205ко WH", "вьсь & \ue201л\ue205къ"]
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
        + ["hl05|hl00|hl11"],
        ["все \ue201л\ue205ко WH", "вьсь & \ue201л\ue205къ"]
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
        + ["hl05|hl00|hl11"],
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
        + ["hl05"],
        [""] * 4 + ["1/5a16"] + [""] * 6 + ["τὸ", "ὁ"] + [""] * 13 + ["hl05"],
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
        + ["hl05"],
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
        + ["hl05"],
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
        + ["hl05|hl00|hl11"],
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
        + ["hl05|hl00|hl11"],
    ]
    res = _close(group, sl_sem, gr_sem)
    expected = [
        ["все \ue201л\ue205ко WH", "вьсь \ue201л\ue205къ"]
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
        + ["hl05|hl00|hl11"],
        [
            "все \ue201л\ue205ко WH",
            "вьсь \ue201л\ue205къ",
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
        + ["hl05|hl00|hl11"],
    ]
    assert res == expected

    g1 = (
        [""] * 4
        + ["1/W168a13"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["ταῖς", "ὁ"]
        + [""] * 13
        + ["hl11"]
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
        + ["hl11"]
    )
    group = [g1, g2]

    res = _close(group, gr_sem, sl_sem)
    e1 = (
        [""] * 4
        + ["01/W168a13", "ₓ вышьн\ue205\ue205мь", "", "вꙑшьнь"]
        + [""] * 3
        + ["ταῖς ἄνω", "ὁ", "ὁ ἄνω"]
        + [""] * 12
        + ["hl11"]
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
        + ["hl11"]
    )
    expected = [e1, e2]
    assert res == expected


def test_tyam_li():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )

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
        + ["hl11"],
        [""] * 4 + ["1/6a11"] + [""] * 7 + ["ἀν"] + [""] * 13 + ["hl11"],
    ]
    res = _close(group, sl_sem, gr_sem)
    expected = [
        ["\ue205л\ue205 WH", "\ue205л\ue205"]
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
        + ["hl11"],
        ["\ue205л\ue205 WH", "\ue205л\ue205"]
        + [""] * 2
        + ["01/006a11", "л\ue205 "]
        + [""] * 5
        + ["κἂν", "καί & ἀν", "κἄν"]
        + [""] * 12
        + ["hl11"],
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
        + ["hl11"],
        [""] * 4 + ["1/6a11"] + [""] * 7 + ["ἀν"] + [""] * 13 + ["hl11"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        ["\ue205л\ue205 WH", "\ue205л\ue205"]
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
        + ["hl11"],
        ["\ue205л\ue205 WH", "\ue205л\ue205"]
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
        + ["hl11"],
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
        + ["hl05"],
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
        + ["hl05"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        ["\ue205л\ue205 WH", "\ue205л\ue205"]
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
        + ["hl05"],
        ["\ue205л\ue205 WH", "\ue205л\ue205"]
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
        + ["hl05"],
    ]
    assert res == expected


def test_biti():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )

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
            "hl05",
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
        + ["hl05|hl09"]
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
        + ["hl05"]
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
            "hl05|hl09",
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
        + ["hl05"]
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
            "hl05|hl09",
        ]
    )
    expected = [e1, e2]
    assert res == expected


def test_vetuhu():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )

    r1 = (
        [""] * 4
        + ["1/W168c20"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τῆς", "ὁ"]
        + [""] * 13
        + ["hl11"]
    )
    r2 = (
        [""] * 4
        + ["1/W168c20", "ветьхоую", "пр\ue205\ue201хомь• ꙁа ветьхоую", "ветъхъ"]
        + [""] * 3
        + ["πάλαι", "πάλαι", "ὁ πάλαι"]
        + [""] * 2
        + ["παλαιᾶς C"]
        + [""] * 9
        + ["hl11"]
    )
    group = [r1, r2]

    expected = [
        [""] * 4
        + ["01/W168c20", "ₓ ветьхоую", "", "ветъхъ"]
        + [""] * 3
        + ["τῆς πάλαι", "ὁ", "ὁ πάλαι"]
        + [""] * 2
        + [" παλαιᾶς C"]
        + [""] * 9
        + ["hl11"],
        [""] * 4
        + ["01/W168c20", "ₓ ветьхоую", "пр\ue205\ue201хомь• ꙁа ветьхоую", "ветъхъ"]
        + [""] * 3
        + ["τῆς πάλαι", "πάλαι", "ὁ πάλαι"]
        + [""] * 2
        + [" παλαιᾶς C"]
        + [""] * 9
        + ["hl11"],
    ]
    res = _close(group, gr_sem, sl_sem)
    assert res == expected


def test_vidit():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )

    r1 = (
        ["вѣдѣл\ue205 WG оувѣдѣл\ue205 H", "ѹвѣдѣт\ue205 H"]
        + [""] * 2
        + ["12/67c10", "в\ue205дѣл\ue205", "в\ue205дѣл\ue205 бꙑхо-", "в\ue205дѣт\ue205"]
        + [""] * 3
        + ["ἔγνωμεν", "γιγνώσκω"]
        + [""] * 13
        + ["hl05"]
    )
    r2 = (
        [""] * 4
        + ["12/67c10", "бꙑхомъ•", "в\ue205дѣл\ue205 бꙑхо-", "бꙑт\ue205"]
        + ["", "gramm.", ""] * 2
        + [""] * 12
        + ["hl05|hl09"]
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
        + ["hl05"]
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
        + ["hl05|hl09"]
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
            "в\ue205дѣт\ue205",
        ]
        + [""] * 3
        + ["ἔγνωμεν", "γιγνώσκω"]
        + [""] * 13
        + ["hl05"]
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
        + ["hl05|hl09"]
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
        + ["hl05"]
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
        + ["hl05|hl09"]
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
        + ["ἔγνωμεν", "γιγνώσκω"]
        + [""] * 13
        + ["hl05"]
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
        + ["hl05|hl09"]
    )

    assert res == [e1, e2]
