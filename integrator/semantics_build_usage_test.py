from distutils.command.config import config


from const import STYLE_COL
from config import FROM_LANG, TO_LANG

from semantics.lang import MainLangSemantics, VarLangSemantics
from semantics.lang import _build_usage

from model import Alternative, Index, Source, Usage, UsageContent

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


def test_build_usage():
    row = (
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "пѫть GH",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/028d18",
            "поутошьств\ue205ꙗ",
            "",
            "пѫтошьств\ue205\ue201",
        ]
        + [""] * 3
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00"]
        + ["1"] * 4
    )

    result = _build_usage(
        row,
        sl_sem.var,
        gr_sem,
        Source("GH"),
        Source(),
        "шьствꙗ пꙋт H шьстꙗ пꙋт G",
        "пѫть",
        "ὁδοιπορίας",
        "ὁδοιπορία",
        1,
        1,
    )
    assert result == Usage(
        Index.unpack("5/28d18"),
        UsageContent(
            "sl",
            Source("GH"),
            Alternative(
                main_lemma="пѫтошьств\ue205\ue201",
                var_lemmas={
                    Source("H"): "шьств\ue205\ue201 пѫт\ue205",
                    Source("G"): "шьст\ue205\ue201 пѫт\ue205",
                },
                main_word="поутошьств\ue205ꙗ",
                var_words={
                    Source("G"): ("шьст\ue205ꙗ пꙋт\ue205 G", 1),
                    Source("H"): ("шьств\ue205ꙗ пꙋт\ue205 H", 1),
                },
            ),
            "шьств\ue205ꙗ пꙋт\ue205 H шьст\ue205ꙗ пꙋт\ue205 G",
            ["пѫть"],
        ),
        UsageContent("gr", word="ὁδοιπορίας", lemmas=["ὁδοιπορία"]),
    )
