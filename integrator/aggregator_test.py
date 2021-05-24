from model import VarLangSemantics
from aggregator import _present


def test_present():
    sem = VarLangSemantics(lang="sl_var", word=0, lemmas=[1, 2, 19, 20])
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

    sem = VarLangSemantics(lang="gr_var", word=15, lemmas=[16, 17, 19])
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
        + ([""] * 10)
        + ["hl00"]
    )
    assert not _present(row, sem)
    row = ["\ue205моуть GH", "ѩт\ue205", "", "1/7b19"] + ([""] * 18) + ["hl00"]
    assert not _present(row, sem)
