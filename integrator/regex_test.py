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
