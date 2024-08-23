from .address import Index

from setup import address_less


def test_index_longstr():
    assert Index("1/W167c4").longstr() == "01/W167c04"

    assert Index("1/7c4-68a1").longstr() == "01/007c04-068a01"

    i = Index("06/33c11")
    i.end = Index("06/33c11*")
    assert i.longstr() == "06/033c11"

    i = Index("07/43c13*")
    i.end = Index("07/43c13")
    assert i.longstr() == "07/043c13*"


def test_index_unpack():
    assert str(Index("1/6c4")) == "1/6c4"

    assert str(Index("1/6c4-8")) == "1/6c4-8"
    assert str(Index("1/6c4-d4")) == "1/6c4-d4"
    assert str(Index("1/6c4-6d4")) == "1/6c4-d4"
    assert str(Index("1/6c4-7d4")) == "1/6c4-7d4"
    assert str(Index("1/6c4-2/6d4")) == "1/6c4-2/6d4"


def test_index_unpack_parts():
    assert Index("2/6a8").data[0] == 2
    assert Index("1/W167c4").data[2] == "W"

    assert Index("2/W167c4").data[2] == "W"
    assert Index("2/W167c4").data[0] == 2


# def test_other_indexing():
#     assert str(Index("554.12")) == "554.12"


def test_index_order():
    Index._less = address_less

    assert Index("1/6a8") < Index("1/6a17")
    assert Index("1/6a8") < Index("1/W167c4")
    assert Index("2/6a8") > Index("2/W167c4")

    assert Index("1/8b5-6") > Index("1/5a5")
    assert Index("1/5a5") < Index("3/11b2-3")
    assert Index("3/11b2-3") > Index("1/W168a14-15")
