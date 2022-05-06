from typing import List

from config import FROM_LANG, TO_LANG
from semantics import MainLangSemantics, VarLangSemantics
from merger import _collect_group, _hilited_gram

from setup import sl_sem, gr_sem


def test_zemenu():
    rows = [
        [""] * 4
        + ["19/94d08"]
        + ["ₓ", ""] * 2
        + [""] * 7
        + ["τῶν Ch", "ὁ"]
        + [""] * 8
        + ["hl16|hl19"],
        [""] * 4
        + ["19/94d08", "ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["ἐπὶ Ch", "ἐπί", "ἐπί + Gen.", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16|hl18"],
        [""] * 4 + ["19/94d08"] + [""] * 11 + ["γῆς Ch", "γῆ"] + [""] * 8 + ["hl16"],
    ]

    merge_rows_main = [0, 1, 2]
    merge_rows_var = [1, 2]

    res = _collect_group(rows.copy(), sl_sem, gr_sem, merge_rows_main, merge_rows_var)
    assert (
        res
        == [""] * 5
        + ["ₓ ꙁемьнꙑ\ue205"]
        + [""] * 10
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ Ch", "", "ὁ ἐπὶ γῆς Ch"]
        + [""] * 6
    )
