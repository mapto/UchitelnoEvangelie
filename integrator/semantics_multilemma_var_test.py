from model import Source
from semantics import MainLangSemantics, VarLangSemantics

from const import STYLE_COL
from config import FROM_LANG, TO_LANG

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
    [12, 13, 14],
    VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20], cnt_col=STYLE_COL + 4),
    cnt_col=STYLE_COL + 3,
)


def test_prichatnik_relative():
    row = (
        [
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 боудоть G пр\ue205\ue20dестн\ue205ц\ue205 боудоть H",
            "бꙑт\ue205 GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "≈ GH",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "боудоуть• \ue201же",
            "пр\ue205\ue20dьтьн\ue205къ & бꙑт\ue205",
            "≈ пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "",
            "",
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05:FFFCD5B4|hl11:FFFCD5B4"]
        + ["1"] * 4
    )

    result = sl_sem.var.multilemma(row, 2)
    assert result == {Source("GH"): "≈"}


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
    result = gr_sem.var.multilemma(row)
    assert result == {Source("Ch"): "ὁ"}


def test_istochenii():
    row = (
        [""] * 4
        + [
            "1/W168c17",
            "\ue205сто\ue20dен\ue205\ue205",
            "всѣмь прѣ\ue205сто\ue20dе\ue201• \ue205 по \ue205сто\ue20dен\ue205\ue205",
            "\ue205сто\ue20dен\ue205\ue201",
        ]
        + [""] * 3
        + ["ὑπερκλύσαι", "ὑπερκλύζω", "Inf."]
        + [""] * 2
        + ["ὑπερβλύσαι", "ὑπερβλύω", "Inf."]
        + [""] * 8
        + ["1"] * 4
    )
    result = gr_sem.var.multilemma(row, 1)
    assert result == {Source("Cs"): "Inf."}


if __name__ == "__main__":
    test_istochenii()
