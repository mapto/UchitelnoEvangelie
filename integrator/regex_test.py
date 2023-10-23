import re

from regex import counter_regex, multilemma_regex

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


def test_multilemma():
    m = re.search(multilemma_regex, "διά + Gen")
    assert m.group(1) == "διά "
    assert m.group(2) == "+ Gen"

    m = re.search(multilemma_regex, "διά + Gen.")
    assert m.group(1) == "διά "
    assert m.group(2) == "+ Gen."

    m = re.search(multilemma_regex, "πρός +Acc.")
    assert m.group(1) == "πρός "
    assert m.group(2) == "+Acc."

    m = re.search(multilemma_regex, "μετά + Acc.")
    assert m.group(1) == "μετά "
    assert m.group(2) == "+ Acc."

    m = re.search(multilemma_regex, "κατά + Gen. Fb")
    assert m.group(1) == "κατά "
    assert m.group(2) == "+ Gen. "
    assert m.group(3) == "Fb"

    m = re.search(multilemma_regex, "νεότης + Gen. CsMdSp")
    assert m.group(1) == "νεότης "
    assert m.group(2) == "+ Gen. "
    assert m.group(3) == "CsMdSp"

    m = re.search(multilemma_regex, "νεανιότης + Gen. FbPcPePgPhPiZaAPaVCh")
    assert m.group(1) == "νεανιότης "
    assert m.group(2) == "+ Gen. "
    assert m.group(3) == "FbPcPePgPhPiZaAPaVCh"

    m = re.search(multilemma_regex, "μετά + Acc. Cs / κατά + Gen. Fb")
    assert m.group(1) == "μετά "
    assert m.group(2) == "+ Acc. "
    assert m.group(3) == "Cs"
    assert m.group(4) == "Cs"
    assert m.group(5) == " /"
    assert m.group(6) == " κατά + Gen. Fb"

    m = re.search(multilemma_regex, "κατά + Gen. Fb")
    assert m.group(1) == "κατά "
    assert m.group(2) == "+ Gen. "
    assert m.group(3) == "Fb"
