import re

import alphabet
from const import SPECIAL_CHARS, EMPTY_CH, OMMIT_SUBLEMMA
from config import FROM_LANG, TO_LANG
from alphabet import remap
from util import ord_word, subscript, _ord, remap_by_range


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

    from util import SPECIALS

    for i, c in enumerate(SPECIALS):
        if i == 0:
            continue
        assert _ord(SPECIALS[i - 1]) < _ord(c)

    assert _ord("≈") < _ord("Ø".lower())


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
    assert ord_word("μαρτυρέω") < ord_word("≈ μαρτυρέω")
    assert ord_word("свѣтъ") < ord_word("≠ свѣтъ")
    # assert ord_word("* свѣтъ") < ord_word("om.")

    assert ord_word("om.") < ord_word("свѣтъ & на")
    assert ord_word("gram.") < ord_word("μαρτυρέω & διαλεγομαι")

    assert ord_word("ὁ κατὰ τῆν χρείαν") == ord_word("ο κατα την χρειαν")
    assert ord_word("ἐξερχόμενοι Nt") == ord_word("εξερχομενοι Nt")
    assert ord_word("ἁμαρτιῶν") == ord_word("αμαρτιων")
    assert ord_word("Ἀβραὰμ") == ord_word("Αβρααμ")

    assert ord_word("давꙑдъ") == ord_word("Давꙑдъ")

    assert ord_word("ὁ & ὑποτεταγμένος") > ord_word("om.")

    assert ord_word("πρᾷος") < ord_word("πτωχός")
    assert ord_word("σ") < ord_word("φ")
    assert ord_word("ζω") < ord_word("τίζω")
    assert ord_word("σωζω") < ord_word("φωτίζω")
    assert ord_word("σῴζω") < ord_word("φωτίζω")

    for c in SPECIAL_CHARS:
        assert ord_word(OMMIT_SUBLEMMA) > ord_word(c)
        assert ord_word(EMPTY_CH) > ord_word(c)


def test_ord_numbers():
    assert ord_word("аї") == ord_word("аї")
    assert ord_word("а҃") == ord_word("а")
    assert ord_word("в҃") == ord_word("в")
    assert ord_word("вї") == ord_word("вї")
    assert ord_word("вї҃") == ord_word("вї")
    assert ord_word("ѕ҃") == ord_word("ѕ")
    assert ord_word("ѕї") > ord_word("ѕ҃и") == ord_word("ꙃи")

    assert ord_word("ѳтꙑ\ue205") == ord_word("ѳ҃тꙑ\ue205")
    assert ord_word("на") == ord_word("н\ue010а")
    assert ord_word("ѵ") > ord_word("н\ue010а") > ord_word("а")
    assert ord_word("аї") == ord_word("а\ue010ї")
    assert ord_word("ѵ") > ord_word("а\ue010ї") > ord_word("а")
    assert ord_word("т҃") < ord_word("тана")


def test_subscript():
    assert subscript(1, FROM_LANG) == ""
    assert subscript(1, TO_LANG) == ""
    assert subscript(2, FROM_LANG) == "2"
    assert subscript(2, TO_LANG) == "β"


def test_remap():
    for k, v in remap.items():
        r = remap_by_range(k)
        if r:
            assert r == v
