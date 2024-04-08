import re

from regex import counter_regex, multiword_regex, multilemma_regex

# from config import source_regex


def test_counter():
    assert re.fullmatch(counter_regex, "")
    assert re.fullmatch(counter_regex, "[3]")
    assert re.fullmatch(counter_regex, "{2}")
    assert re.fullmatch(counter_regex, "[4]{2}")


# def test_source():
#     assert re.fullmatch(source_regex, "WGH")
#     assert re.fullmatch(source_regex, "MPaPb")

#     # Non UE
#     assert re.fullmatch(source_regex, "D56D58")


def test_mulitword():
    re.search(multiword_regex, "Dat. Nt")


def test_multilemma():
    print(multilemma_regex)
    m = re.search(multilemma_regex, "διά + Gen.")
    assert m.group(1) == "διά "
    assert m.group(2) == None
    assert m.group(3) == "διά "
    assert m.group(4) == "+ Gen."

    m = re.search(multilemma_regex, "διά + Gen.")
    assert m.group(1) == "διά "
    assert m.group(4) == "+ Gen."

    m = re.search(multilemma_regex, "πρός + Acc.")
    assert m.group(1) == "πρός "
    assert m.group(4) == "+ Acc."

    m = re.search(multilemma_regex, "μετά + Acc.")
    assert m.group(1) == "μετά "
    assert m.group(4) == "+ Acc."

    m = re.search(multilemma_regex, "κατά + Gen. Fb")
    assert m.group(1) == "κατά "
    assert m.group(4) == "+ Gen. "
    assert m.group(6) == "Fb"

    m = re.search(multilemma_regex, "νεότης + Gen. CsMdSp")
    assert m.group(1) == "νεότης "
    assert m.group(4) == "+ Gen. "
    assert m.group(6) == "CsMdSp"

    m = re.search(multilemma_regex, "νεανιότης + Gen. FbPcPePgPhPiZaAPaVCh")
    assert m.group(1) == "νεανιότης "
    assert m.group(4) == "+ Gen. "
    assert m.group(6) == "FbPcPePgPhPiZaAPaVCh"

    m = re.search(multilemma_regex, "μετά + Acc. Cs / κατά + Gen. Fb")
    assert m.group(1) == "μετά "
    assert m.group(4) == "+ Acc. "
    assert m.group(6) == "Cs"
    assert m.group(7) == "Cs"
    assert m.group(8) == " /"
    assert m.group(9) == " κατά + Gen. Fb"

    m = re.search(multilemma_regex, "κατά + Gen. Fb")
    assert m.group(1) == "κατά "
    assert m.group(4) == "+ Gen. "
    assert m.group(6) == "Fb"

    m = re.search(multilemma_regex, "≈ GH")
    assert m.group(1) == "≈ "
    assert m.group(6) == "GH"

    m = re.search(multilemma_regex, "≈ ходт спѣѭще")
    assert m.group(1) == "≈ ходт спѣѭще"
    assert m.group(3) == "ходт спѣѭще"

    m = re.search(multilemma_regex, "ходомь спѣт WG")
    assert m.group(1) == "ходомь спѣт "
    assert m.group(6) == "WG"

    m = re.search(multilemma_regex, "≈ ходт спѣѭще")
    assert m.group(1) == "≈ ходт спѣѭще"
    assert m.group(3) == "ходт спѣѭще"

    m = re.search(multilemma_regex, "ὁ")
    assert m.group(3) == "ὁ"

    m = re.search(multilemma_regex, "≠ Gen.")
    assert m.group(1) == "≠ "
    assert m.group(4) == "Gen."

    m = re.search(multilemma_regex, "om.")
    assert m.group(4) == "om."

    m = re.search(multilemma_regex, "Inf.")
    assert m.group(4) == "Inf."

    m = re.search(multilemma_regex, "\ue205 pron.")
    assert m.group(3) == "\ue205 "
    assert m.group(4) == "pron."

def test_multilemma_multi():
    m = re.search(multilemma_regex, "μετά Cs / κατά Fb")
    assert m.group(3) == "μετά "
    assert m.group(6) == "Cs"
    assert m.group(9) == " κατά Fb"