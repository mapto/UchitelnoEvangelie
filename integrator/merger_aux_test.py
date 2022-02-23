from setup import sl_sem, gr_sem
from semantics import VarLangSemantics
from merger import _hilited_lemma, _expand_special_char


def test_hilited_lemma():
    r = (
        [""] * 4
        + [
            "1/W168a15",
            "б\ue205хомь",
            "б\ue205хомь стрьпѣтї• ",
            "бꙑт\ue205 ",
            "",
            "gramm.",
        ]
        + [""] * 16
        + ["hl05|hl09"]
    )
    assert _hilited_lemma(sl_sem, gr_sem, r)
    assert _hilited_lemma(gr_sem, sl_sem, r)
    r = (
        [""] * 4
        + [
            "1/W168a14",
            "вьꙁмогл\ue205",
            "мы брьньн\ue205 \ue205 ꙁемⷧ҇ьн\ue205\ue205• вьꙁмогл\ue205",
            "въꙁмощ\ue205",
        ]
        + [""] * 3
        + ["ἠδυνήθημεν", "δύναμαι", "pass."]
        + [""] * 12
        + ["hl05"]
    )
    assert not _hilited_lemma(sl_sem, gr_sem, r)
    assert not _hilited_lemma(gr_sem, sl_sem, r)
    r = (
        [
            "+ \ue201сть GH",
            "бꙑт\ue205",
            "gramm.",
            "",
            "07/47a06",
            "om.",
            "сътвор\ue205лъ",
            "om.",
        ]
        + [""] * 3
        + ["Ø"] * 2
        + [""] * 13
        + ["hl05|hl02"]
    )
    assert _hilited_lemma(sl_sem, gr_sem, r)
    assert _hilited_lemma(sl_sem.var, gr_sem.var, r)
    r = (
        [""] * 4
        + ["12/67c10", "бꙑхомъ•", "в\ue205дѣл\ue205 бꙑхо-", "бꙑт\ue205"]
        + ["", "gramm.", ""] * 2
        + [""] * 12
        + ["hl05|hl09"]
    )
    assert _hilited_lemma(sl_sem, gr_sem, r)
    assert _hilited_lemma(sl_sem.var, gr_sem, r)


def test_expand_special_char():
    sl_sem = VarLangSemantics("sl", 0, [1, 2, 3], None)
    r = _expand_special_char(sl_sem, ["word", "lemma", "*", ""])
    assert r == ["word", "lemma", "* lemma", ""]
    r = _expand_special_char(sl_sem, ["word", "lemma", "* l2", ""])
    assert r == ["word", "lemma", "* l2", ""]
