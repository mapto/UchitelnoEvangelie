from model import TableSemantics, MainLangSemantics, VarLangSemantics
from aggregator import _present, _build_key, _build_usage
from sortedcontainers import SortedDict  # type: ignore


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


def test__build_key():
    sem = MainLangSemantics(
        lang="sl",
        word=4,
        lemmas=[6, 7, 8, 9],
        var=VarLangSemantics(lang="sl", word=0, lemmas=[1, 2, 19, 20]),
    )
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

    assert "сел\ue205ко" == _build_key(row, sem)
    assert " {\ue201л\ue205ко}" == _build_key(row, sem.var)
    # assert " {\ue201л\ue205ко WH}" == _build_key(row, sem.var)


def test__build_usage():
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
    key = ("вѣроують {вѣроу GH}", "πιστεύσωσι")
    d1 = _build_usage(row, sem.sl, sem.gr, key, d1)
    # TODO: Need to find way to exclude current variant from alternative variants
    """
    assert (
        repr(d1)
        == "SortedDict({'πιστεύω': {('вѣроують {вѣроу GH}', 'πιστεύσωσι'): SortedSet([Usage(idx=Index(ch=1, alt=False, page=7, col='b', row=19, var=False, end=None, bold=False, italic=False), lang='sl', var='', orig_alt='', orig_alt_var=['вѣра'], trans_alt='', trans_alt_var=[])])}})"
    )
    """
    d2 = SortedDict()
    key = ("πιστεύσωσι", "вѣроують {вѣроу GH}")
    d2 = _build_usage(row, sem.gr, sem.sl, key, d2)
    """
    assert (
        repr(d2)
        == "SortedDict({'вѣроват_': {('πιστεύσωσι', 'вѣроують {вѣроу GH}'): SortedSet([Usage(idx=Index(ch=1, alt=False, page=7, col='b', row=19, var=False, end=None, bold=False, italic=False), lang='gr', var='', orig_alt='', orig_alt_var=[], trans_alt='', trans_alt_var=['вѣра'])])}})"
    )
    """