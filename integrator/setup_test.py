from model import Index
from setup import address_less, sl_sem, gr_sem

LETTERS = ord("Z") - ord("A") + 1


def sheet_column(i: int) -> str:
    """
    Converts a 0-index of column to the spreadsheet column name
    >>> sheet_column(0)
    'A'
    >>> sheet_column(25)
    'Z'
    >>> sheet_column(26)
    'AA'
    >>> sheet_column(51)
    'AZ'
    >>> sheet_column(52)
    'BA'
    """
    if i >= LETTERS:
        return chr(ord("A") - 1 + i // LETTERS) + chr(ord("A") + i % LETTERS)
    return chr(ord("A") + i)


def test_address_less():
    assert address_less(Index("1/5a5"), Index("2/5a5"))
    assert address_less(Index("1/5a5"), Index("1/6a5"))
    assert address_less(Index("1/5a5"), Index("1/5b5"))
    assert address_less(Index("1/5a5"), Index("1/5a6"))

    assert address_less(Index("1/5a5"), Index("1/W5a5"))
    assert address_less(Index("2/W5a5"), Index("2/5a5"))


def test_ranges():
    assert sheet_column(sl_sem.word) == "F"
    assert "".join(sheet_column(c) for c in sl_sem.lemmas) == "HIJK"
    assert sheet_column(sl_sem.var.word) == "A"
    assert "".join(sheet_column(c) for c in sl_sem.var.lemmas) == "BCDW"

    assert sheet_column(gr_sem.word) == "L"
    assert "".join(sheet_column(c) for c in gr_sem.lemmas) == "MNOP"
    assert sheet_column(gr_sem.var.word) == "Q"
    assert "".join(sheet_column(c) for c in gr_sem.var.lemmas) == "RSTU"
