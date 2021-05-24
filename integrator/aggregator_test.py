from model import LangSemantics
from aggregator import _present


def test_present():
    sem = LangSemantics(lang="sl_var", word=0, lemmas=[1, 2, 19, 20], var=None)
    row = [
        "вѣроу GH",
        "вѣра",
        "вѣрѫ ѩт\ue205",
        "1/7b19",
        "вѣроують",
        "вьс\ue205 вѣроують",
        "вѣроват\ue205",
        "",
        "",
        "",
        "πιστεύσωσι",
        "πιστεύω",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "hl00",
    ]
    assert _present(row, sem)
    row = [
        "\ue205моуть GH",
        "ѩт\ue205",
        "",
        "1/7b19",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "hl00",
    ]
    assert _present(row, sem)
    row = [
        "\ue205моуть GH",
        "",
        "",
        "1/7b19",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "hl00",
    ]
    assert not _present(row, sem)

    sem = LangSemantics(lang="gr_var", word=15, lemmas=[16, 17, 19], var=None)
    row = [
        "вѣроу GH",
        "вѣра",
        "вѣрѫ ѩт\ue205",
        "1/7b19",
        "вѣроують",
        "вьс\ue205 вѣроують",
        "вѣроват\ue205",
        "",
        "",
        "",
        "πιστεύσωσι",
        "πιστεύω",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "hl00",
    ]
    assert not _present(row, sem)
    row = [
        "\ue205моуть GH",
        "ѩт\ue205",
        "",
        "1/7b19",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "hl00",
    ]
    assert not _present(row, sem)
