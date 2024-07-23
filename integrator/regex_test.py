import re

from regex import counter_regex, multiword_regex, multilemma_regex
from regex import LP_PRE, LP_LEM, LP_ANN, LP_SRC, LP_SEP, LP_OTHER

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
    # re.search(multiword_regex, "Dat. Nt")
    m = re.search(multiword_regex, "συναλλάγματα ... τὰς ἐμπορίας Ch")
    assert m.group(1) == "συναλλάγματα ... τὰς ἐμπορίας "
    assert m.group(3) == "Ch"


def test_multilemma():
    # print(multilemma_regex)
    m = re.search(multilemma_regex, "διά + Gen.")
    # assert m.group(1) == "διά "
    assert m.group(LP_PRE) == None
    assert m.group(LP_LEM) == "διά "
    assert m.group(LP_ANN) == "+ Gen."

    m = re.search(multilemma_regex, "διά + Gen.")
    assert m.group(LP_LEM) == "διά "
    assert m.group(LP_ANN) == "+ Gen."

    m = re.search(multilemma_regex, "πρός + Acc.")
    assert m.group(LP_LEM) == "πρός "
    assert m.group(LP_ANN) == "+ Acc."

    m = re.search(multilemma_regex, "μετά + Acc.")
    assert m.group(LP_LEM) == "μετά "
    assert m.group(LP_ANN) == "+ Acc."

    m = re.search(multilemma_regex, "κατά + Gen. Fb")
    assert m.group(LP_LEM) == "κατά "
    assert m.group(LP_ANN) == "+ Gen. "
    assert m.group(LP_SRC) == "Fb"

    m = re.search(multilemma_regex, "νεότης + Gen. CsMdSp")
    assert m.group(LP_LEM) == "νεότης "
    assert m.group(LP_ANN) == "+ Gen. "
    assert m.group(LP_SRC) == "CsMdSp"

    m = re.search(multilemma_regex, "νεανιότης + Gen. FbPcPePgPhPiZaAPaVCh")
    assert m.group(LP_LEM) == "νεανιότης "
    assert m.group(LP_ANN) == "+ Gen. "
    assert m.group(LP_SRC) == "FbPcPePgPhPiZaAPaVCh"

    m = re.search(multilemma_regex, "≈ GH")
    assert m.group(LP_PRE) == "≈ "
    assert m.group(LP_SRC) == "GH"

    m = re.search(multilemma_regex, "≈ ходт спѣѭще")
    assert m.group(LP_PRE) == "≈ "
    assert m.group(LP_LEM) == "ходт спѣѭще"

    m = re.search(multilemma_regex, "ходомь спѣт WG")
    assert m.group(LP_LEM) == "ходомь спѣт "
    assert m.group(LP_SRC) == "WG"

    m = re.search(multilemma_regex, "≈ ходт спѣѭще")
    assert m.group(LP_PRE) == "≈ "
    assert m.group(LP_LEM) == "ходт спѣѭще"

    m = re.search(multilemma_regex, "ὁ")
    assert m.group(LP_LEM) == "ὁ"

    m = re.search(multilemma_regex, "≠ Gen.")
    assert m.group(LP_PRE) == "≠ "
    assert m.group(LP_ANN) == "Gen."

    m = re.search(multilemma_regex, "om.")
    assert m.group(LP_ANN) == "om."

    m = re.search(multilemma_regex, "Inf.")
    assert m.group(LP_ANN) == "Inf."

    m = re.search(multilemma_regex, "\ue205 pron.")
    assert m.group(LP_LEM) == "\ue205 "
    assert m.group(LP_ANN) == "pron."

    m = re.search(multilemma_regex, "εὔδηλον (scil. ἐστί)")
    assert m.group(LP_LEM) == "εὔδηλον "
    assert m.group(LP_ANN) == "(scil. ἐστί)"


def test_multilemma_multi():
    m = re.search(multilemma_regex, "μετά Cs / κατά Fb")
    assert m.group(LP_LEM) == "μετά "
    assert m.group(LP_SRC) == "Cs"
    assert m.group(LP_SEP) == " /"
    assert m.group(LP_OTHER) == " κατά Fb"

    m = re.search(multilemma_regex, "μετά + Acc. Cs / κατά + Gen. Fb")
    assert m.group(LP_LEM) == "μετά "
    assert m.group(LP_ANN) == "+ Acc. "
    assert m.group(LP_SRC) == "Cs"
    assert m.group(LP_SEP) == " /"
    assert m.group(LP_OTHER) == " κατά + Gen. Fb"
