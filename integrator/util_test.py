from util import collect, ord_word
from semantics import MainLangSemantics, VarLangSemantics


def test_collect_words():
    sl_sem = MainLangSemantics(
        "sl", 5, [7, 8, 9, 10], VarLangSemantics("sl", 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        "gr", 11, [12, 13, 14], VarLangSemantics("gr", 16, [17, 18, 19])
    )

    r1 = (
        [""] * 4
        + ["1/5a5", "не", "не бѣ ꙗвленъ•", "не", "не бꙑт\ue205 ꙗвл\ue201нъ"]
        + [""] * 2
        + ["ἠγνοεῖτο", "ἀγνοέω"]
        + [""] * 13
        + ["hl05"]
    )
    r2 = (
        [""] * 4
        + ["1/5a5", "бѣ", "", "бꙑт\ue205", "", "gramm."]
        + [""] * 2
        + ["pass."]
        + [""] * 13
        + ["hl05|hl09"]
    )
    r3 = [""] * 4 + ["1/5a5", "ꙗвленъ•", "", "ꙗв\ue205т\ue205"] + [""] * 18 + ["hl05"]

    group = [r1, r2, r3]

    result = collect(group, sl_sem.word)
    assert result == ["не", "бѣ", "ꙗвленъ•"]


def test_ord_word():
    assert ord_word("свѣтъ") < ord_word("свѧтъ")
    assert ord_word("μαρτυρέω") == ord_word("μαρτυρέω")
    assert ord_word("διαλεγομαι") < ord_word("διαλεγω") < ord_word("διατριβω")
    assert ord_word("а conj.") > ord_word("а")
    assert ord_word("на + Acc.") > ord_word("на")
    assert ord_word("*") > ord_word(" conj.: н*") > ord_word(" conj.")

    assert ord_word("свѣтъ") < ord_word("om.")
    assert ord_word("μαρτυρέω") < ord_word("gram.")

    assert ord_word("μαρτυρέω") < ord_word("Ø")
    assert ord_word("Ø") < ord_word("≠")
    assert ord_word("μαρτυρέω") < ord_word("≈ μαρτυρέω")
    assert ord_word("свѣтъ") < ord_word("≠ свѣтъ")
    assert ord_word("* свѣтъ") < ord_word("om.")

    assert ord_word("om.") < ord_word("свѣтъ & на")
    assert ord_word("gram.") < ord_word("μαρτυρέω & διαλεγομαι")
