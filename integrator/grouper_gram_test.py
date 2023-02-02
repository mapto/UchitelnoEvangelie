from setup import sl_sem, gr_sem
from setup import sl_sem, gr_sem
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
    result = _close_group(rows, gr_sem, sl_sem)

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


def test_hilited_gram():
    rows = [r.copy() for r in raw]

    merge_rows_main = [
        i for i, r in enumerate(rows) if not _hilited_gram(gr_sem, sl_sem, r)
    ]
    assert merge_rows_main == [0]

    merge_rows_var = [
        i for i, r in enumerate(rows) if not _hilited_gram(gr_sem, sl_sem.var, r)
    ]
    assert merge_rows_var == [0]


def test_collect_raspetou_inverse():
    rows = [r.copy() for r in raw]
    merge_rows_main = [0]
    merge_rows_var = [0]

    result = _collect_group(rows, gr_sem, sl_sem, merge_rows_main, merge_rows_var)

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
    merge_rows_main = [0]
    merge_rows_var = [0]
    line = (
        ["распетоу WG", "распѧт\ue205 WG"]
        + [""] * 3
        + ["пропѧтоу бꙑт\ue205•", "", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι"]
        + [""] * 14
    )

    result = _update_group(rows, gr_sem, sl_sem, line, merge_rows_main, merge_rows_var)

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
