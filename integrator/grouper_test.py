from model import Source
from setup import sl_sem, gr_sem

from grouper import _merge_indices
from grouper import _hilited, _hilited_local
from grouper import _group_variants


def test_hilited():
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
    assert _hilited_local(sl_sem, gr_sem, r)
    assert _hilited_local(gr_sem, sl_sem, r)
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
    assert not _hilited_local(sl_sem, gr_sem, r)
    assert not _hilited_local(gr_sem, sl_sem, r)
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
    assert _hilited_local(sl_sem, gr_sem, r)
    r = (
        [""] * 4
        + ["12/67c10", "бꙑхомъ•", "в\ue205дѣл\ue205 бꙑхо-", "бꙑт\ue205"]
        + ["", "gramm.", ""] * 2
        + [""] * 12
        + ["hl05:AAAAAAAA|hl09:AAAAAAAA"]
    )
    assert _hilited_local(sl_sem, gr_sem, r)


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
        == _hilited_local(sl_sem, gr_sem, rows[0])
        == _hilited_local(sl_sem.var, gr_sem, rows[0])
    )
    assert (
        True
        == _hilited_local(sl_sem, gr_sem, rows[1])
        == _hilited_local(sl_sem.var, gr_sem, rows[1])
    )


def test_merge_indices():
    rows = [
        [""] * 4
        + ["05/24c01"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τοὺς", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + ["05/24b21", "авраамовоу", "н\ue205ша сѧ• авраа-", "авраамовъ"]
        + [""] * 3
        + ["περὶ", "περί", "περί + Acc.", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl13:FF92D050"],
        [""] * 4
        + ["", "ₓ"] * 2
        + [""] * 3
        + ["τὸν", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + [
            "05/24c01",
            "\ue20dадь",
            "мовоу \ue20dадь г\ue010лю-",
            "\ue20dѧдь",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["Ἀβραὰμ", "Ἀβραάμ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4"],
    ]

    assert _merge_indices(rows).longstr() == "05/024b21-c01"
