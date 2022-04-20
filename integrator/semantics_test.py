from sortedcontainers.sorteddict import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL
from model import Alternative, Index, Path, Source, Usage
from semantics import MainLangSemantics, VarLangSemantics
from semantics import _is_variant_lemma, _add_usage
from setup import sl_sem, gr_sem


def test_post_init():
    sem = MainLangSemantics(
        FROM_LANG, 4, [6, 7, 8, 9], VarLangSemantics(FROM_LANG, 0, [1, 2])
    )
    assert len(sem.lemmas) == len(sem.var.lemmas) == 4
    sem = MainLangSemantics(
        FROM_LANG, 4, [6, 7], VarLangSemantics(FROM_LANG, 0, [1, 2, 8, 9])
    )
    assert len(sem.lemmas) == len(sem.var.lemmas) == 4


def test__is_variant_lemma():
    row = (
        [""] * 4
        + [
            "1/W168c17",
            "прѣ\ue205сто\ue20dе",
            "всѣмь прѣ\ue205сто\ue20dе\ue201• \ue205 по \ue205сто\ue20dен\ue205\ue205",
            "прѣ\ue205сто\ue20d\ue205т\ue205",
        ]
        + [""] * 3
        + ["ὑπερκλύζων", "ὑπερκλύζω"]
        + [""] * 3
        + ["ὑπερβλύζων C", "ὑπερβλύω"]
        + [""] * 9
    )
    exception = False
    try:
        _is_variant_lemma(row, gr_sem, Source("C"), "ὑπερκλύζω")
    except AssertionError:
        exception = True
    assert exception

    assert _is_variant_lemma(row, gr_sem, Source(""), "ὑπερκλύζω")
    assert _is_variant_lemma(row, gr_sem.var, Source("C"), "ὑπερβλύω")

    assert not _is_variant_lemma(row, gr_sem.var, Source("D"), "ὑπερβλύω")

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
    assert _is_variant_lemma(row, sl_sem.var, Source("HW"), "\ue201д\ue205но\ue20dѧдъ")
    assert not _is_variant_lemma(
        row, sl_sem.var, Source("G"), "\ue201д\ue205но\ue20dѧдъ"
    )
    assert not _is_variant_lemma(row, sl_sem.var, Source("G"), "\ue205но\ue20dѧдъ")
    assert _is_variant_lemma(row, sl_sem, Source(""), "\ue205но\ue20dѧдъ")
    assert _is_variant_lemma(row, gr_sem, Source(""), "μονογενής")
    assert not _is_variant_lemma(row, gr_sem.var, Source(""), "μονογενής")


def test_is_variant_lemma_bozhii():
    row = (
        ["б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H", "бож\ue205\ue205"]
        + [""] * 2
        + ["1/7a4", "боꙁѣ", "о боꙁѣ словес\ue205•", "богъ", "Dat."]
        + [""] * 2
        + ["Θεοῦ", "θεός", "Gen."]
        + [""] * 13
    )
    assert _is_variant_lemma(row, sl_sem.var, Source("W"), "бож\ue205\ue205")


def test_build_paths():
    res = sl_sem.build_paths([""] * 7 + ["боудеть", "бꙑт\ue205 ", "", "gram."])
    res = [str(r) for r in res]
    assert res == ["бꙑт\ue205 → боудеть gram."]

    res = sl_sem.build_paths([""] * 7 + ["едно", "две", "три", "четири"])
    res = [str(r) for r in res]
    assert res == ["четири → три → две → едно"]

    res = sl_sem.build_paths([""] * 7 + ["едно", "две", "три", "gram."])
    res = [str(r) for r in res]
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
    res = [str(r) for r in res]
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
    res = [str(r) for r in res]
    assert res == ["\ue201д\ue205нородъ", "\ue205но\ue20dѧдъ"]

    row = (
        [""] * 4
        + ["1/8a13"]
        + ["Instr.", ""] * 2
        + [""] * 2
        + ["παρὰ", "παρά", "παρά + Acc."]
        + [""] * 13
    )
    res = sl_sem.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["Instr."]

    res = gr_sem.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["παρά + Acc. → παρά"]

    assert not gr_sem.var.build_paths(row)[0]
    assert not sl_sem.var.build_paths(row)[0]

    row = (
        ["вь WGH", "въ", "въ + Loc.", "", "1/7d1", "оу", "оу насъ", "ѹ"]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["παρ’ C", "παρά", "παρά + Acc."]
        + [""] * 8
    )
    res = sl_sem.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["ѹ"]

    res = sl_sem.var.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["въ + Loc. → въ"]

    res = gr_sem.build_paths(row)
    res = [str(r) for r in res]
    assert res == [""]

    res = gr_sem.var.build_paths(row)
    res = [str(r) for r in res]
    assert res == ["παρά + Acc. → παρά"]


def test_build_paths_special():
    row = (
        ["свѣть WH"]
        + [""] * 3
        + ["1/6c8", "всѣмъ", "всѣмъ \ue20dл\ue010вкомъ•", "вьсь", "≈ вьсѣмъ"]
        + [""] * 2
        + ["καθόλου", "καθόλου"]
        + [""] * 14
    )
    res = sl_sem.build_paths(row)
    assert [str(p) for p in res] == ["≈ вьсѣмъ → вьсь"]
    assert res == [Path(parts=["вьсь", "≈ вьсѣмъ"])]

    row = (
        [""] * 4
        + [
            "1/4b16",
            "на\ue20dатъ",
            "семоу на\ue20dатъ",
            "на\ue20dѧт\ue205",
            "≠ на\ue20dѧт\ue205",
        ]
        + [""] * 2
        + ["ᾐνίξατο", "αἰνίσσομαι"]
        + [""] * 14
    )
    res = sl_sem.build_paths(row)
    assert [str(p) for p in res] == ["≠ на\ue20dѧт\ue205"]
    assert res == [Path(parts=["на\ue20dѧт\ue205", "≠ на\ue20dѧт\ue205"])]


def test_add_usage():
    usages = [
        Usage(
            idx=Index(
                ch=1,
                alt=True,
                page=168,
                col="a",
                row=25,
                word="μονογενοῦς",
            ),
            lang=TO_LANG,
            var="G",
            trans_alt=Alternative(
                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                var_lemmas={"H": "\ue201д\ue205нородъ"},
            ),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=False,
                page=5,
                col="a",
                row=4,
                word="μονογενὴς",
            ),
            lang=TO_LANG,
            trans_alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=False,
                page=4,
                col="c",
                row=15,
                word="μονογενοῦς",
            ),
            lang=TO_LANG,
            trans_alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=True,
                page=168,
                col="a",
                row=25,
                word="μονογενοῦς",
            ),
            lang=TO_LANG,
            var="H",
            trans_alt=Alternative(
                main_lemma="\ue201д\ue205но\ue20dѧдъ",
                var_lemmas={"G": "\ue205но\ue20dѧдъ"},
            ),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=True,
                page=168,
                col="a",
                row=28,
                word="μονογενοῦς",
            ),
            lang=TO_LANG,
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=True,
                page=168,
                col="a",
                row=25,
                word="μονογενοῦς",
            ),
            lang=TO_LANG,
            trans_alt=Alternative(
                var_lemmas={
                    "H": "\ue201д\ue205нородъ",
                    "G": "\ue205но\ue20dѧдъ",
                }
            ),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=False,
                page=5,
                col="a",
                row=4,
                word="μονογενὴς",
            ),
            lang=TO_LANG,
            var="WH",
            trans_alt=Alternative(main_lemma="\ue205но\ue20dѧдъ "),
        ),
        Usage(
            idx=Index(
                ch=1,
                alt=False,
                page=4,
                col="c",
                row=15,
                word="μονογενοῦς",
            ),
            lang=TO_LANG,
            var="WH",
            trans_alt=Alternative(main_lemma="\ue205но\ue20dѧдъ"),
        ),
    ]

    d = SortedDict()
    for u in usages:
        _add_usage(u, "", ("", ""), d)
    assert d == SortedDict(
        {
            "": {
                ("", ""): SortedSet(
                    [
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=False,
                                page=4,
                                col="c",
                                row=15,
                                word="μονογενοῦς",
                            ),
                            lang=TO_LANG,
                            trans_alt=Alternative(
                                var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}
                            ),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=False,
                                page=4,
                                col="c",
                                row=15,
                                word="μονογενοῦς",
                            ),
                            lang=TO_LANG,
                            var="WH",
                            trans_alt=Alternative(main_lemma="\ue205но\ue20dѧдъ"),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=False,
                                page=5,
                                col="a",
                                row=4,
                                word="μονογενὴς",
                            ),
                            lang=TO_LANG,
                            trans_alt=Alternative(
                                var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}
                            ),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=False,
                                page=5,
                                col="a",
                                row=4,
                                word="μονογενὴς",
                            ),
                            lang=TO_LANG,
                            var="WH",
                            trans_alt=Alternative(main_lemma="\ue205но\ue20dѧдъ "),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                word="μονογενοῦς",
                            ),
                            lang=TO_LANG,
                            trans_alt=Alternative(
                                var_lemmas={
                                    "H": "\ue201д\ue205нородъ",
                                    "G": "\ue205но\ue20dѧдъ",
                                }
                            ),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=28,
                                word="μονογενοῦς",
                            ),
                            lang=TO_LANG,
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                word="μονογενοῦς",
                            ),
                            lang=TO_LANG,
                            var="G",
                            trans_alt=Alternative(
                                "\ue201д\ue205но\ue20dѧдъ",
                                var_lemmas={"H": "\ue201д\ue205нородъ"},
                            ),
                        ),
                        Usage(
                            idx=Index(
                                ch=1,
                                alt=True,
                                page=168,
                                col="a",
                                row=25,
                                word="μονογενοῦς",
                            ),
                            lang=TO_LANG,
                            var="H",
                            trans_alt=Alternative(
                                "\ue201д\ue205но\ue20dѧдъ",
                                var_lemmas={"G": "\ue205но\ue20dѧдъ"},
                            ),
                        ),
                    ]
                )
            }
        }
    )


def test_LangSemantics_compile_words_by_lemma():
    sl_sem = MainLangSemantics(
        FROM_LANG,
        5,
        [7, 8, 9, 10],
        VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 1),
    )
    row = (
        ["б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H", "бож\ue205\ue205"]
        + [""] * 2
        + ["1/7a4", "боꙁѣ", "о боꙁѣ словес\ue205•", "богъ", "Dat."]
        + [""] * 2
        + ["Θεοῦ", "θεός", "Gen."]
        + [""] * 13
        + ["1"]
    )

    result = sl_sem.var.compile_words_by_lemma(row, "WGH")
    assert result == ("б\ue010жї\ue205 H б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G", 1)

    row = (
        ["ѿ WG  ѡ H", "отъ"]
        + [""] * 2
        + ["1/5d11"]
        + ["om.", ""] * 2
        + [""] * 2
        + ["ἐπὶ", "ἐπί", "ἐπί + Gen."]
        + [""] * 13
        + ["1"]
    )

    result = sl_sem.var.compile_words_by_lemma(row, "WGH")
    assert result == ("ѡ H ѿ WG", 1)

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
        + ["2"]
    )
    result = sl_sem.var.compile_words_by_lemma(row, "H")
    assert result == ("днородоу H", 2)


def test_add_count():
    sem = MainLangSemantics(FROM_LANG, 5, [], VarLangSemantics(FROM_LANG, 0, []))
    counts = {}
    rows = [[""] * 5 + ["om."], [""] * 4 + ["1/1a1", "om."]]
    for r in rows:
        counts = sem.add_count(r, counts)
    assert not counts
    assert rows == [[""] * 5 + ["om.", "1"], [""] * 4 + ["1/1a1", "om.", "1"]]

    counts = {}
    rows = [["om."], ["om."], ["om."]]
    for r in rows:
        counts = sem.var.add_count(r, counts)
    assert not counts
    assert rows == [["om.", "1"], ["om.", "1"], ["om.", "1"]]

    counts = {}
    rows = [["om. WH"], ["om. WH"], ["om. WH"]]
    for r in rows:
        counts = sem.var.add_count(r, counts)
    assert not counts
    assert rows == [["om. WH", "1"], ["om. WH", "1"], ["om. WH", "1"]]


def test_compile_words_by_lemma_artos():
    gr_sem = MainLangSemantics(
        TO_LANG,
        11,
        [12, 13, 14],
        VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20], cnt_col=STYLE_COL + 1),
    )
    row = (
        [""] * 4
        + ["16/80a08", "хлѣбꙑ•", "ре\ue20dе хлѣбꙑ• не", "хлѣбъ"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 3
        + ["ἄρτους Ch", "ἄρτος"]
        + [""] * 9
        + ["1"] * 4
    )
    res = gr_sem.var.compile_words_by_lemma(row, Source("Ch"))
    assert res == ("ἄρτους Ch", 1)
