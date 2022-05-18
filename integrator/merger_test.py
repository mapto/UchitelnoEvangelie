from semantics import VarLangSemantics
from merger import _expand_special_char


def test_expand_special_char():
    sl_sem = VarLangSemantics("sl", 0, [1, 2, 3], None)
    r = _expand_special_char(sl_sem, ["word", "lemma", "*", ""])
    assert r == ["word", "lemma", "* lemma", ""]
    r = _expand_special_char(sl_sem, ["word", "lemma", "* l2", ""])
    assert r == ["word", "lemma", "* l2", ""]
