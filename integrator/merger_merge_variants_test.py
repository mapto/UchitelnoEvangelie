from const import IDX_COL
from setup import sl_sem, gr_sem
from merger import merge, _close, _close_group

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


def test_raspetou():
    rows = [r for r in raw]
    result = merge(rows, sl_sem, gr_sem)

    assert result == [
        ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 2
        + ["18/089c21", "пропѧтоу бꙑт\ue205•", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"]
        + ["1"] * 4,
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
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"]
        + ["1"] * 4,
    ]


def test_raspetou_var():
    rows = [r for r in raw]
    result = merge(rows, sl_sem.var, gr_sem)

    assert result == [
        ["распетоу WG", "распѧт\ue205"]
        + [""] * 2
        + ["18/089c21", "пропѧтоу бꙑт\ue205•", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"]
        + ["1"] * 4,
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
        + ["hl05:FFFCD5B4|hl08:FFFFFFFF|hl09:FFB8CCE4"]
        + ["1"] * 4,
    ]
