from config import FROM_LANG
from const import STYLE_COL
from model import Alternative, Source, Usage
from semantics import MainLangSemantics, VarLangSemantics
from semantics.lang import _build_content

sl_sem = MainLangSemantics(
    FROM_LANG,
    5,
    [7, 8, 9, 10],
    VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
    cnt_col=STYLE_COL + 1,
)


def test_relative():
    row = (
        [
            "боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 G пр\ue205\ue20dестн\ue205ц\ue205 H",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "≈ GH",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "≈",
            "",
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05:FFFCD5B4|hl00:FFFCD5B4|hl11:FFFCD5B4"]
        + ["1"] * 4
    )
    result = _build_content(row, sl_sem, Source(), "прьтьнц боудоуть", 1)
    assert result == Usage(
        lang="sl",
        main_alt=Alternative(),
        var_alt={
            Source("GH"): Alternative(
                "пр\ue205\ue20dестьн\ue205ц\ue205 G пр\ue205\ue20dестн\ue205ц\ue205 H",
                [
                    "пр\ue205\ue20dѧстьн\ue205къ",
                    "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                ],
                1,
                "≈",
            )
        },
        word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
        lemmas=[
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "≈",  # TODO remove
        ],
    )
