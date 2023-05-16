from setup import sl_sem, gr_sem
from hiliting import Hiliting
from grouper import _close_group, _collect_group, _update_group, _hilited_gram

# INFO:root:Събиране на многоредови преводи от славянски основен към гръцки...
raw = [
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


def test_close_raspetou_inverse():
    rows = [r.copy() for r in raw]
    h = Hiliting(rows, gr_sem, sl_sem)
    result = _close_group(rows, gr_sem, sl_sem, h)

    assert result == [
        ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 2
        + ["18/089c21", "пропѧтоу бꙑт\ue205•", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"],
        ["распетоу WG"]
        + [""] * 3
        + [
            "18/89c21-d01",
            "пропѧтоу бꙑт\ue205•",
            "же пропѧтоу бꙑ-",
            "бꙑт\ue205",
            "",
            "gramm.",
            "",
            "σταυρωθῆναι",
            "pass.",
        ]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"],
    ]


def test_collect_raspetou_inverse():
    rows = [r.copy() for r in raw]
    h = Hiliting(rows, gr_sem, sl_sem)
    result = _collect_group(rows, gr_sem, sl_sem, h)

    assert (
        result
        == ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 3
        + ["пропѧтоу бꙑт\ue205•", "", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι"]
        + [""] * 14
    )


def test_update_raspetou_inverse():
    rows = [r.copy() for r in raw]
    h = Hiliting(rows, gr_sem, sl_sem)
    line = (
        ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 3
        + ["пропѧтоу бꙑт\ue205•", "", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι"]
        + [""] * 14
    )

    result = _update_group(rows, gr_sem, sl_sem, line, h)

    assert result == [
        ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 2
        + ["18/089c21", "пропѧтоу бꙑт\ue205•", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"],
        ["распетоу WG"]
        + [""] * 3
        + [
            "18/89c21-d01",
            "пропѧтоу бꙑт\ue205•",
            "же пропѧтоу бꙑ-",
            "бꙑт\ue205",
            "",
            "gramm.",
            "",
            "σταυρωθῆναι",
            "pass.",
        ]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"],
    ]


def test_close_sloves_inverse():
    rows = [
        [""] * 4
        + ["38/178c06"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τῶν", "ὁ"]
        + [""] * 13
        + ["hl11:FFFCD5B4|hl14:FFB8CCE4"],
        [""] * 4
        + ["38/178c06", "словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
        + [""] * 3
        + ["εἰρημένων", "λέγω", "τὸ εἰρημένον"]
        + [""] * 12
        + ["hl11:FFFCD5B4"],
    ]
    h = Hiliting(rows, gr_sem, sl_sem)
    result = _close_group(rows, gr_sem, sl_sem, h)

    assert result == [
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "", "ₓ"]
        + [""] * 3
        + ["τῶν εἰρημένων", "ὁ"]
        + [""] * 13
        + ["hl11:FFFCD5B4|hl14:FFB8CCE4"],
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
        + [""] * 3
        + ["τῶν εἰρημένων", "λέγω", "τὸ εἰρημένον"]
        + [""] * 12
        + ["hl11:FFFCD5B4"],
    ]


def test_collect_sloves_inverse():
    rows = [
        [""] * 5
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τῶν", "ὁ"]
        + [""] * 13
        + ["hl11:FFFCD5B4|hl14:FFB8CCE4"],
        [""] * 4
        + ["38/178c06", "словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
        + [""] * 3
        + ["εἰρημένων", "λέγω", "τὸ εἰρημένον"]
        + [""] * 12
        + ["hl11:FFFCD5B4"],
    ]

    h = Hiliting(rows, gr_sem, sl_sem)

    result = _collect_group(rows, gr_sem, sl_sem, h)

    assert (
        result
        == [""] * 5
        + ["ₓ словесъ", "", "слово"]
        + [""] * 3
        + ["τῶν εἰρημένων", "", "τὸ εἰρημένον"]
        + [""] * 12
    )


def test_update_sloves_inverse():
    rows = [
        [""] * 4
        + ["38/178c06"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τῶν", "ὁ"]
        + [""] * 13
        + ["hl11:FFFCD5B4|hl14:FFB8CCE4"],
        [""] * 4
        + ["38/178c06", "словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
        + [""] * 3
        + ["εἰρημένων", "λέγω", "τὸ εἰρημένον"]
        + [""] * 12
        + ["hl11:FFFCD5B4"],
    ]

    h = Hiliting(rows, gr_sem, sl_sem)
    line = (
        [""] * 5
        + ["ₓ словесъ", "", "слово"]
        + [""] * 3
        + ["τῶν εἰρημένων", "", "τὸ εἰρημένον"]
        + [""] * 12
    )

    result = _update_group(rows, gr_sem, sl_sem, line, h)

    assert result == [
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "", "ₓ"]
        + [""] * 3
        + ["τῶν εἰρημένων", "ὁ"]
        + [""] * 13
        + ["hl11:FFFCD5B4|hl14:FFB8CCE4"],
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
        + [""] * 3
        + ["τῶν εἰρημένων", "λέγω", "τὸ εἰρημένον"]
        + [""] * 12
        + ["hl11:FFFCD5B4"],
    ]


def test_rechi():
    group = [
        ["бꙑше H", "бꙑт\ue205", "", "gramm.", "25/123b05"]
        + ["om.", ""] * 2
        + [""] * 3
        + ["gramm."]
        + [""] * 13
        + ["hl00:FFF8CBAD|hl03:FFBDD7EE"]
        + ["1"] * 4,
        ["рекл\ue205 H"]
        + [""] * 3
        + ["25/123b05", "рѣша", "ко г\ue010лще рѣша• ꙗ-", "рещ\ue205"]
        + [""] * 3
        + ["φασὶν", "φημί"]
        + [""] * 13
        + ["hl00:FFF8CBAD"]
        + ["1"] * 4,
    ]

    h = Hiliting(group, sl_sem, gr_sem)
    res = _close_group(group, sl_sem, gr_sem, h)

    assert res == [
        [
            "бꙑше рекл\ue205 H",
            "бꙑт\ue205",
            "",
            "gramm.",
            "25/123b05",
            "om. рѣша",
            "",
            "om.",
        ]
        + [""] * 3
        + ["φασὶν", "gramm."]
        + [""] * 13
        + ["hl00:FFF8CBAD|hl03:FFBDD7EE"]
        + ["1"] * 4,
        [
            "бꙑше рекл\ue205 H",
            "бꙑт\ue205 H",
            "",
            "",
            "25/123b05",
            "om. рѣша",
            "ко г\ue010лще рѣша• ꙗ-",
            "рещ\ue205",
        ]
        + [""] * 3
        + ["φασὶν", "φημί"]
        + [""] * 13
        + ["hl00:FFF8CBAD"]
        + ["1"] * 4,
    ]


def test_collect_rechi():
    group = [
        ["бꙑше H", "бꙑт\ue205", "", "gramm.", "25/123b05"]
        + ["om.", ""] * 2
        + [""] * 3
        + ["gramm."]
        + [""] * 13
        + ["hl00:FFF8CBAD|hl03:FFBDD7EE"]
        + ["1"] * 4,
        ["рекл\ue205 H", "рещ\ue205"]
        + [""] * 2
        + ["25/123b05", "рѣша", "ко г\ue010лще рѣша• ꙗ-", "рещ\ue205"]
        + [""] * 3
        + ["φασὶν", "φημί"]
        + [""] * 13
        + ["hl00:FFF8CBAD"]
        + ["1"] * 4,
    ]

    h = Hiliting(group, sl_sem, gr_sem)
    res = _collect_group(group, sl_sem, gr_sem, h)

    assert res == (
        [
            "бꙑше рекл\ue205 H",
            "бꙑт\ue205 рещ\ue205 H",
            "",
            "",
            "",
            "om. рѣша",
            "",
            "",
            "",
        ]
        + [""] * 2
        + ["φασὶν", "φημί"]
        + [""] * 13
    )
