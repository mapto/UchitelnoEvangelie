from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import FROM_LANG, TO_LANG
from config import FROM_LANG
from const import STYLE_COL

from model import Index, Source, Alignment, Alternative, Usage
from semantics import MainLangSemantics, VarLangSemantics
from aggregator import _agg_lemma

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


def test_prichatnik():
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

    # result = _agg_lemma(rows, sl_sem.var, gr_sem, SortedDict(), col=LAST_LEMMA, olemvar=Source('G'), tlemma="ποιέω & κοινωνός")
    result = _agg_lemma(
        row,
        sl_sem.var,
        gr_sem,
        SortedDict(),
        col=3,
        olemvar=Source("GH"),
        tlemma="ποιέω & κοινωνός",
    )
    assert result == {
        "": {
            "": {
                "≈ ποιέω κοινωνόν → ποιέω & κοινωνός": {
                    (
                        "пр\ue205\ue20dестн\ue205ц\ue205 боудоть H пр\ue205\ue20dестьн\ue205ц\ue205 боудоть G",
                        "ποιῆσαι κοινωνοὺς",
                    ): SortedSet(
                        [
                            Alignment(
                                Index("5/28c21-d1"),
                                Usage(
                                    "sl",
                                    Source("GH"),
                                    "пр\ue205\ue20dестн\ue205ц\ue205 боудоть H пр\ue205\ue20dестьн\ue205ц\ue205 боудоть G",
                                    [
                                        "бꙑт\ue205",
                                        "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205",
                                    ],
                                    main_alt=Alternative(
                                        "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
                                        [
                                            "пр\ue205\ue20dьтьн\ue205къ & бꙑт\ue205",
                                            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
                                        ],
                                        semantic="≈",
                                    ),
                                ),
                                Usage(
                                    "gr",
                                    word="ποιῆσαι κοινωνοὺς",
                                    lemmas=[
                                        "ποιέω & κοινωνός",
                                        "≈ ποιέω κοινωνόν",
                                    ],
                                ),
                                semantic="≈",
                            )
                        ]
                    )
                }
            }
        }
    }
