from sortedcontainers.sorteddict import SortedDict  # type: ignore
from model import MainLangSemantics, VarLangSemantics


def test_MainLangSemantics_alternatives():
    row = (
        ["ю G", "\ue205 pron.", "", "1/W168b6", "om.", "", "om."]
        + [""] * 3
        + ["ταύτην", "οὗτος"]
        + [""] * 12
    )
    sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    result = sem.alternatives(row, "*IGNORED*")
    assert result == ("", {"": "\ue205 pron."})


def test_VarLangSemantics_multilemma():
    row = (
        ["ю G", "\ue205 pron.", "", "1/W168b6", "om.", "", "om."]
        + [""] * 3
        + ["ταύτην", "οὗτος"]
        + [""] * 12
    )
    sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    result = sem.var.multilemma(row)
    assert result == {"": "\ue205 pron."}


def test_LangSemantics_build_keys():
    row = (
        [
            "\ue201д\ue205но\ue20dеды WH Ø G",
            "\ue201д\ue205но\ue20dѧдъ",
            "",
            "1/5a4",
            "\ue205но\ue20dадꙑ\ue205",
            "нъ ꙗко б\ue010ъ• а \ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ ",
        ]
        + [""] * 3
        + ["μονογενὴς", "μονογενής"]
        + [""] * 12
    )

    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    sl_sem.var.main = sl_sem
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )
    gr_sem.var.main = gr_sem

    assert sl_sem.build_keys(row) == ["\ue205но\ue20dадꙑ\ue205"]
    assert gr_sem.build_keys(row) == ["μονογενὴς"]
    assert sl_sem.var.build_keys(row) == ["\ue201д\ue205но\ue20dеды", "Ø"]
    assert gr_sem.var.build_keys(row) == [""]


def test_LangSemantics_build_usages():
    row = (
        [
            "\ue201д\ue205но\ue20dеды WH Ø G",
            "\ue201д\ue205но\ue20dѧдъ",
            "",
            "1/5a4",
            "\ue205но\ue20dадꙑ\ue205",
            "нъ ꙗко б\ue010ъ• а \ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ ",
        ]
        + [""] * 3
        + ["μονογενὴς", "μονογενής"]
        + [""] * 12
    )

    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    sl_sem.var.main = sl_sem
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )
    gr_sem.var.main = gr_sem

    d = SortedDict()

    d = sl_sem.build_usages(gr_sem, row, d)

    assert len(d) == 1
    assert len(d["μονογενής"]) == 1
    assert len(d["μονογενής"][("\ue205но\ue20dадꙑ\ue205", "μονογενὴς")]) == 1
    first = next(iter(d["μονογενής"][("\ue205но\ue20dадꙑ\ue205", "μονογενὴς")]))
    assert str(first.idx) == "1/5a4"
    assert first.orig_alt_var == {"": "\ue201д\ue205но\ue20dѧдъ"}

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
        + ([""] * 3)
        + ["τοῦτο", "οὗτος",]
        + ([""] * 11)
        + ["hl04|hl00|hl10"]
    )

    assert ["сел\ue205ко"] == sl_sem.build_keys(row)
    assert ["\ue201л\ue205ко"] == sl_sem.var.build_keys(row)
