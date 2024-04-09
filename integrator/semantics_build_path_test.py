from config import FROM_LANG
from const import STYLE_COL
from model import Path
from semantics import MainLangSemantics, VarLangSemantics

sl_sem = MainLangSemantics(
    FROM_LANG,
    5,
    [7, 8, 9, 10],
    VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
    cnt_col=STYLE_COL + 1,
)


def test_satvoriti():
    row = (
        [
            "не створ\ue205т\ue205 H",
            "не & сътвор\ue205т\ue205 H",
            "не сътвор\ue205т\ue205 H",
            "≈ H",
            "47/214c06",
            "не твор\ue205т\ue205",
            "ѭ не твор\ue205т\ue205",
            "не",
            "не твор\ue205т\ue205",
            "≈",
            "",
            "ἀμελεῖν",
            "ἀμελέω",
        ]
        + [""] * 14
        + ["hl05:FFFCD5B4"]
        + ["1"] * 4
    )

    result = sl_sem.build_paths(row)
    assert result == [Path(parts=["не", "не твор\ue205т\ue205"], semantics="≈")]

    result = sl_sem.var.build_paths(row)
    assert result == [
        Path(
            parts=["не & сътвор\ue205т\ue205", "не сътвор\ue205т\ue205"],
            annotation="",
            semantics="≈",
        )
    ]
