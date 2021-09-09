import re

from const import STYLE_COL

from model import Index, Usage
from semantics import TableSemantics, MainLangSemantics, VarLangSemantics
from aggregator import (
    present,
    _build_usages,
    _multilemma,
    _agg_lemma,
    aggregate,
)
from sortedcontainers import SortedDict, SortedSet  # type: ignore


def test_present():
    sem = VarLangSemantics(lang="sl", word=0, lemmas=[1, 2, 19, 20])
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "1/7b19",
            "вѣроують",
            "вьс\ue205 вѣроують",
            "вѣроват\ue205",
        ]
        + ([""] * 3)
        + ["πιστεύσωσι", "πιστεύω"]
        + ([""] * 11)
        + ["hl00"]
    )
    assert present(row, sem)
    row = ["\ue205моуть GH", "ѩт\ue205", "", "1/7b19"] + ([""] * 18) + ["hl00"]
    assert present(row, sem)
    row = ["\ue205моуть GH", "", "", "1/7b19"] + ([""] * 18) + ["hl00"]
    assert not present(row, sem)

    sem = VarLangSemantics(lang="gr", word=15, lemmas=[16, 17, 19])
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "1/7b19",
            "вѣроують",
            "вьс\ue205 вѣроують",
            "вѣроват\ue205",
        ]
        + ([""] * 3)
        + [
            "πιστεύσωσι",
            "πιστεύω",
        ]
        + ([""] * 11)
        + ["hl00"]
    )
    assert not present(row, sem)
    row = ["\ue205моуть GH", "ѩт\ue205", "", "1/7b19"] + ([""] * 18) + ["hl00"]
    assert not present(row, sem)

    row = (
        ([""] * 3)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με C", "ἐγώ"]
        + ([""] * 7)
    )
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )
    assert not present(row, sl_sem.var)
    assert present(row, sl_sem)
    assert not present(row, gr_sem)
    assert present(row, gr_sem.var)


def test__build_usages():
    sl_sem = MainLangSemantics("sl", 4, [6, 7, 8, 9], VarLangSemantics("sl", 0, [1, 2]))
    sl_sem.var.main = sl_sem
    assert sl_sem.var  # for mypy
    gr_sem = MainLangSemantics(
        "gr", 10, [11, 12, 13], VarLangSemantics("gr", 15, [16, 17])
    )
    gr_sem.var.main = gr_sem
    assert gr_sem.var  # for mypy
    sem = TableSemantics(sl_sem, gr_sem)

    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт_",
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
        + ([""] * 11)
        + ["hl00"]
    )

    d1 = SortedDict()
    d1 = _build_usages(row, sem.sl, sem.gr, d1, "вѣроват_", "πιστεύω")
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
    d2 = _build_usages(row, sem.gr, sem.sl, d2, "πιστεύω", "вѣроват_")
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

    row = (
        ([""] * 3)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με C", "ἐγώ"]
        + ([""] * 7)
    )
    """
    d3 = SortedDict()
    d3 = _build_usages(row, sem.sl, sem.gr, d3, "аꙁъ", "ἐγώ")
    assert d3 == SortedDict(
        {
            "ἐγώ": {
                ("мене",  "με"): SortedSet(
                    [
                        Usage(
                            idx=Index.unpack("1/W168c7"),
                            lang="sl",
                            trans_alt=""
                        )
                    ]
                )
            }
        }
    )
    d4 = SortedDict()
    d4 = _build_usages(row, sem.gr, sem.sl, d4, "ἐγώ", "аꙁъ")
    assert d4 == SortedDict(
        {
            "аꙁъ": {
                ("με", "мене"): SortedSet(
                    [
                        Usage(idx=Index.unpack("1/W168c7"), lang="gr", orig_alt="")
                    ]
                )
            }
        }
    )
    """


def test__multilemma():
    sem = VarLangSemantics("sl", 0, [1])

    result = _multilemma(["ноедаго G  днородоу H", "днородъ H & ноѧдъ G"], sem)
    assert len(result) == 2
    assert result["H"] == "\ue201д\ue205нородъ"
    assert result["G"] == "\ue205но\ue20dѧдъ"

    result = _multilemma(["", ""], sem)
    assert len(result) == 0

    result = _multilemma(["дноеды WH Ø G", "дноѧдъ"], sem)
    assert result == {"WH": "дноѧдъ"}

    gr_sem = VarLangSemantics("gr", 0, [1])
    result = _multilemma(["με C", "ἐγώ"], gr_sem)
    assert result == {"C": "ἐγώ"}


def test__agg_lemma():
    row = [""] * STYLE_COL
    sem = VarLangSemantics(lang="sl_var", word=0, lemmas=[1, 2, 19, 20])
    d = SortedDict()

    result = _agg_lemma(row, None, sem, d)
    assert len(result) == 0

    result = _agg_lemma(row, sem, None, d)
    assert len(result) == 0


def test_aggregate():
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
        + [""] * 12
    )
    sl_sem = MainLangSemantics("sl", 4, [6], VarLangSemantics("sl", 0, [1]))
    gr_sem = MainLangSemantics("gr", 10, [11], VarLangSemantics("gr", 15, [16, 17]))
    result = aggregate([row], sl_sem, gr_sem)

    assert result == SortedDict(
        {
            "\ue205но\ue20dѧдъ": SortedDict(
                {
                    "μονογενής": {
                        ("\ue205но\ue20dедаго", "μονογενοῦς"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1, alt=True, page=168, col="a", row=25
                                    ),
                                    lang="sl",
                                    var="G",
                                    orig_alt="\ue201д\ue205но\ue20dѧдъ",
                                    orig_alt_var={"H": "\ue201д\ue205нородъ"},
                                )
                            ]
                        ),
                    }
                }
            ),
            "\ue201д\ue205нородъ": SortedDict(
                {
                    "μονογενής": {
                        ("\ue201д\ue205нородоу", "μονογενοῦς"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1, alt=True, page=168, col="a", row=25
                                    ),
                                    lang="sl",
                                    var="H",
                                    orig_alt="\ue201д\ue205но\ue20dѧдъ",
                                    orig_alt_var={"G": "\ue205но\ue20dѧдъ"},
                                )
                            ]
                        ),
                    }
                }
            ),
            "\ue201д\ue205но\ue20dѧдъ": SortedDict(
                {
                    "μονογενής": {
                        ("\ue201д\ue205но\ue20dедоу", "μονογενοῦς"): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1, alt=True, page=168, col="a", row=25
                                    ),
                                    lang="sl",
                                    var="",
                                    orig_alt="",
                                    orig_alt_var={
                                        "H": "\ue201д\ue205нородъ",
                                        "G": "\ue205но\ue20dѧдъ",
                                    },
                                )
                            ]
                        )
                    }
                }
            ),
        }
    )
