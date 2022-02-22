from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import STYLE_COL

from semantics import MainLangSemantics, VarLangSemantics
from aggregator import present, _expand_and_aggregate


def test_present():
    sem = VarLangSemantics(lang="sl", word=0, lemmas=[1, 2, 20, 21])
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "",
            "1/7b19",
            "вѣроують",
            "вьс\ue205 вѣроують",
            "вѣроват\ue205",
        ]
        + ([""] * 3)
        + ["πιστεύσωσι", "πιστεύω"]
        + ([""] * 13)
        + ["hl00"]
    )
    assert present(row, sem)
    row = (
        ["\ue205моуть GH", "ѩт\ue205"]
        + ([""] * 2)
        + ["1/7b19"]
        + ([""] * 20)
        + ["hl00"]
    )
    assert present(row, sem)
    row = ["\ue205моуть GH"] + ([""] * 3) + ["1/7b19"] + ([""] * 20) + ["hl00"]
    assert not present(row, sem)

    sem = VarLangSemantics(lang="gr", word=16, lemmas=[17, 18, 19])
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "",
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
        + ([""] * 13)
        + ["hl00"]
    )
    assert not present(row, sem)
    row = (
        ["\ue205моуть GH", "ѩт\ue205"]
        + ([""] * 2)
        + ["1/7b19"]
        + ([""] * 20)
        + ["hl00"]
    )
    assert not present(row, sem)

    row = (
        ([""] * 4)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με C", "ἐγώ"]
        + ([""] * 9)
    )
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )
    assert not present(row, sl_sem.var)
    assert present(row, sl_sem)
    assert not present(row, gr_sem)
    assert present(row, gr_sem.var)


def test__agg_lemma():
    row = [""] * STYLE_COL
    dummy_sem = VarLangSemantics(lang="sl_var", word=0, lemmas=[1, 2, 19, 20])
    d = SortedDict()

    d = _expand_and_aggregate(row, None, dummy_sem, d)
    assert len(d) == 0

    d = _expand_and_aggregate(row, dummy_sem, None, d)
    assert len(d) == 0

    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )
