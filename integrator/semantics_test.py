from sortedcontainers.sorteddict import SortedDict, SortedSet  # type: ignore
from model import Index, Usage
from semantics import MainLangSemantics, VarLangSemantics


def test_post_init():
    sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    assert len(sem.lemmas) == len(sem.var.lemmas) == 4
    sem = MainLangSemantics("sl", 4, [6, 7], VarLangSemantics("sl", 0, [1, 2, 8, 9]))
    assert len(sem.lemmas) == len(sem.var.lemmas) == 4


def test_MainLangSemantics_alternatives():
    row = (
        ["ю G", "\ue205 pron.", "", "1/W168b6", "om.", "", "om."]
        + [""] * 3
        + ["ταύτην", "οὗτος"]
        + [""] * 12
    )
    sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    result = sem.alternatives(row, "*IGNORED*")
    assert result == ("", {"G": "\ue205 pron."})


def test_VarLangSemantics_multiword():
    sem = VarLangSemantics("sl", 0, [1])
    result = sem.multiword(["ноедаго G  днородоу H", "днородъ H / ноѧдъ G"])
    assert len(result) == 2
    assert result["G"] == "\ue205но\ue20dедаго"
    assert result["H"] == "\ue201д\ue205нородоу"

    result = sem.multiword(["ноедаго G", "днородъ H / ноѧдъ G"])
    assert result == {"G": "\ue205но\ue20dедаго"}

    result = sem.multiword(["", ""])
    assert result == {"WGH": ""}

    result = sem.multiword(["дноеды WH Ø G", "дноѧдъ"])
    assert result == {"WH": "дноеды", "G": "Ø"}

    result = sem.multiword(["дноеды", "дноѧдъ"])
    assert result == {"WGH": "дноеды"}

    gr_sem = VarLangSemantics("gr", 0, [1])
    result = gr_sem.multiword(["με C", "ἐγώ"])
    assert result == {"C": "με"}


def test_VarLangSemantics_multilemma():
    row = (
        ["ю G", "\ue205 pron.", "", "1/W168b6", "om.", "", "om."]
        + [""] * 3
        + ["ταύτην", "οὗτος"]
        + [""] * 12
    )
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )
    result = sl_sem.var.multilemma(row)
    assert result == {"G": "\ue205 pron."}

    row = (
        ["вь WGH", "въ", "въ + Loc.", "1/7d1", "оу", "оу насъ", "ѹ"]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["παρ’ C", "παρά ", "παρά + Acc."]
        + [""] * 6
    )
    result = sl_sem.var.multilemma(row)
    assert result == {"WGH": "въ"}
    result = gr_sem.var.multilemma(row)
    assert result == {"C": "παρά"}


def test_LangSemantics_build_keys():
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )

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

    assert sl_sem.build_keys(row) == ["\ue205но\ue20dадꙑ\ue205"]
    assert gr_sem.build_keys(row) == ["μονογενὴς"]
    assert sl_sem.var.build_keys(row) == ["\ue201д\ue205но\ue20dеды", "Ø"]
    assert gr_sem.var.build_keys(row) == [""]

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
        + [
            "τοῦτο",
            "οὗτος",
        ]
        + ([""] * 11)
        + ["hl04|hl00|hl10"]
    )

    assert ["сел\ue205ко"] == sl_sem.build_keys(row)
    assert ["\ue201л\ue205ко"] == sl_sem.var.build_keys(row)


def test_LangSemantics_build_usages():
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )

    row = (
        [
            "\ue201д\ue205но\ue20dеды WH Ø G",
            "\ue201д\ue205но\ue20dѧдъ",
            "",
            "1/5a4",
            "\ue205но\ue20dадꙑ\ue205",
            "нъ ꙗко б\ue010ъ• а \ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενὴς", "μονογενής"]
        + [""] * 12
    )

    d = SortedDict()
    d = sl_sem.build_usages(gr_sem, row, d, "\ue205но\ue20dѧдъ")

    assert d == SortedDict(
        {
            "μονογενής": {
                ("\ue205но\ue20dадꙑ\ue205", "μονογενὴς"): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=False,
                                page=5,
                                col="a",
                                row=4,
                                var=False,
                                end=None,
                                bold=False,
                                italic=False,
                            ),
                            lang="sl",
                            var="",
                            orig_alt="",
                            orig_alt_var={"WH": "\ue201д\ue205но\ue20dѧдъ"},
                            trans_alt="",
                            trans_alt_var={},
                        )
                    ]
                )
            }
        }
    )

    row = (
        [
            "\ue205но\ue20dедаго G  \ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ H / \ue205но\ue20dѧдъ G",
            "",
            "1/W168a25",
            "\ue201д\ue205но\ue20dедоу",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 11
        + ["bold|italic"]
    )

    d = SortedDict()
    d = sl_sem.var.build_usages(gr_sem, row, d, "\ue205но\ue20dѧдъ")
    assert len(d["μονογενής"]) == 1
    assert len(d["μονογενής"][("\ue205но\ue20dедаго", "μονογενοῦς")]) == 1
    assert next(iter(d["μονογενής"][("\ue205но\ue20dедаго", "μονογενοῦς")])) == Usage(
        idx=Index(ch=1, alt=True, page=168, col="a", row=25, bold=True, italic=True),
        lang="sl",
        var="G",
        orig_alt="\ue201д\ue205но\ue20dѧдъ",
        orig_alt_var={"H": "\ue201д\ue205нородъ"},
    )

    d = SortedDict()
    d = sl_sem.var.build_usages(gr_sem, row, d, "\ue201д\ue205нородъ")
    assert len(d["μονογενής"]) == 1
    assert len(d["μονογενής"][("\ue201д\ue205нородоу", "μονογενοῦς")]) == 1
    assert next(iter(d["μονογενής"][("\ue201д\ue205нородоу", "μονογενοῦς")])) == Usage(
        idx=Index(ch=1, alt=True, page=168, col="a", row=25, bold=True, italic=True),
        lang="sl",
        var="H",
        orig_alt="\ue201д\ue205но\ue20dѧдъ",
        orig_alt_var={"G": "\ue205но\ue20dѧдъ"},
    )


def test_build_paths():
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    res = sl_sem.build_paths([""] * 6 + ["боудеть", "бꙑт\ue205 ", "", "gram."])
    assert res == ["бꙑт\ue205 → боудеть gram."]

    res = sl_sem.build_paths([""] * 6 + ["едно", "две", "три", "четири"])
    assert res == ["четири → три → две → едно"]

    res = sl_sem.build_paths([""] * 6 + ["едно", "две", "три", "gram."])
    assert res == ["три → две → едно gram."]

    res = sl_sem.build_paths(
        [""] * 3
        + ["1/4b17"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["ὁ", "ὁ"]
        + [""] * 11
        + ["bold|italic"]
    )
    assert res == ["ₓ"]

    row = (
        [
            "\ue205но\ue20dедаго G  \ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ H / \ue205но\ue20dѧдъ G",
            "",
            "1/W168a25",
            "\ue201д\ue205но\ue20dедоу",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 11
        + ["bold|italic"]
    )
    res = sl_sem.var.build_paths(row)
    assert res == ["\ue201д\ue205нородъ", "\ue205но\ue20dѧдъ"]
