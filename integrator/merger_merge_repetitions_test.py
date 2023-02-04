from const import STYLE_COL
from setup import sl_sem, gr_sem
from semantics import MainLangSemantics, VarLangSemantics
from merger import merge


def test_om():
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
        + ["1"] * 4,
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
        + ["1"] * 4,
    ]


def test_kai():
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

    r2 = [rows[0].copy(), rows[1].copy()]
    res = merge(r2, sl_sem, gr_sem)
    assert r2 == rows
    assert sl_sem.cnt_col == STYLE_COL + 3
    assert sl_sem.var.cnt_col == STYLE_COL + 4
    assert gr_sem.cnt_col == STYLE_COL + 1
    assert gr_sem.var.cnt_col == STYLE_COL + 2
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
    assert sl_sem.cnt_col == STYLE_COL + 3
    assert sl_sem.var.cnt_col == STYLE_COL + 4
    assert gr_sem.cnt_col == STYLE_COL + 1
    assert gr_sem.var.cnt_col == STYLE_COL + 2
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

    res = merge([rows[0].copy(), rows[1].copy()], sl_sem.var, gr_sem)
    assert sl_sem.cnt_col == STYLE_COL + 3
    assert sl_sem.var.cnt_col == STYLE_COL + 4
    assert gr_sem.cnt_col == STYLE_COL + 1
    assert gr_sem.var.cnt_col == STYLE_COL + 2
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


def test_repeated_nareshti():
    rows = [
        [""] * 4
        + ["38/179c02", "наре\ue20dе", "его наре\ue20dе наре-", "нарещ\ue205"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 3
        + ["ἔφησεν", "φημί"]
        + [""] * 9,
        ["рещ\ue205 H"]
        + [""] * 3
        + ["38/179c02", "нарещ\ue205", "его наре\ue20dе наре-", "нарещ\ue205"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 3
        + ["καλεῖσθαι", "καλέω", "pass."]
        + [""] * 8,
    ]
    res = merge(rows, sl_sem, gr_sem)
    assert res == [
        [""] * 4
        + ["38/179c02", "наре\ue20dе", "его наре\ue20dе наре-", "нарещ\ue205"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 3
        + ["ἔφησεν", "φημί"]
        + [""] * 9
        + ["1", "1", "1", "1"],
        ["рещ\ue205 H"]
        + [""] * 3
        + ["38/179c02", "нарещ\ue205", "его наре\ue20dе наре-", "нарещ\ue205"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 3
        + ["καλεῖσθαι", "καλέω", "pass."]
        + [""] * 8
        + ["1", "1", "2", "1"],
    ]
