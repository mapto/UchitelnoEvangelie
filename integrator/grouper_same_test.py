from config import FROM_LANG, TO_LANG
from model import Index
from semantics import MainLangSemantics, VarLangSemantics
from grouper import _unwrap_same, _close_group

Index.maxlen = [2, 1, 3, 3, 2, 2]
sl_sem = MainLangSemantics(
    FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
)
gr_sem = MainLangSemantics(
    TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20])
)


def test_unwrap_same():
    rows = [
        [""] * 4
        + ["19/97d20", "нѣсть", "", "не"]
        + [""] * 3
        + ["οὐκ", "οὐ"]
        + [""] * 14,
        [""] * 5 + ["=", "", "бꙑт"] + [""] * 3 + ["εἰμί", "εἰμί"] + [""] * 14,
    ]

    res = _unwrap_same([rows[0].copy(), rows[1].copy()], gr_sem, sl_sem)

    assert res == [
        [""] * 4
        + ["19/97d20", "нѣсть", "", "не"]
        + [""] * 3
        + ["οὐκ", "οὐ"]
        + [""] * 14,
        [""] * 5 + ["нѣсть", "", "бꙑт"] + [""] * 3 + ["εἰμί", "εἰμί"] + [""] * 14,
    ]


def test_close_group():
    rows = [
        [""] * 4
        + ["19/97d20", "нѣсть", "", "не"]
        + [""] * 3
        + ["οὐκ", "οὐ"]
        + [""] * 14,
        [""] * 4
        + ["19/97d20", "=", "", "бꙑт"]
        + [""] * 3
        + ["εἰμί", "εἰμί"]
        + [""] * 14,
    ]

    res = _close_group([rows[0].copy(), rows[1].copy()], sl_sem, gr_sem)

    assert res == [
        [""] * 4
        + ["19/097d20", "нѣсть", "", "не"]
        + [""] * 3
        + ["οὐκ εἰμί", "οὐ & εἰμί"]
        + [""] * 14,
        [""] * 4
        + ["19/097d20", "нѣсть", "", "бꙑт\ue205"]
        + [""] * 3
        + ["οὐκ εἰμί", "οὐ & εἰμί"]
        + [""] * 14,
    ]

    res = _close_group([rows[0].copy(), rows[1].copy()], gr_sem, sl_sem)

    assert res == [
        [""] * 4
        + ["19/097d20", "нѣсть", "", "не & бꙑт\ue205"]
        + [""] * 3
        + ["οὐκ εἰμί", "οὐ"]
        + [""] * 14,
        [""] * 4
        + ["19/097d20", "нѣсть", "", "не & бꙑт\ue205"]
        + [""] * 3
        + ["οὐκ εἰμί", "εἰμί"]
        + [""] * 14,
    ]
