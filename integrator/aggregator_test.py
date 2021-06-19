import re

from const import STYLE_COL

from model import TableSemantics, MainLangSemantics, VarLangSemantics
from model import Index, Usage
from aggregator import (
    _present,
    _build_usages,
    _multiword,
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
    assert _present(row, sem)
    row = ["\ue205моуть GH", "ѩт\ue205", "", "1/7b19"] + ([""] * 18) + ["hl00"]
    assert _present(row, sem)
    row = ["\ue205моуть GH", "", "", "1/7b19"] + ([""] * 18) + ["hl00"]
    assert not _present(row, sem)

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
        + ["πιστεύσωσι", "πιστεύω",]
        + ([""] * 11)
        + ["hl00"]
    )
    assert not _present(row, sem)
    row = ["\ue205моуть GH", "ѩт\ue205", "", "1/7b19"] + ([""] * 18) + ["hl00"]
    assert not _present(row, sem)


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
        + ["πιστεύσωσι", "πιστεύω",]
        + ([""] * 11)
        + ["hl00"]
    )

    d1 = SortedDict()
    d1 = _build_usages(row, sem.sl, sem.gr, d1, "вѣроват_")
    assert d1 == SortedDict(
        {
            "πιστεύω": {
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
    d2 = _build_usages(row, sem.gr, sem.sl, d2, "πιστεύω")
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


def test__multiword():
    sem = VarLangSemantics("sl", 0, [1])
    result = _multiword(["ноедаго G  днородоу H", "днородъ H / ноѧдъ G"], sem)
    assert len(result) == 2
    assert result["G"] == "\ue205но\ue20dедаго"
    assert result["H"] == "\ue201д\ue205нородоу"

    result = _multiword(["ноедаго G", "днородъ H / ноѧдъ G"], sem)
    assert result == {"G": "\ue205но\ue20dедаго"}

    result = _multiword(["", ""], sem)
    assert result == {}

    result = _multiword(["дноеды WH Ø G", "дноѧдъ"], sem)
    assert result == {"WH": "дноеды", "G": "Ø"}

    result = _multiword(["дноеды", "дноѧдъ"], sem)
    assert result == {"WGH": "дноеды"}


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
