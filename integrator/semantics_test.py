from sortedcontainers.sorteddict import SortedDict, SortedSet  # type: ignore
from model import Index, Usage
from semantics import MainLangSemantics, VarLangSemantics


def test_post_init():
    sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    assert len(sem.lemmas) == len(sem.var.lemmas) == 4
    sem = MainLangSemantics("sl", 4, [6, 7], VarLangSemantics("sl", 0, [1, 2, 8, 9]))
    assert len(sem.lemmas) == len(sem.var.lemmas) == 4


def test_LangSemantics_alternatives():
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )

    row = (
        ["ю G", "\ue205 pron.", "", "1/W168b6", "om.", "", "om."]
        + [""] * 3
        + ["ταύτην", "οὗτος"]
        + [""] * 12
    )
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == ("", {"G": "\ue205 pron."})

    row = (
        ([""] * 3)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με C", "ἐγώ"]
        + ([""] * 7)
    )
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == ("", {})
    result == gr_sem.var.alternatives(row, "C")
    # assert result == ("μὲν", {})

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
    result = sl_sem.alternatives(row, "*IGNORED*")
    assert result == ("", {"G": "\ue205но\ue20dѧдъ", "H": "\ue201д\ue205нородъ"})
    result = sl_sem.var.alternatives(row, "G")
    assert result == ("\ue201д\ue205но\ue20dѧдъ", {"H": "\ue201д\ue205нородъ"})
    result = sl_sem.var.alternatives(row, "H")
    assert result == ("\ue201д\ue205но\ue20dѧдъ", {"G": "\ue205но\ue20dѧдъ"})


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


def test_LangSemantics_multilemma():
    # old semantics
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )

    row = (
        ["ю G", "\ue205 pron.", "", "1/W168b6", "om.", "", "om."]
        + [""] * 3
        + ["ταύτην", "οὗτος"]
        + [""] * 12
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

    row = (
        ([""] * 3)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με C", "ἐγώ"]
        + ([""] * 7)
    )
    result = sl_sem.multilemma(row)
    assert result == {"": "аꙁъ"}
    result = gr_sem.var.multilemma(row)
    assert result == {"C": "ἐγώ"}

    dummy_sem = MainLangSemantics("sl", 2, [3], VarLangSemantics("sl", 0, [1]))

    result = dummy_sem.var.multilemma(
        ["ноедаго G  днородоу H", "днородъ H & ноѧдъ G", "", ""]
    )
    assert len(result) == 2
    assert result["H"] == "\ue201д\ue205нородъ"
    assert result["G"] == "\ue205но\ue20dѧдъ"

    result = dummy_sem.var.multilemma(["", "", "", ""])
    assert len(result) == 0

    result = dummy_sem.var.multilemma(
        [
            "дноеды WH Ø G",
            "дноѧдъ",
            "\ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ",
        ]
    )
    assert result == {"WH": "дноѧдъ", "G": "\ue205но\ue20dѧдъ"}

    dummy_sem2 = VarLangSemantics("gr", 0, [1])
    result = dummy_sem2.multilemma(["με C", "ἐγώ"])
    assert result == {"C": "ἐγώ"}

    # semantics update from September 2021
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )

    row = (
        ["\ue201д\ue205но\ue20dеды WH Ø G", "\ue201д\ue205но\ue20dѧдъ"]
        + [""] * 2
        + [
            "1/5a4",
            "\ue205но\ue20dадꙑ\ue205",
            "нъ ꙗко б\ue010ъ• а \ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενὴς", "μονογενής"]
        + [""] * 14
    )
    result = sl_sem.var.multilemma(row)
    assert result == {"WH": "\ue201д\ue205но\ue20dѧдъ", "G": "\ue205но\ue20dѧдъ"}


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


def test_LangSemantics_build_usages_verovat():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт_",
            "",
            "1/7b19",
            "вѣроують",
            "вьс_ вѣроують",
            "вѣроват_",
        ]
        + ([""] * 3)
        + [
            "πιστεύσωσι",
            "πιστεύω",
        ]
        + ([""] * 13)
        + ["hl00"]
    )

    d1 = SortedDict()
    d1 = sl_sem.build_usages(gr_sem, row, d1, "вѣроват_", "πιστεύω")
    assert d1 == SortedDict(
        {
            "πιστεύω": {
                ("вѣроують", "πιστεύσωσι"): SortedSet(
                    [
                        Usage(
                            idx=Index(ch=1, alt=False, page=7, col="b", row=19),
                            lang="sl",
                            orig_alt_var={"GH": "вѣра"},
                        )
                    ]
                )
            }
        }
    )
    d2 = SortedDict()
    d2 = gr_sem.build_usages(sl_sem, row, d2, "πιστεύω", "вѣроват_")
    assert d2 == SortedDict(
        {
            "вѣроват_": {
                ("πιστεύσωσι", "вѣроують"): SortedSet(
                    [
                        Usage(
                            idx=Index(ch=1, alt=False, page=7, col="b", row=19),
                            lang="gr",
                            trans_alt_var={"GH": "вѣра"},
                        )
                    ]
                )
            }
        }
    )


def test_LangSemantics_build_usages_mene():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    row = (
        ([""] * 4)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με C", "ἐγώ"]
        + ([""] * 9)
    )

    d3 = SortedDict()
    d3 = sl_sem.build_usages(gr_sem.var, row, d3, "аꙁъ", "ἐγώ")
    assert d3 == SortedDict(
        {
            "ἐγώ": {
                ("мене", "με"): SortedSet(
                    [
                        Usage(
                            idx=Index.unpack("1/W168c7"),
                            lang="sl",
                            var="C",
                            trans_alt="",
                        )
                    ]
                )
            }
        }
    )
    d4 = SortedDict()
    d4 = gr_sem.var.build_usages(sl_sem, row, d4, "ἐγώ", "аꙁъ")
    assert d4 == SortedDict(
        {
            "аꙁъ": {
                ("με", "мене"): SortedSet(
                    [
                        Usage(
                            idx=Index.unpack("1/W168c7"),
                            lang="gr",
                            var="C",
                            orig_alt="",
                        )
                    ]
                )
            }
        }
    )


def test_LangSemantics_build_usages_monogenis():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    row = (
        ["\ue201д\ue205но\ue20dеды WH Ø G", "\ue201д\ue205но\ue20dѧдъ"]
        + [""] * 2
        + [
            "1/5a4",
            "\ue205но\ue20dадꙑ\ue205",
            "нъ ꙗко б\ue010ъ• а \ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενὴς", "μονογενής"]
        + [""] * 14
    )

    d0 = SortedDict()
    d0 = sl_sem.build_usages(gr_sem, row, d0, "\ue205но\ue20dѧдъ", "μονογενής")
    assert d0 == SortedDict(
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
                            ),
                            lang="sl",
                            orig_alt_var={"WH": "\ue201д\ue205но\ue20dѧдъ"},
                        )
                    ]
                )
            }
        }
    )

    d01 = SortedDict()
    d01 = gr_sem.build_usages(sl_sem, row, d01, "μονογενής", "\ue205но\ue20dѧдъ")
    assert d01 == SortedDict(
        {
            "\ue205но\ue20dѧдъ": {
                ("μονογενὴς", "\ue205но\ue20dадꙑ\ue205"): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=False,
                                page=5,
                                col="a",
                                row=4,
                            ),
                            lang="gr",
                            trans_alt_var={
                                "WH": "\ue201д\ue205но\ue20dѧдъ",
                            },
                        )
                    ]
                )
            }
        }
    )

    d02 = SortedDict()
    d02 = gr_sem.build_usages(sl_sem, row, d02, "μονογενής", "\ue201д\ue205но\ue20dѧдъ")
    print(d02)

    row = (
        [
            "\ue205но\ue20dедаго G  \ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ H / \ue205но\ue20dѧдъ G",
        ]
        + [""] * 2
        + [
            "1/W168a25",
            "\ue201д\ue205но\ue20dедоу",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 13
        + ["bold|italic"]
    )

    d1 = SortedDict()
    d1 = sl_sem.var.build_usages(gr_sem, row, d1, "\ue205но\ue20dѧдъ", "μονογενής")
    # print(d1)
    assert len(d1["μονογενής"]) == 1
    assert len(d1["μονογενής"][("\ue205но\ue20dедаго", "μονογενοῦς")]) == 1
    assert next(iter(d1["μονογενής"][("\ue205но\ue20dедаго", "μονογενοῦς")])) == Usage(
        idx=Index(ch=1, alt=True, page=168, col="a", row=25, bold=True, italic=True),
        lang="sl",
        var="G",
        orig_alt="\ue201д\ue205но\ue20dѧдъ",
        orig_alt_var={"H": "\ue201д\ue205нородъ"},
    )

    d2 = SortedDict()
    d2 = sl_sem.var.build_usages(gr_sem, row, d2, "\ue201д\ue205нородъ", "μονογενής")
    assert len(d2["μονογενής"]) == 1
    assert len(d2["μονογενής"][("\ue201д\ue205нородоу", "μονογενοῦς")]) == 1
    assert next(iter(d2["μονογενής"][("\ue201д\ue205нородоу", "μονογενοῦς")])) == Usage(
        idx=Index(ch=1, alt=True, page=168, col="a", row=25, bold=True, italic=True),
        lang="sl",
        var="H",
        orig_alt="\ue201д\ue205но\ue20dѧдъ",
        orig_alt_var={"G": "\ue205но\ue20dѧдъ"},
    )

    row = (
        [
            "\ue205но\ue20dедаго G  \ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ H / \ue205но\ue20dѧдъ G",
        ]
        + [""] * 2
        + [
            "1/W168a25",
            "\ue201д\ue205но\ue20dедоу",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 14
    )

    d = SortedDict()
    d = sl_sem.var.build_usages(gr_sem, row, d, "\ue205но\ue20dѧдъ", "μονογενής")
    # print(d)
    expected = SortedDict(
        {
            "μονογενής": {
                ("\ue205но\ue20dедаго", "μονογενοῦς"): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                            ),
                            lang="sl",
                            var="G",
                            orig_alt="\ue201д\ue205но\ue20dѧдъ",
                            orig_alt_var={"H": "\ue201д\ue205нородъ"},
                            trans_alt="",
                            trans_alt_var={},
                        )
                    ]
                )
            }
        }
    )
    assert d == expected

    d = SortedDict()
    d = sl_sem.var.build_usages(gr_sem, row, d, "\ue201д\ue205нородъ", "μονογενής")
    expected = SortedDict(
        {
            "μονογενής": {
                ("\ue201д\ue205нородоу", "μονογενοῦς"): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                            ),
                            lang="sl",
                            var="H",
                            orig_alt="\ue201д\ue205но\ue20dѧдъ",
                            orig_alt_var={"G": "\ue205но\ue20dѧдъ"},
                            trans_alt="",
                            trans_alt_var={},
                        )
                    ]
                )
            }
        }
    )
    assert d == expected

    d = SortedDict()
    d = gr_sem.build_usages(sl_sem, row, d, "μονογενής", "\ue201д\ue205но\ue20dѧдъ")
    expected = SortedDict(
        {
            "\ue201д\ue205но\ue20dѧдъ": {
                ("μονογενοῦς", "\ue201д\ue205но\ue20dедоу"): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                            ),
                            lang="gr",
                            var="",
                            orig_alt="",
                            orig_alt_var={},
                            trans_alt="",
                            trans_alt_var={
                                "H": "\ue201д\ue205нородъ",
                                "G": "\ue205но\ue20dѧдъ",
                            },
                        )
                    ]
                )
            }
        }
    )
    assert d == expected

    d = SortedDict()
    d = gr_sem.build_usages(sl_sem.var, row, d, "μονογενής", "\ue201д\ue205нородъ")
    expected = SortedDict(
        {
            "\ue201д\ue205нородъ": {
                ("μονογενοῦς", "\ue201д\ue205нородоу"): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                var=False,
                                end=None,
                                bold=False,
                                italic=False,
                            ),
                            lang="gr",
                            var="H",
                            orig_alt="",
                            orig_alt_var={},
                            trans_alt="\ue201д\ue205но\ue20dѧдъ",
                            trans_alt_var={"G": "\ue205но\ue20dѧдъ"},
                        )
                    ]
                ),
            },
        }
    )
    assert d == expected

    d = SortedDict()
    d = gr_sem.build_usages(sl_sem.var, row, d, "μονογενής", "\ue205но\ue20dѧдъ")
    expected = SortedDict(
        {
            "\ue205но\ue20dѧдъ": {
                ("μονογενοῦς", "\ue205но\ue20dедаго"): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                var=False,
                                end=None,
                                bold=False,
                                italic=False,
                            ),
                            lang="gr",
                            var="G",
                            orig_alt="",
                            orig_alt_var={},
                            trans_alt="\ue201д\ue205но\ue20dѧдъ",
                            trans_alt_var={"H": "\ue201д\ue205нородъ"},
                        )
                    ]
                ),
            },
        }
    )
    assert d == expected


def test_build_paths():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    res = sl_sem.build_paths([""] * 7 + ["боудеть", "бꙑт\ue205 ", "", "gram."])
    assert res == ["бꙑт\ue205 → боудеть gram."]

    res = sl_sem.build_paths([""] * 7 + ["едно", "две", "три", "четири"])
    assert res == ["четири → три → две → едно"]

    res = sl_sem.build_paths([""] * 7 + ["едно", "две", "три", "gram."])
    assert res == ["три → две → едно gram."]

    res = sl_sem.build_paths(
        [""] * 4
        + ["1/4b17"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["ὁ", "ὁ"]
        + [""] * 13
        + ["bold|italic"]
    )
    assert res == ["ₓ"]

    row = (
        [
            "\ue205но\ue20dедаго G  \ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ H / \ue205но\ue20dѧдъ G",
        ]
        + [""] * 2
        + [
            "1/W168a25",
            "\ue201д\ue205но\ue20dедоу",
            "вргь(!) г\ue010ле• славоу ꙗко \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενοῦς", "μονογενής"]
        + [""] * 13
        + ["bold|italic"]
    )
    res = sl_sem.var.build_paths(row)
    assert res == ["\ue201д\ue205нородъ", "\ue205но\ue20dѧдъ"]
