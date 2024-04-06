from config import FROM_LANG, TO_LANG
from const import STYLE_COL
from semantics import MainLangSemantics, VarLangSemantics


sl_sem = MainLangSemantics(
    FROM_LANG,
    5,
    [7, 8, 9, 10],
    VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
    cnt_col=STYLE_COL + 1,
)
gr_sem = MainLangSemantics(
    TO_LANG,
    11,
    [12, 13, 14, 15],
    VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20], cnt_col=STYLE_COL + 4),
    cnt_col=STYLE_COL + 3,
)


def test_build_content():
    row = (
        [
            "\ue201сть GH",
            "бꙑт\ue205",
            "",
            "gramm.",
            "07/47a06",
            "om.",
            "сътвор\ue205лъ",
            "om.",
        ]
        + [""] * 3
        + ["Ø"] * 2
        + [""] * 13
        + ["hl03"]
        + ["1"] * 4
    )
    result = sl_sem.var.var_alt_lemmas(row)
    assert result == {"G": ["бꙑт\ue205", "gramm."], "H": ["бꙑт\ue205", "gramm."]}


def test_zemen():
    row = (
        [""] * 4
        + ["19/94d08", "ₓ ꙁемьнꙑ\ue205", "", "ₓ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "ὁ"]
        + [""] * 8
        + ["hl16:FFF8CBAD|hl19:FFB4C7E7"]
        + ["1"] * 4
    )
    result = gr_sem.var.var_alt_lemmas(row)
    assert result == {"Ch": ["ὁ"]}
