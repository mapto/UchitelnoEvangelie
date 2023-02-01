from typing import List

from config import FROM_LANG, TO_LANG
from model import Index
from semantics import MainLangSemantics, VarLangSemantics
from merger import _close

Index.maxlen = [2, 1, 3, 3, 2, 2]
sl_sem = MainLangSemantics(
    FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
)
gr_sem = MainLangSemantics(
    TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20])
)


def test_vispatiu():
    # INFO:root:Събиране на многоредови преводи от гръцки основен към славянски...
    rows = [
        [""] * 4
        + ["35/163a07", "въспꙗть", "\ue205 в\ue205дѣвъ• въ-", "въспѧть"]
        + [""] * 3
        + ["εἰς", "εἰς", "εἰς τοὐπίσω"]
        + [""] * 12
        + ["hl11:FFF8CBAD"],
        [""] * 4
        + ["", "ₓ"] * 2
        + [""] * 3
        + ["τοὐπίσω", "ὁ"]
        + [""] * 13
        + ["hl11:FFF8CBAD|hl14:FFB4C7E7"],
        [""] * 11 + ["=", "ὀπίσω"] + [""] * 13 + ["hl11:FFF8CBAD"],
    ]

    res = _close(rows, gr_sem, sl_sem)
    assert res == [
        [""] * 4
        + ["35/163a07", "въспꙗть ₓ", "\ue205 в\ue205дѣвъ• въ-", "въспѧть"]
        + [""] * 3
        + ["εἰς τοὐπίσω", "εἰς", "εἰς τοὐπίσω"]
        + [""] * 12
        + ["hl11:FFF8CBAD"],
        [""] * 5
        + ["въспꙗть ₓ", "", "ₓ"]
        + [""] * 3
        + ["εἰς τοὐπίσω", "ὁ"]
        + [""] * 13
        + ["hl11:FFF8CBAD|hl14:FFB4C7E7"],
        [""] * 4
        + ["35/163a07", "въспꙗть ₓ", "", "въспѧть"]
        + [""] * 3
        + ["εἰς τοὐπίσω", "ὀπίσω", "εἰς τοὐπίσω"]
        + [""] * 12
        + ["hl11:FFF8CBAD"],
    ]
