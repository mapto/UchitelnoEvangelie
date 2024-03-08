from setup import sl_sem, gr_sem
from merger import merge


def test_vrah():
    row = (
        ["тврьдь G  врагь H"]
        + [""] * 3
        + [
            "1/W168a25",
            "вргь(!)",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "врьхъ",
            "*",
            "",
            "",
            "κορυφὴν",
            "κορυφός",
        ]
        + [""] * 14
    )
    result = merge([row], gr_sem, sl_sem)

    assert result == [
        ["тврьдь G  врагь H"]
        + [""] * 3
        + [
            "1/W168a25",
            "вргь(!)",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "врьхъ",
            "*",
            "",
            "",
            "κορυφὴν",
            "κορυφός",
        ]
        + [""] * 14
        + ["1"] * 4
    ]
