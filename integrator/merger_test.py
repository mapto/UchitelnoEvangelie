from typing import List

from model import Index, LangSemantics, MainLangSemantics, VarLangSemantics
from merger import _close, _grouped


def _equal(a: List[List[str]], b: List[List[str]]) -> bool:
    if len(a) != len(b):
        return False
    for r in range(len(a)):
        if len(a[r]) != len(b[r]):
            return False
        for c in range(len(a[r])):
            if a[r][c] != b[r][c]:
                return False
    return True


def test_grouped():
    sem = MainLangSemantics(
        lang="gr",
        word=10,
        lemmas=[11, 12, 13],
        var=VarLangSemantics(lang="gr_var", word=15, lemmas=[16, 17, 19]),
    )
    row = (
        [
            "\ue201л\ue205ко WH",
            "\ue201л\ue205къ",
            "",
            "1/7c12",
            "сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
        ]
        + [""] * 3
        + ["τοῦτο", "οὗτος"]
        + [""] * 11
        + ["hl04|hl00|hl10"]
    )
    assert _grouped(row, sem)

    sem = MainLangSemantics(
        lang="sl",
        word=4,
        lemmas=[6, 7, 8, 9],
        var=VarLangSemantics(lang="sl_var", word=0, lemmas=[1, 2, 19, 20]),
    )
    row = (
        [""] * 3
        + ["1/7d1", "насъ", "оу насъ", "мꙑ"]
        + [""] * 3
        + ["om.", "om."]
        + [""] * 3
        + ["ἡμῖν", "ἡμεῖς"]
        + [""] * 7
    )
    assert not _grouped(row, sem)
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "1/7b19",
            "вѣроують",
            "вьс\ue205 вѣроують",
            "вѣроват\ue205",
        ]
        + [""] * 3
        + ["πιστεύσωσι", "πιστεύω",]
        + [""] * 11
        + ["hl00"]
    )
    assert _grouped(row, sem)
    row = ["\ue205моуть GH", "ѩт\ue205", "", "1/7b19"] + [""] * 19 + ["hl00"]
    assert _grouped(row, sem)


def test_close():
    sl_sem = MainLangSemantics(
        lang="sl",
        word=4,
        lemmas=[6, 7, 8, 9],
        var=VarLangSemantics(lang="sl_var", word=0, lemmas=[1, 2, 19, 20]),
    )
    gr_sem = MainLangSemantics(
        lang="gr",
        word=10,
        lemmas=[11, 12, 13],
        var=VarLangSemantics(lang="gr_var", word=15, lemmas=[16, 17, 19]),
    )
    group = [
        ["все WH", "вьсь", "", "1/7c12", "въ", "въ сел\ue205ко", "въ", "въ + Acc."]
        + [""] * 2
        + ["εἰς", "εἰς",]
        + [""] * 11
        + ["hl04|hl00|hl10"],
        [
            "\ue201л\ue205ко WH",
            "\ue201л\ue205къ",
            "",
            "1/7c12",
            "сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
        ]
        + [""] * 3
        + ["τοῦτο", "οὗτος",]
        + [""] * 11
        + ["hl04|hl00|hl10"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        [
            "все WH \ue201л\ue205ко WH",
            "вьсь & \ue201л\ue205къ",
            "",
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "въ & сел\ue205къ",
            "въ + Acc.",
        ]
        + [""] * 2
        + ["εἰς τοῦτο", "εἰς",]
        + [""] * 11
        + ["hl04|hl00|hl10"],
        [
            "все WH \ue201л\ue205ко WH",
            "вьсь & \ue201л\ue205къ",
            "",
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "въ & сел\ue205къ",
            "въ + Acc.",
        ]
        + [""] * 2
        + ["εἰς τοῦτο", "οὗτος",]
        + [""] * 11
        + ["hl04|hl00|hl10"],
    ]

    group = [
        [""] * 3
        + ["1/5a10", "беꙁ", "ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ", "беꙁ ", "беꙁ вѣдѣн\ue205ꙗ"]
        + [""] * 2
        + ["ἀπείρως", "ἀπείρως",]
        + [""] * 11
        + ["hl04|hl10",],
        [""] * 3
        + [
            "1/5a10",
            "вѣдѣн\ue205ꙗ",
            "ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ",
            "вѣдѣн\ue205\ue201",
        ]
        + [""] * 16
        + ["hl04|hl10",],
    ]
    res = _close(group, sl_sem, gr_sem)
    expected = [
        [""] * 3
        + [
            "01/005a10",
            "беꙁ вѣдѣн\ue205ꙗ",
            "ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ",
            "беꙁ ",
            "беꙁ вѣдѣн\ue205ꙗ",
        ]
        + [""] * 2
        + ["ἀπείρως", "ἀπείρως",]
        + [""] * 11
        + ["hl04|hl10"],
        [""] * 3
        + [
            "01/005a10",
            "беꙁ вѣдѣн\ue205ꙗ",
            "ꙗвѣ• \ue205 беꙁ вѣдѣн\ue205ꙗ",
            "вѣдѣн\ue205\ue201",
            "беꙁ вѣдѣн\ue205ꙗ",
        ]
        + [""] * 2
        + ["ἀπείρως", "ἀπείρως",]
        + [""] * 11
        + ["hl04|hl10"],
    ]
    assert _equal(res, expected)

    group = [
        ["все WH", "вьсь", "", "1/7c12", "въ", "въ сел\ue205ко", "въ", "въ + Acc."]
        + [""] * 2
        + ["εἰς", "εἰς",]
        + [""] * 11
        + ["hl04|hl00|hl07|hl10"],
        [
            "\ue201л\ue205ко WH",
            "\ue201л\ue205къ",
            "",
            "1/7c12",
            "сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
        ]
        + [""] * 3
        + ["τοῦτο", "οὗτος",]
        + [""] * 11
        + ["hl04|hl00|hl10"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        [
            "все WH \ue201л\ue205ко WH",
            "вьсь & \ue201л\ue205къ",
            "",
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "въ & сел\ue205къ",
            "въ + Acc.",
        ]
        + [""] * 2
        + ["εἰς τοῦτο", "εἰς",]
        + [""] * 11
        + ["hl04|hl00|hl07|hl10"],
        [
            "все WH \ue201л\ue205ко WH",
            "вьсь & \ue201л\ue205къ",
            "",
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "въ & сел\ue205къ",
            "въ + Acc.",
        ]
        + [""] * 2
        + ["εἰς τοῦτο", "οὗτος",]
        + [""] * 11
        + ["hl04|hl00|hl10"],
    ]
    assert _equal(res, expected)

    group = [
        [""] * 3
        + [
            "1/5a16",
            "ꙁан\ue201",
            "еще же \ue205 ꙁан\ue201 въꙁвѣст\ue205лъ",
            "ꙁан\ue201",
        ]
        + [""] * 3
        + ["διὰ", "διά ", "διά + Acc.", "διὰ τό",]
        + [""] * 9
        + ["hl04|hl10|hl12"],
        [""] * 3 + ["1/5a16"] + [""] * 6 + ["τὸ", "ὁ"] + [""] * 11 + ["hl04|hl10"],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        [""] * 3
        + [
            "01/005a16",
            "ꙁан\ue201",
            "еще же \ue205 ꙁан\ue201 въꙁвѣст\ue205лъ",
            "ꙁан\ue201",
        ]
        + [""] * 3
        + ["διὰ τὸ", "διά ", "διά + Acc.", "διὰ τό",]
        + [""] * 9
        + ["hl04|hl10|hl12"],
        [""] * 3
        + ["01/005a16", "ꙁан\ue201", "", "ꙁан\ue201",]
        + [""] * 3
        + ["διὰ τὸ", "ὁ", "", "διὰ τό",]
        + [""] * 9
        + ["hl04|hl10"],
    ]
    assert _equal(res, expected)

    group = [
        ["все WH", "вьсь", "", "1/7c12", "въ", "въ сел\ue205ко", "въ", "въ + Acc."]
        + [""] * 2
        + ["εἰς", "εἰς",]
        + [""] * 11
        + ["hl04|hl00|hl07|hl10"],
        [
            "\ue201л\ue205ко WH",
            "\ue201л\ue205къ",
            "",
            "1/7c12",
            "сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
        ]
        + [""] * 3
        + ["τοῦτο", "οὗτος",]
        + [""] * 11
        + ["hl04|hl00|hl10"],
    ]
    res = _close(group, sl_sem, gr_sem)
    expected = [
        [
            "все WH \ue201л\ue205ко WH",
            "вьсь",
            "",
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "въ",
            "въ + Acc.",
        ]
        + [""] * 2
        + ["εἰς τοῦτο", "εἰς & οὗτος",]
        + [""] * 11
        + ["hl04|hl00|hl07|hl10"],
        [
            "все WH \ue201л\ue205ко WH",
            "\ue201л\ue205къ",
            "",
            "01/007c12",
            "въ сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
        ]
        + [""] * 3
        + ["εἰς τοῦτο", "εἰς & οὗτος",]
        + [""] * 11
        + ["hl04|hl00|hl10"],
    ]
    assert _equal(res, expected)

    group = [
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "1/6a11",
            "л\ue205 ",
            "\ue201сть л\ue205 раꙁѹмьно",
            "л\ue205 ",
        ]
        + [""] * 3
        + ["κἂν", "καί", "κἄν",]
        + [""] * 10
        + ["hl10"],
        [""] * 3 + ["1/6a11"] + [""] * 7 + ["ἀν"] + [""] * 11 + ["hl10"],
    ]
    res = _close(group, sl_sem, gr_sem)
    expected = [
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "01/006a11",
            "л\ue205 ",
            "\ue201сть л\ue205 раꙁѹмьно",
            "л\ue205 ",
        ]
        + [""] * 3
        + ["κἂν", "καί & ἀν", "κἄν",]
        + [""] * 10
        + ["hl10"],
        ["\ue205л\ue205 WH", "", "", "01/006a11", "л\ue205 ",]
        + [""] * 5
        + ["κἂν", "καί & ἀν", "κἄν",]
        + [""] * 10
        + ["hl10"],
    ]
    assert _equal(res, expected)

    group = [
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "1/6a11",
            "л\ue205 ",
            "\ue201сть л\ue205 раꙁѹмьно",
            "л\ue205 ",
        ]
        + [""] * 3
        + ["κἂν", "καί", "κἄν",]
        + [""] * 10
        + ["hl10"],
        [""] * 3 + ["1/6a11"] + [""] * 7 + ["ἀν"] + [""] * 11 + ["hl10",],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "01/006a11",
            "л\ue205 ",
            "\ue201сть л\ue205 раꙁѹмьно",
            "л\ue205 ",
        ]
        + [""] * 3
        + ["κἂν", "καί", "κἄν",]
        + [""] * 10
        + ["hl10"],
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "01/006a11",
            "л\ue205 ",
            "",
            "л\ue205 ",
        ]
        + [""] * 3
        + ["κἂν", "ἀν", "κἄν",]
        + [""] * 10
        + ["hl10"],
    ]
    assert _equal(res, expected)

    group = [
        [""] * 3
        + ["1/6a10", "тѣмь", "тѣмь л\ue205 в\ue205д\ue205мо", "тѣмь", "тѣмь л\ue205"]
        + [""] * 2
        + ["κἂν", "καί", "κἄν",]
        + [""] * 10
        + ["hl04"],
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "1/6a10",
            "л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "л\ue205",
        ]
        + [""] * 4
        + ["ἀν"]
        + [""] * 11
        + ["hl04"],
    ]
    res = _close(group, sl_sem, gr_sem)
    expected = [
        ["\ue205л\ue205 WH"]
        + [""] * 2
        + [
            "01/006a10",
            "тѣмь л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь",
            "тѣмь л\ue205",
        ]
        + [""] * 2
        + ["κἂν", "καί & ἀν", "κἄν",]
        + [""] * 10
        + ["hl04"],
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "01/006a10",
            "тѣмь л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "л\ue205",
            "тѣмь л\ue205",
        ]
        + [""] * 2
        + ["κἂν", "καί & ἀν", "κἄν",]
        + [""] * 10
        + ["hl04"],
    ]
    assert _equal(res, expected)

    group = [
        [""] * 3
        + ["1/6a10", "тѣмь", "тѣмь л\ue205 в\ue205д\ue205мо", "тѣмь", "тѣмь л\ue205"]
        + [""] * 2
        + ["κἂν", "καί", "κἄν",]
        + [""] * 10
        + ["hl04"],
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "1/6a10",
            "л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "л\ue205",
        ]
        + [""] * 4
        + ["ἀν", "", "", "", "", "", "", "", "", "", "", "", "hl04",],
    ]
    res = _close(group, gr_sem, sl_sem)
    expected = [
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "01/006a10",
            "тѣмь л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь & л\ue205",
            "тѣмь л\ue205",
        ]
        + [""] * 2
        + ["κἂν", "καί", "κἄν",]
        + [""] * 10
        + ["hl04"],
        [
            "\ue205л\ue205 WH",
            "\ue205л\ue205",
            "",
            "01/006a10",
            "тѣмь л\ue205",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь & л\ue205",
            "тѣмь л\ue205",
        ]
        + [""] * 2
        + ["κἂν", "ἀν", "κἄν",]
        + [""] * 10
        + ["hl04"],
    ]
    assert _equal(res, expected)
