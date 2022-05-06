import re

import alphabet
from config import FROM_LANG, TO_LANG
from util import ord_word, subscript, _ord


def test_ord_letters():
    lines = alphabet.__doc__.split("\n")
    for l in lines:
        line = l.strip()
        if len(line) == 0 or (line[0] != "а" and line[0] != "α"):
            continue
        chars = line.split(" ")
        for i in range(1, len(chars)):
            a = chars[i - 1]
            b = chars[i]
            if len(chars[i - 1]) > 1:
                chars2 = [x for x in re.split(r"\W", a) if x]
                for j in range(1, len(chars2)):
                    assert abs(_ord(chars2[j - 1]) - _ord(chars2[j])) <= 0.5
                a = chars2[0]
            if len(b) > 1:
                chars2 = [x for x in re.split(r"\W", b) if x]
                for j in range(1, len(chars2)):
                    assert abs(_ord(chars2[j - 1]) - _ord(chars2[j])) <= 0.5
                b = chars2[0]
            assert _ord(a) < _ord(b)


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


def test_subscript():
    assert subscript(1, FROM_LANG) == ""
    assert subscript(1, TO_LANG) == ""
    assert subscript(2, FROM_LANG) == "2"
    assert subscript(2, TO_LANG) == "β"
