from typing import List
from const import STYLE_COL

from config import FROM_LANG, TO_LANG
from model import Source
from semantics import MainLangSemantics, VarLangSemantics
from merger import merge, _grouped, _group_variants


def test_grouped():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
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
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
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
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
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
        + ["hl05"]
        + ["1"] * 4,
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
        + ["hl05|hl09"]
        + ["1"] * 4,
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
        + ["hl05"]
        + ["1"] * 4,
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
        + ["hl05"]
        + ["1"] * 4,
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
        + ["hl05|hl09"]
        + ["1"] * 4,
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
        + ["hl05"]
        + ["1"] * 4,
    ]
    assert result == expected


def test_merge_special():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
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
        + ["1"] * 4
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
        + ["1"] * 4
    ]


def test_merge_repeated_om():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )

    rows = [
        ["om. WH", "om."]
        + [""] * 2
        + ["1/7c6", "аще", "аще \ue205 не", "аще"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 14,
        [""] * 4
        + ["1/7c6", "не", "аще \ue205 не", "не"]
        + [""] * 3
        + ["οὐ"] * 2
        + [""] * 14,
        ["om. WH", "om."]
        + [""] * 2
        + ["1/7c6", "\ue205", "аще \ue205 не", "\ue205 conj."]
        + [""] * 3
        + ["om."] * 2
        + [""] * 14,
    ]
    res = merge(rows, sl_sem, gr_sem)
    assert res == [
        ["om. WH", "om."]
        + [""] * 2
        + ["1/7c6", "аще", "аще \ue205 не", "аще"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["1/7c6", "не", "аще \ue205 не", "не"]
        + [""] * 3
        + ["οὐ", "οὐ"]
        + [""] * 14
        + ["1"] * 4,
        ["om. WH", "om."]
        + [""] * 2
        + ["1/7c6", "\ue205", "аще \ue205 не", "\ue205 conj."]
        + [""] * 3
        + ["om."] * 2
        + [""] * 14
        + ["1", "1", "1", "1"],
    ]

    res = merge(rows, sl_sem.var, gr_sem)
    assert res == [
        ["om. WH", "om."]
        + [""] * 2
        + [
            "1/7c6",
            "аще",
            "аще \ue205 не",
            "аще",
        ]
        + [""] * 3
        + ["om."] * 2
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["1/7c6", "не", "аще \ue205 не", "не"]
        + [""] * 3
        + ["οὐ"] * 2
        + [""] * 14
        + ["1"] * 4,
        ["om. WH", "om."]
        + [""] * 2
        + ["1/7c6", "\ue205", "аще \ue205 не", "\ue205 conj."]
        + [""] * 3
        + ["om.", "om."]
        + [""] * 14
        + ["1", "1", "1", "1"],
    ]


def test_merge_repeated_kai():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )

    rows = [
        [""] * 4
        + ["1/5d9", "него•", "се \ue205 ѿ него• \ue205 не", "\ue205 pron."]
        + [""] * 3
        + ["αὐτοῦ", "αὐτός"]
        + [""] * 14,
        [""] * 4
        + ["1/5d9", "се", "се \ue205 ѿ него• \ue205 не", "се"]
        + [""] * 3
        + ["ἰδοὺ", "ἰδού"]
        + [""] * 14,
        [""] * 4
        + ["1/5d9(1)", "\ue205", "се \ue205 ѿ него• \ue205 не", "\ue205 conj."]
        + [""] * 3
        + ["καὶ", "καί"]
        + [""] * 14,
        [""] * 4
        + ["1/5d9", "ѿ", "се \ue205 ѿ него• \ue205 не", "отъ"]
        + [""] * 3
        + ["ἐξ", "ἐκ"]
        + [""] * 14,
        [""] * 4
        + ["1/5d9", "него•", "се \ue205 ѿ него• \ue205 не", "\ue205 pron."]
        + [""] * 3
        + ["αὐτοῦ", "αὐτός"]
        + [""] * 14,
        [""] * 4
        + ["1/5d9(2)", "\ue205", "се \ue205 ѿ него• \ue205 не", "\ue205 conj."]
        + [""] * 3
        + ["καὶ", "καί"]
        + [""] * 14,
        [""] * 4
        + ["1/5d9", "не", "се \ue205 ѿ него• \ue205 не", "не"]
        + [""] * 3
        + ["οὐχ", "οὐ"]
        + [""] * 14,
    ]
    res = merge([list(r) for r in rows], sl_sem, gr_sem)
    assert res == [
        [""] * 4
        + ["1/5d9", "него•", "се \ue205 ѿ него• \ue205 не", "\ue205 pron."]
        + [""] * 3
        + ["αὐτοῦ", "αὐτός"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["1/5d9", "се", "се \ue205 ѿ него• \ue205 не", "се"]
        + [""] * 3
        + ["ἰδοὺ", "ἰδού"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["1/5d9(1)", "\ue205", "се \ue205 ѿ него• \ue205 не", "\ue205 conj."]
        + [""] * 3
        + ["καὶ", "καί"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["1/5d9", "ѿ", "се \ue205 ѿ него• \ue205 не", "отъ"]
        + [""] * 3
        + ["ἐξ", "ἐκ"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["1/5d9", "него•", "се \ue205 ѿ него• \ue205 не", "\ue205 pron."]
        + [""] * 3
        + ["αὐτοῦ", "αὐτός"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["1/5d9(2)", "\ue205", "се \ue205 ѿ него• \ue205 не", "\ue205 conj."]
        + [""] * 3
        + ["καὶ", "καί"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["1/5d9", "не", "се \ue205 ѿ него• \ue205 не", "не"]
        + [""] * 3
        + ["οὐχ", "οὐ"]
        + [""] * 14
        + ["1"] * 4,
    ]


def test_merge_repeated_velichanie():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )

    rows = [
        ["вел\ue205\ue20dан\ue205е WGH", "вел\ue205\ue20dан\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14,
        ["невел\ue205\ue20d\ue205\ue201 WGH", "невел\ue205\ue20d\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14,
    ]

    r2 = [list(rows[0]), list(rows[1])]
    res = merge(r2, sl_sem, gr_sem)
    assert r2 == rows
    assert sl_sem.cnt_col == STYLE_COL + 1
    assert sl_sem.other().cnt_col == STYLE_COL + 2
    assert gr_sem.cnt_col == STYLE_COL + 3
    assert res == [
        ["вел\ue205\ue20dан\ue205е WGH", "вел\ue205\ue20dан\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["1"] * 4,
        ["невел\ue205\ue20d\ue205\ue201 WGH", "невел\ue205\ue20d\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["2", "1"] * 2,
    ]

    res = merge(rows, gr_sem, sl_sem.var)
    assert sl_sem.cnt_col == STYLE_COL + 1
    assert sl_sem.other().cnt_col == STYLE_COL + 2
    assert gr_sem.cnt_col == STYLE_COL + 3
    assert res == [
        ["вел\ue205\ue20dан\ue205е WGH", "вел\ue205\ue20dан\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["1"] * 4,
        ["невел\ue205\ue20d\ue205\ue201 WGH", "невел\ue205\ue20d\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["2", "1"] * 2,
    ]

    res = merge([list(rows[0]), list(rows[1])], sl_sem.var, gr_sem)
    assert sl_sem.cnt_col == STYLE_COL + 1
    assert sl_sem.other().cnt_col == STYLE_COL + 2
    assert gr_sem.cnt_col == STYLE_COL + 3
    assert res == [
        ["вел\ue205\ue20dан\ue205е WGH", "вел\ue205\ue20dан\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["1"] * 4,
        ["невел\ue205\ue20d\ue205\ue201 WGH", "невел\ue205\ue20d\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["2", "1"] * 2,
    ]


def test_merge_na():
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )

    rows = [
        [""] * 4
        + [
            "02/W169b26",
            "ѡбою",
            "ма же \ue201д\ue205нь ѿ ѡбою на де-",
            "оба",
            "",
            "оба на десѧте",
            "",
        ]
        + ["ιβʹ"] * 2
        + [""] * 3
        + ["δώδεκα MPaPh", "δώδεκα"]
        + [""] * 8
        + ["hl05|bold|italic"],
        [""] * 4
        + ["02/W169b26", "на", "ма же \ue201д\ue205нь ѿ ѡбою на де-", "на", "на + Loc."]
        + [""] * 17
        + ["hl05|hl08|bold|italic"],
        [""] * 4
        + ["02/W169b26", "десете•", "ма же \ue201д\ue205нь ѿ ѡбою на де-", "десѧть"]
        + [""] * 18
        + ["hl05|bold|italic"],
    ]

    res = merge([rows[0].copy(), rows[1].copy(), rows[2].copy()], sl_sem, gr_sem)
    assert res == [
        [""] * 4
        + [
            "02/W169b26",
            "ѡбою на десете•",
            "ма же \ue201д\ue205нь ѿ ѡбою на де-",
            "оба",
            "",
            "оба на десѧте",
            "",
        ]
        + ["ιβʹ"] * 2
        + [""] * 3
        + ["δώδεκα MPaPh", "δώδεκα"]
        + [""] * 8
        + ["hl05|bold|italic"]
        + ["1"] * 4,
        [""] * 4
        + [
            "02/W169b26",
            "ѡбою на десете•",
            "ма же \ue201д\ue205нь ѿ ѡбою на де-",
            "на",
            "на + Loc.",
            "оба на десѧте",
            "",
        ]
        + ["ιβʹ"] * 2
        + [""] * 3
        + ["δώδεκα MPaPh", "δώδεκα"]
        + [""] * 8
        + ["hl05|hl08|bold|italic"]
        + ["1"] * 4,
        [""] * 4
        + [
            "02/W169b26",
            "ѡбою на десете•",
            "ма же \ue201д\ue205нь ѿ ѡбою на де-",
            "десѧть",
            "",
            "оба на десѧте",
            "",
        ]
        + ["ιβʹ"] * 2
        + [""] * 3
        + ["δώδεκα MPaPh", "δώδεκα"]
        + [""] * 8
        + ["hl05|bold|italic"]
        + ["1"] * 4,
    ]

    res = merge([rows[0].copy(), rows[1].copy(), rows[2].copy()], gr_sem, sl_sem)
    assert res == [
        [""] * 4
        + [
            "02/W169b26",
            "ѡбою на десете•",
            "ма же \ue201д\ue205нь ѿ ѡбою на де-",
            "оба & на & десѧть",
            "",
            "оба на десѧте",
            "",
        ]
        + ["ιβʹ"] * 2
        + [""] * 3
        + ["δώδεκα MPaPh", "δώδεκα"]
        + [""] * 8
        + ["hl05|bold|italic"]
        + ["1"] * 4,
        [""] * 4
        + [
            "02/W169b26",
            "ѡбою на десете•",
            "ма же \ue201д\ue205нь ѿ ѡбою на де-",
            "оба & на & десѧть",
            "на + Loc.",
            "оба на десѧте",
            "",
            "ιβʹ",
        ]
        + [""] * 4
        + ["δώδεκα MPaPh", "δώδεκα"]
        + [""] * 8
        + ["hl05|hl08|bold|italic"]
        + ["1"] * 4,
        [""] * 4
        + [
            "02/W169b26",
            "ѡбою на десете•",
            "ма же \ue201д\ue205нь ѿ ѡбою на де-",
            "оба & на & десѧть",
            "",
            "оба на десѧте",
            "",
            "ιβʹ",
        ]
        + [""] * 4
        + ["δώδεκα MPaPh", "δώδεκα"]
        + [""] * 8
        + ["hl05|bold|italic"]
        + ["1"] * 4,
    ]
