"""Tests of LangSemantics.compile_usages with SPECIAL_CHARS"""

from sortedcontainers.sorteddict import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL
from model import Alternative, Index, Source, Alignment, Usage
from semantics import MainLangSemantics, VarLangSemantics

# semantics update from September 2021
# with repetitions added (as if after merge)
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
    VarLangSemantics(TO_LANG, 16, [17, 18, 19], cnt_col=STYLE_COL + 4),
    cnt_col=STYLE_COL + 3,
)


def test_prichatnik():
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

    result = sl_sem.compile_usages(gr_sem, row, "ποιέω & κοινωνός")
    assert result == SortedDict(
        {
            "ποιέω κοινωνόν → ποιέω & κοινωνός": {
                (
                    "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                    "ποιῆσαι κοινωνοὺς",
                ): SortedSet(
                    [
                        Alignment(
                            Index("5/28c21-d1"),
                            Usage(
                                "sl",
                                word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                lemmas=[
                                    "пр\ue205\ue20dьтьн\ue205къ",
                                    "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
                                    "≈",
                                ],
                                var_alt={
                                    Source("GH"): Alternative(
                                        "пр\ue205\ue20dестьн\ue205ц\ue205 G пр\ue205\ue20dестн\ue205ц\ue205 H",
                                        [
                                            "пр\ue205\ue20dѧстьн\ue205къ",
                                            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                        ],
                                        semantic="≈",
                                    )
                                },
                            ),
                            Usage(
                                "gr",
                                word="ποιῆσαι κοινωνοὺς",
                                lemmas=["ποιέω & κοινωνός", "ποιέω κοινωνόν"],
                            ),
                        )
                    ]
                )
            }
        }
    )
