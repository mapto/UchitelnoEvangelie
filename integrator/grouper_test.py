from typing import List

from model import Source
from grouper import _hilited, _hilited_gram
from grouper import _group_variants, _update_group, _collect_group
from setup import sl_sem, gr_sem


def test_grouped():
    row = (
        [
            "\ue201л\ue205ко WH",
            "\ue201л\ue205къ",
        ]
        + [""] * 2
        + [
            "1/7c12",
            "сел\ue205ко",
            "въ сел\ue205ко",
            "сел\ue205къ",
        ]
        + [""] * 3
        + ["τοῦτο", "οὗτος"]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl00:AAAAAAAA|hl11:AAAAAAAA"]
    )
    assert _hilited(row, gr_sem)

    row = (
        [""] * 4
        + ["1/7d1", "насъ", "оу насъ", "мꙑ"]
        + [""] * 3
        + ["om.", "om."]
        + [""] * 3
        + ["ἡμῖν", "ἡμεῖς"]
        + [""] * 9
    )
    assert not _hilited(row, sl_sem)
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "",
            "1/7b19",
            "вѣроують",
            "вьс\ue205 вѣроують",
            "вѣроват\ue205",
        ]
        + [""] * 3
        + [
            "πιστεύσωσι",
            "πιστεύω",
        ]
        + [""] * 13
        + ["hl00:AAAAAAAA"]
    )
    assert _hilited(row, sl_sem)
    row = (
        ["\ue205моуть GH", "ѩт\ue205"]
        + [""] * 2
        + ["1/7b19"]
        + [""] * 21
        + ["hl00:AAAAAAAA"]
    )
    assert _hilited(row, sl_sem)


def test_group_variants():
    g1 = (
        [""] * 2
        + [
            "тѣмь \ue205л\ue205",
            "",
            "1/6a10",
            "тѣмь",
            "тѣмь л\ue205 в\ue205д\ue205мо",
            "тѣмь",
            "тѣмь л\ue205",
        ]
        + [""] * 2
        + ["κἂν"] * 2
        + [""] * 13
        + ["hl04:AAAAAAAA"]
    )
    g2 = (
        ["\ue205л\ue205 WH", "\ue205л\ue205"]
        + [""] * 2
        + ["1/6a10", "л\ue205", "тѣмь л\ue205 в\ue205д\ue205мо", "л\ue205"]
        + [""] * 18
        + ["hl04:AAAAAAAA"]
    )
    group = [g1, g2]
    res = _group_variants(group, sl_sem)
    assert res == Source("WH")


def test_merge_rows():
    rows = [
        [""] * 4
        + ["19/94d08"]
        + ["ₓ", ""] * 2
        + [""] * 7
        + ["τῶν Ch", "ὁ"]
        + [""] * 8
        + ["hl16:AAAAAAAA|hl19:AAAAAAAA"],
        [""] * 4
        + ["19/94d08", "ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["ἐπὶ Ch", "ἐπί", "ἐπί + Gen.", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16:AAAAAAAA|hl18:AAAAAAAA"],
        [""] * 4
        + ["19/94d08"]
        + [""] * 11
        + ["γῆς Ch", "γῆ"]
        + [""] * 8
        + ["hl16:AAAAAAAA"],
    ]

    merge_rows_main = [
        i for i, r in enumerate(rows) if not _hilited_gram(sl_sem, gr_sem, r)
    ]
    assert merge_rows_main == [0, 1, 2]

    merge_rows_var = [
        i for i, r in enumerate(rows) if not _hilited_gram(sl_sem, gr_sem.var, r)
    ]
    assert merge_rows_var == [1, 2]


def test_merge_rows_raspatu():
    rows = [
        ["распетоу WG", "распѧт\ue205"]
        + [""] * 2
        + ["18/89c21", "пропѧтоу", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"],
        [""] * 4
        + ["18/89c21-d01", "бꙑт\ue205•", "же пропѧтоу бꙑ-", "бꙑт\ue205", "", "gramm."]
        + [""] * 2
        + ["pass."]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"],
    ]

    merge_rows_main = [
        i for i, r in enumerate(rows) if not _hilited_gram(sl_sem, gr_sem, r)
    ]
    assert merge_rows_main == [0]

    merge_rows_var = [
        i for i, r in enumerate(rows) if not _hilited_gram(sl_sem, gr_sem.var, r)
    ]
    assert merge_rows_var == [0]


def test_update_group_zemen():
    rows = [
        [""] * 4
        + ["19/94d08"]
        + ["ₓ", ""] * 2
        + [""] * 7
        + ["τῶν Ch", "ὁ"]
        + [""] * 8
        + ["hl16:AAAAAAAA|hl19:AAAAAAAA"],
        [""] * 4
        + ["19/94d08", "ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["ἐπὶ Ch", "ἐπί", "ἐπί + Gen.", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16:AAAAAAAA|hl18:AAAAAAAA"],
        [""] * 4
        + ["19/94d08"]
        + [""] * 11
        + ["γῆς Ch", "γῆ"]
        + [""] * 8
        + ["hl16:AAAAAAAA"],
    ]
    merge_rows_main = [0, 1, 2]
    merge_rows_var = [1, 2]

    line = (
        [""] * 5
        + ["ₓ ꙁемьнꙑ\ue205"]
        + [""] * 10
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ", "", "ὁ ἐπὶ γῆς"]
        + [""] * 6
    )

    res = _update_group(rows, sl_sem, gr_sem, line, merge_rows_main, merge_rows_var)
    assert res == [
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205", "", "ₓ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "ὁ"]
        + [""] * 8
        + ["hl16:AAAAAAAA|hl19:AAAAAAAA"],
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ", "ἐπί + Gen.", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16:AAAAAAAA|hl18:AAAAAAAA"],
        [""] * 4
        + ["19/094d08", "ₓ ꙁемьнꙑ\ue205"]
        + [""] * 10
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ", "", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16:AAAAAAAA"],
    ]


def test_update_group_puteshestvie():
    rows = [
        [
            "шьст\ue205ꙗ G шьств\ue205ꙗ H",
            "шьст\ue205\ue201 G / шьств\ue205\ue201 H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/28d18",
            "поутошьств\ue205ꙗ",
            "поутошьств\ue205-",
            "пѫтошьств\ue205\ue201",
        ]
        + [""] * 3
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00:AAAAAAAA"],
        ["пꙋт\ue205 GH", "пѫть GH"] + [""] * 24 + ["hl00:AAAAAAAA"],
    ]
    merge = (
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст\ue205\ue201 пѫть G шьств\ue205\ue201 пѫть H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
        ]
        + [""] * 2
        + ["поутошьств\ue205ꙗ"]
        + [""] * 5
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
    )
    merge_rows_main = [0, 1]
    merge_rows_var = [0, 1]
    result = _update_group(rows, sl_sem, gr_sem, merge, merge_rows_main, merge_rows_var)
    assert result == [
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст\ue205\ue201 пѫть G шьств\ue205\ue201 пѫть H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/028d18",
            "поутошьств\ue205ꙗ",
            "поутошьств\ue205-",
            "пѫтошьств\ue205\ue201",
        ]
        + [""] * 3
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00:AAAAAAAA"],
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст\ue205\ue201 пѫть G шьств\ue205\ue201 пѫть H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/028d18",
            "поутошьств\ue205ꙗ",
        ]
        + [""] * 5
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00:AAAAAAAA"],
    ]


def test_biti():
    g1 = (
        [""] * 4
        + [
            "1/W168a14",
            "вьꙁмогл\ue205",
            "мы брьньн\ue205 \ue205 ꙁемⷧ҇ьн\ue205\ue205• вьꙁмогл\ue205",
            "въꙁмощ\ue205",
        ]
        + [""] * 3
        + [
            "ἠδυνήθημεν",
            "δύναμαι",
        ]
        + [""] * 13
        + [
            "hl05:AAAAAAAA",
        ]
    )
    g2 = (
        [""] * 4
        + [
            "1/W168a15",
            "б\ue205хомь",
            "б\ue205хомь стрьпѣтї• ",
            "бꙑт\ue205 ",
            "",
            "gramm.",
        ]
        + [""] * 2
        + [
            "pass.",
        ]
        + [""] * 13
        + ["hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    group = [g1.copy(), g2.copy()]

    line = (
        [""] * 5
        + ["вьꙁмогл\ue205 б\ue205хомь"]
        + [""] * 5
        + ["ἠδυνήθημεν", "δύναμαι"]
        + [""] * 13
    )

    res = _update_group(group, sl_sem, gr_sem, line, [0], [])
    e1 = (
        [""] * 4
        + [
            "01/W168a14-15",
            "вьꙁмогл\ue205 б\ue205хомь",
            "мы брьньн\ue205 \ue205 ꙁемⷧ҇ьн\ue205\ue205• вьꙁмогл\ue205",
            "въꙁмощ\ue205",
        ]
        + [""] * 3
        + ["ἠδυνήθημεν", "δύναμαι"]
        + [""] * 13
        + ["hl05:AAAAAAAA"]
    )
    e2 = (
        [""] * 4
        + [
            "1/W168a15",
            "вьꙁмогл\ue205 б\ue205хомь",
            "б\ue205хомь стрьпѣтї• ",
            "бꙑт\ue205 ",
            "",
            "gramm.",
            "",
            "ἠδυνήθημεν",
            "pass.",
        ]
        + [""] * 13
        + [
            "hl05:AAAAAAAA|hl09:AAAAAAAA",
        ]
    )
    expected = [e1, e2]
    assert res == expected


def test_zemenu():
    rows = [
        [""] * 4
        + ["19/94d08"]
        + ["ₓ", ""] * 2
        + [""] * 7
        + ["τῶν Ch", "ὁ"]
        + [""] * 8
        + ["hl16|hl19"],
        [""] * 4
        + ["19/94d08", "ꙁемьнꙑ\ue205", "сад\ue205 ꙁемьнꙑ-", "ꙁемьнъ"]
        + [""] * 8
        + ["ἐπὶ Ch", "ἐπί", "ἐπί + Gen.", "ὁ ἐπὶ γῆς"]
        + [""] * 6
        + ["hl16:AAAAAAAA|hl18:AAAAAAAA"],
        [""] * 4
        + ["19/94d08"]
        + [""] * 11
        + ["γῆς Ch", "γῆ"]
        + [""] * 8
        + ["hl16:AAAAAAAA"],
    ]

    merge_rows_main = [0, 1, 2]
    merge_rows_var = [1, 2]

    res = _collect_group(rows.copy(), sl_sem, gr_sem, merge_rows_main, merge_rows_var)
    assert (
        res
        == [""] * 5
        + ["ₓ ꙁемьнꙑ\ue205"]
        + [""] * 10
        + ["τῶν ἐπὶ γῆς Ch", "ἐπί & γῆ Ch", "", "ὁ ἐπὶ γῆς Ch"]
        + [""] * 6
    )


def test_hilited_gram():
    r = (
        [""] * 4
        + [
            "1/W168a15",
            "б\ue205хомь",
            "б\ue205хомь стрьпѣтї• ",
            "бꙑт\ue205 ",
            "",
            "gramm.",
        ]
        + [""] * 16
        + ["hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    assert _hilited_gram(sl_sem, gr_sem, r)
    assert _hilited_gram(gr_sem, sl_sem, r)
    r = (
        [""] * 4
        + [
            "1/W168a14",
            "вьꙁмогл\ue205",
            "мы брьньн\ue205 \ue205 ꙁемⷧ҇ьн\ue205\ue205• вьꙁмогл\ue205",
            "въꙁмощ\ue205",
        ]
        + [""] * 3
        + ["ἠδυνήθημεν", "δύναμαι", "pass."]
        + [""] * 12
        + ["hl05:AAAAAAAA"]
    )
    assert not _hilited_gram(sl_sem, gr_sem, r)
    assert not _hilited_gram(gr_sem, sl_sem, r)
    r = (
        [
            "+ \ue201сть GH",
            "бꙑт\ue205",
            "gramm.",
            "",
            "07/47a06",
            "om.",
            "сътвор\ue205лъ",
            "om.",
        ]
        + [""] * 18
        + ["hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    assert _hilited_gram(sl_sem, gr_sem, r)
    r = (
        [""] * 4
        + ["12/67c10", "бꙑхомъ•", "в\ue205дѣл\ue205 бꙑхо-", "бꙑт\ue205"]
        + ["", "gramm.", ""] * 2
        + [""] * 12
        + ["hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    assert _hilited_gram(sl_sem, gr_sem, r)


def test_hilited_gram_cross():
    rows = [
        ["распетоу WG", "распѧт\ue205"]
        + [""] * 2
        + ["18/89c21", "пропѧтоу", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"],
        [""] * 4
        + ["18/89c21-d01", "бꙑт\ue205•", "же пропѧтоу бꙑ-", "бꙑт\ue205", "", "gramm."]
        + [""] * 2
        + ["pass."]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"],
    ]

    assert (
        False
        == _hilited_gram(sl_sem, gr_sem, rows[0])
        == _hilited_gram(sl_sem.var, gr_sem, rows[0])
    )
    assert (
        True
        == _hilited_gram(sl_sem, gr_sem, rows[1])
        == _hilited_gram(sl_sem.var, gr_sem, rows[1])
    )


def test_collect_group():
    rows = [
        [
            "шьст\ue205ꙗ G шьств\ue205ꙗ H",
            "шьст\ue205\ue201 G / шьств\ue205\ue201 H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/28d18",
            "поутошьств\ue205ꙗ",
            "поутошьств\ue205-",
            "пѫтошьств\ue205\ue201",
        ]
        + [""] * 3
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00"],
        ["пꙋт\ue205 GH", "пѫть GH"] + [""] * 24 + ["hl00:AAAAAAAA"],
    ]
    merge_rows_main = [0, 1]
    merge_rows_var = [0, 1]
    result = _collect_group(rows, sl_sem, gr_sem, merge_rows_main, merge_rows_var)
    assert result == (
        [
            "шьст\ue205ꙗ пꙋт\ue205 G шьств\ue205ꙗ пꙋт\ue205 H",
            "шьст\ue205\ue201 пѫть G / шьств\ue205\ue201 пѫть H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
        ]
        + [""] * 2
        + ["поутошьств\ue205ꙗ"]
        + [""] * 5
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
    )
