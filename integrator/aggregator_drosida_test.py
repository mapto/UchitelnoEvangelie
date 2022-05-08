from sortedcontainers import SortedDict  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL

from semantics import MainLangSemantics, VarLangSemantics
from aggregator import aggregate, _expand_and_aggregate


def drosida_test():
    sl_sem = MainLangSemantics(
        FROM_LANG,
        5,
        [7],
        VarLangSemantics(FROM_LANG, 0, [1], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )
    gr_sem = MainLangSemantics(
        TO_LANG,
        11,
        [12],
        VarLangSemantics(TO_LANG, 16, [17, 18], cnt_col=STYLE_COL + 4),
        cnt_col=STYLE_COL + 3,
    )

    rows = [
        [
            "на",
            "",
            "",
            "",
            "554.26",
            "om.",
            "ἐμβληθῆναι ἐν αὐτῇ τὰς ἱερὰς γυναῖκας, καὶ σὺν αὐταῖς χαλκὸν ἱκανόν, ἐφ᾽ ᾧ διὰ τῆς ἀναλύσεως ἀμφοτέρων",
            "",
            "",
            "",
            "",
            "διὰ",
            "διά",
            "διά + G",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "hl22",
            "1",
            "1",
            "1",
            "1",
        ],
        [
            "Instr.",
            "Instr. B",
            "",
            "",
            "554.27",
            "вь",
            "ἀναμιγῆναι τὸν χαλκὸν μετὰ τοῦ χοὸς τῶν ἁγίων γυναικῶν· καὶ διὰ τοῦ τοιούτου χαλκοῦ κατασκευασθῆναι",
            "",
            "",
            "",
            "",
            "διὰ",
            "διά",
            "διά + G",
            "",
            "",
            "",
            "",
            "",
            "",
            "Instr. B",
            "",
            "",
            "",
            "",
            "",
            "hl22",
            "1",
            "1",
            "1",
            "1",
        ],
    ]

    result = SortedDict()
    result = aggregate(rows, sl_sem, gr_sem, result)
    assert result == {}

    result = SortedDict()
    result = _expand_and_aggregate([rows[1]], sl_sem.var, gr_sem, result)
    assert result == {}
