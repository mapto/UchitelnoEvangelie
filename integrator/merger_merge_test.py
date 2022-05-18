from const import STYLE_COL
from setup import sl_sem, gr_sem
from semantics import MainLangSemantics, VarLangSemantics
from merger import merge


def test_gram():
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


def test_special():
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


def test_repeated_om():
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


def test_repeated_kai():
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


def test_repeated_velichanie():
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


def test_na():

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
        + ["δώδεκα MPaPh"] * 2
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
        + ["δώδεκα MPaPh"] * 2
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
        + ["δώδεκα MPaPh"] * 2
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
        + ["δώδεκα MPaPh"] * 2
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
        + ["δώδεκα MPaPh"] * 2
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
        + ["δώδεκα MPaPh"] * 2
        + [""] * 8
        + ["hl05|bold|italic"]
        + ["1"] * 4,
    ]


def test_same():
    rows = [
        [""] * 4
        + ["19/97d20", "нѣсть", "", "не"]
        + [""] * 3
        + ["οὐκ", "οὐ"]
        + [""] * 14,
        [""] * 5 + ["=", "", "бꙑт"] + [""] * 3 + ["εἰμί", "εἰμί"] + [""] * 14,
    ]

    res = merge([rows[0].copy(), rows[1].copy()], gr_sem, sl_sem)

    assert res == [
        [""] * 4
        + ["19/97d20", "нѣсть", "", "не"]
        + [""] * 3
        + ["οὐκ", "οὐ"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["19/97d20", "нѣсть", "", "бꙑт"]
        + [""] * 3
        + ["εἰμί", "εἰμί"]
        + [""] * 14
        + ["1"] * 4,
    ]

    res = merge([rows[0].copy(), rows[1].copy()], sl_sem, gr_sem)

    assert res == [
        [""] * 4
        + ["19/97d20", "нѣсть", "", "не"]
        + [""] * 3
        + ["οὐκ", "οὐ"]
        + [""] * 14
        + ["1"] * 4,
        [""] * 4
        + ["19/97d20", "нѣсть", "", "бꙑт"]
        + [""] * 3
        + ["εἰμί", "εἰμί"]
        + [""] * 14
        + ["1"] * 4,
    ]


def test_hodom_spiti():
    rows = [
        [
            "хⷪ҇домь WG ход\ue205т\ue205 H",
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
        + ["hl05|hl00"],
        ["спѣюще WG с пѣн\ue205\ue201мь H"]
        + [""] * 3
        + ["14/72d19", "спѣюще•", "д\ue205мъ спѣюще•", "спѣт\ue205"]
        + [""] * 18
        + ["hl05|hl00"],
    ]
    res = merge([rows[0].copy(), rows[1].copy()], gr_sem, sl_sem)
    # TODO
    # assert res == [
    #     [
    #         "хⷪ҇домь WG ход\ue205т\ue205 H",
    #         "ходъ WG",
    #         "ходомь спѣт\ue205 WG",
    #         "",
    #         "14/72d18",
    #         "ход\ue205мъ",
    #         "себе• по поут\ue205 хо-",
    #         "ход\ue205т\ue205",
    #         "≈ ход\ue205т\ue205 спѣѭще",
    #         "",
    #         "",
    #         "προβαίνοντες",
    #         "προβαίνω",
    #     ]
    #     + [""] * 13
    #     + ["hl05|hl00"]
    #     + ["1"] * 4,
    #     ["спѣюще WG с пѣн\ue205\ue201мь H"]
    #     + [""] * 3
    #     + ["14/72d19", "спѣюще•", "д\ue205мъ спѣюще•", "спѣт\ue205"]
    #     + [""] * 18
    #     + ["hl05|hl00"]
    #     + ["1"] * 4,
    # ]


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
        ["пꙋт\ue205 GH", "пѫть GH"] + [""] * 24 + ["hl00"],
    ]
    res = merge([rows[0].copy(), rows[1].copy()], sl_sem, gr_sem)
    assert res == [
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
        + ["hl00"]
        + ["1"] * 4,
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
        + ["hl00"]
        + ["1"] * 4,
    ]

    res = merge([rows[0].copy(), rows[1].copy()], sl_sem.var, gr_sem)
    assert res == [
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст\ue205\ue201 G / шьств\ue205\ue201 H",
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
        + ["hl00"]
        + ["1"] * 4,
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "пѫть GH",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/028d18",
            "поутошьств\ue205ꙗ",
            "",
            "пѫтошьств\ue205\ue201",
        ]
        + [""] * 3
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00"]
        + ["1"] * 4,
    ]
