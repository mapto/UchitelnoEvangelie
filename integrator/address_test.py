from address import Index


def test_index_unpack():
    assert Index.unpack("1/W167c4").longstr() == "01/W167c04"
    assert str(Index.unpack("1/6c4")) == "1/6c4"
    assert (
        str(Index.unpack("1/6c4", ocnt=3))
        == "1/6c4[3]"
        == str(Index.unpack("1/6c4[3]"))
    )

    # DIRTY:
    assert str(Index.unpack("1/6c4", ocnt=3, tcnt=2)) == "1/6c4[3]{2}"
    assert "1/6c4{3}" == str(Index.unpack("1/6c4", tcnt=3))

    assert str(Index.unpack("1/6c4-8")) == "1/6c4-8"
    assert str(Index.unpack("1/6c4-d4")) == "1/6c4-d4"
    assert str(Index.unpack("1/6c4-6d4")) == "1/6c4-d4"
    assert str(Index.unpack("1/6c4-7d4")) == "1/6c4-7d4"
    assert str(Index.unpack("1/6c4-2/6d4")) == "1/6c4-2/6d4"


def test_index_unpack_parts():
    assert Index.unpack("2/6a8").ch == 2
    assert Index.unpack("1/W167c4").alt

    assert not Index.unpack("2/W167c4").alt
    assert Index.unpack("2/W167c4").ch == 2


# def test_other_indexing():
#     assert str(Index.unpack("554.12")) == "554.12"


def test_index_order():
    assert Index.unpack("1/6a8") < Index.unpack("1/6a17")
    assert Index.unpack("1/6a8") < Index.unpack("1/W167c4")
    assert Index.unpack("2/6a8") > Index.unpack("2/W167c4")

    assert Index.unpack("1/8b5-6") > Index.unpack("1/5a5")
    assert Index.unpack("1/5a5") < Index.unpack("3/11b2-3")
    assert Index.unpack("3/11b2-3") > Index.unpack("1/W168a14-15")

    assert Index.unpack("1/8a13") > Index.unpack("1/5d9{2}")
