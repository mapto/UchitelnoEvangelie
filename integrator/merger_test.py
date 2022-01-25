from typing import List

from model import Source
from semantics import MainLangSemantics, VarLangSemantics
from merger import merge, _grouped, _group_variants


def test_grouped():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    row = (
        [
            "\ue201л\ue205ко WH",
            "\ue201л\ue205къ",
        ]
        + [""] * 2
        + [
            "1/7c12",
            "сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
        ]
        + [""] * 3
        + ["τοῦτο", "οὗτος"]
        + [""] * 13
        + ["hl05|hl00|hl11"]
    )
    assert _grouped(row, gr_sem)

    row = (
        [""] * 4
        + ["1/7d1", "насъ", "оу насъ", "мꙑ"]
        + [""] * 3
        + ["om.", "om."]
        + [""] * 3
        + ["ἡμῖν", "ἡμεῖς"]
        + [""] * 9
    )
    assert not _grouped(row, sl_sem)
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "",
            "1/7b19",
            "вѣроують",
            "вьс\ue205 вѣроують",
            "вѣроват\ue205",
        ]
        + [""] * 3
        + [
            "πιστεύσωσι",
            "πιστεύω",
        ]
        + [""] * 13
        + ["hl00"]
    )
    assert _grouped(row, sl_sem)
    row = ["\ue205моуть GH", "ѩт\ue205"] + [""] * 2 + ["1/7b19"] + [""] * 21 + ["hl00"]
    assert _grouped(row, sl_sem)


def test_group_variants():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    g1 = (
        [""] * 2
        + [
            "тѣмь \ue205л\ue205",
            "",
            "1/6a10",
            "тѣмь",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь",
            "тѣмь л\ue205",
        ]
        + [""] * 2
        + ["κἂν"] * 2
        + [""] * 13
        + ["hl04"]
    )
    g2 = (
        ["\ue205л\ue205 WH", "\ue205л\ue205"]
        + [""] * 2
        + ["1/6a10", "л\ue205", "тѣмь л\ue205 в\ue205д\ue205мо", "л\ue205"]
        + [""] * 18
        + ["hl04"]
    )
    group = [g1, g2]
    res = _group_variants(group, sl_sem)
    assert res == Source("WH")


def test_merge():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    r1 = (
        [""] * 4
        + ["1/5a5", "не", "не бѣ ꙗвленъ•", "не", "не бꙑт\ue205 ꙗвл\ue201нъ"]
        + [""] * 2
        + ["ἠγνοεῖτο", "ἀγνοέω"]
        + [""] * 13
        + ["hl05"]
    )
    r2 = (
        [""] * 4
        + ["1/5a5", "бѣ", "", "бꙑт\ue205", "", "gramm."]
        + [""] * 2
        + ["pass."]
        + [""] * 13
        + ["hl05|hl09"]
    )
    r3 = [""] * 4 + ["1/5a5", "ꙗвленъ•", "", "ꙗв\ue205т\ue205"] + [""] * 18 + ["hl05"]

    rows = [r1, r2, r3]
    result = merge(rows, sl_sem, gr_sem)
    expected = [
        [""] * 4
        + [
            "01/005a05",
            "не бѣ ꙗвленъ•",
            "не бѣ ꙗвленъ•",
            "не",
            "не бꙑт\ue205 ꙗвл\ue201нъ",
        ]
        + [""] * 2
        + ["ἠγνοεῖτο", "ἀγνοέω"]
        + [""] * 13
        + ["hl05"],
        [""] * 4
        + [
            "1/5a5",
            "не бѣ ꙗвленъ•",
            "",
            "бꙑт\ue205",
            "",
            "gramm.",
            "",
            "ἠγνοεῖτο",
            "pass.",
        ]
        + [""] * 13
        + ["hl05|hl09"],
        [""] * 4
        + [
            "01/005a05",
            "не бѣ ꙗвленъ•",
            "",
            "ꙗв\ue205т\ue205",
            "не бꙑт\ue205 ꙗвл\ue201нъ",
        ]
        + [""] * 2
        + ["ἠγνοεῖτο", "ἀγνοέω"]
        + [""] * 13
        + ["hl05"],
    ]
    assert result == expected

    result = merge(rows, gr_sem, sl_sem)
    expected = [
        [""] * 4
        + [
            "01/005a05",
            "не бѣ ꙗвленъ•",
            "не бѣ ꙗвленъ•",
            "не & ꙗв\ue205т\ue205",
            "не бꙑт\ue205 ꙗвл\ue201нъ",
        ]
        + [""] * 2
        + ["ἠγνοεῖτο", "ἀγνοέω"]
        + [""] * 13
        + ["hl05"],
        [""] * 4
        + [
            "1/5a5",
            "не бѣ ꙗвленъ•",
            "",
            "бꙑт\ue205",
            "",
            "gramm.",
            "",
            "ἠγνοεῖτο",
            "pass.",
        ]
        + [""] * 13
        + [
            "hl05|hl09",
        ],
        [""] * 4
        + [
            "01/005a05",
            "не бѣ ꙗвленъ•",
            "",
            "не & ꙗв\ue205т\ue205",
            "не бꙑт\ue205 ꙗвл\ue201нъ",
        ]
        + [""] * 2
        + ["ἠγνοεῖτο"]
        + [""] * 14
        + ["hl05"],
    ]
    assert result == expected


def test_merge_special():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    row = (
        [""] * 4
        + ["1/4b16", "на\ue20dатъ", "семоу на\ue20dатъ", "на\ue20dѧт\ue205", "≠"]
        + [""] * 2
        + ["ᾐνίξατο", "αἰνίσσομαι"]
        + [""] * 14
    )
    res = merge([row.copy()], sl_sem, gr_sem)
    assert res == [
        [""] * 4
        + [
            "1/4b16",
            "на\ue20dатъ",
            "семоу на\ue20dатъ",
            "на\ue20dѧт\ue205",
            "≠ на\ue20dѧт\ue205",
        ]
        + [""] * 2
        + ["ᾐνίξατο", "αἰνίσσομαι"]
        + [""] * 14
    ]
    res = merge([row.copy()], gr_sem, sl_sem)
    assert res == [
        [""] * 4
        + [
            "1/4b16",
            "на\ue20dатъ",
            "семоу на\ue20dатъ",
            "на\ue20dѧт\ue205",
            "≠ на\ue20dѧт\ue205",
        ]
        + [""] * 2
        + ["ᾐνίξατο", "αἰνίσσομαι"]
        + [""] * 14
    ]
