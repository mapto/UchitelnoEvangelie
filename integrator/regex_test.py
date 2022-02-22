import re

from regex import counter_regex, source_regex


def test_counter():
    assert re.fullmatch(counter_regex, "")
    assert re.fullmatch(counter_regex, "[3]")
    assert re.fullmatch(counter_regex, "{2}")
    assert re.fullmatch(counter_regex, "[4]{2}")


def test_source():
    assert re.fullmatch(source_regex, "WGH")
    assert re.fullmatch(source_regex, "MPaPb")

    # Non UE
    assert re.fullmatch(source_regex, "D56D58")
