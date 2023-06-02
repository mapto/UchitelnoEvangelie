"""like config, but depends on models"""

import logging as log

from config import FROM_LANG, TO_LANG
from model import Index
from semantics import MainLangSemantics, VarLangSemantics


def address_less(a: Index, b: Index) -> bool:
    """
    >>> address_less(Index("37/169b09"), Index("37/W234b17"))
    True
    >>> address_less(Index("37/169b10"), Index("37/W234b17"))
    False
    >>> address_less(Index("47/211b01"), Index("47/W258b17"))
    True
    >>> address_less(Index("47/211b02"), Index("47/W258b17"))
    False
    >>> address_less(Index("48/216b12"), Index("48/W260c26"))
    True
    >>> address_less(Index("48/216b13"), Index("48/W260c26"))
    False
    """
    if a.data[0] == b.data[0] == 1:
        if a.data[2] == "W" and b.data[2] != "W":
            return False
        if a.data[2] != "W" and b.data[2] == "W":
            return True

    if a.data[0] == b.data[0] == 2:
        if a.data[2] == "W" and b.data[2] != "W":
            return True
        if a.data[2] != "W" and b.data[2] == "W":
            return False

    if a.data[0] == b.data[0] == 37:
        if a.data[2] == "W" and b.data[2] != "W":
            assert type(b.data[2]) == type(b.data[4]) == int  # for mypy
            assert type(b.data[3]) == str  # for mypy
            return (
                b.data[2] > 169
                or b.data[2] == 169
                and b.data[3] > "b"
                or b.data[2] == 169
                and b.data[3] == "b"
                and b.data[4] > 9
            )
        if a.data[2] != "W" and b.data[2] == "W":
            assert type(a.data[2]) == type(a.data[4]) == int  # for mypy
            assert type(a.data[3]) == str  # for mypy
            return (
                a.data[2] < 169
                or a.data[2] == 169
                and a.data[3] < "b"
                or a.data[2] == 169
                and a.data[3] == "b"
                and a.data[4] < 10
            )  # type: ignore

    if a.data[0] == b.data[0] == 47:
        if a.data[2] == "W" and b.data[2] != "W":
            assert type(b.data[2]) == type(b.data[4]) == int  # for mypy
            assert type(b.data[3]) == str  # for mypy
            return (
                b.data[2] > 211
                or b.data[2] == 211
                and b.data[3] > "b"
                or b.data[2] == 211
                and b.data[3] == "b"
                and b.data[4] > 1
            )
        if a.data[2] != "W" and b.data[2] == "W":
            assert type(a.data[2]) == type(a.data[4]) == int  # for mypy
            assert type(a.data[3]) == str  # for mypy
            return (
                a.data[2] < 211
                or a.data[2] == 211
                and a.data[3] < "b"
                or a.data[2] == 211
                and a.data[3] == "b"
                and a.data[4] < 2
            )

    if a.data[0] == b.data[0] == 48:
        if a.data[2] == "W" and b.data[2] != "W":
            assert type(b.data[2]) == type(b.data[4]) == int  # for mypy
            assert type(b.data[3]) == str  # for mypy
            return (
                b.data[2] > 216
                or b.data[2] == 216
                and b.data[3] > "c"
                or b.data[2] == 216
                and b.data[3] == "b"
                and b.data[4] > 12
            )  # type: ignore
        if a.data[2] != "W" and b.data[2] == "W":
            assert type(a.data[2]) == type(a.data[4]) == int  # for mypy
            assert type(a.data[3]) == str  # for mypy
            return (
                a.data[2] < 216
                or a.data[2] == 216
                and a.data[3] < "b"
                or a.data[2] == 216
                and a.data[3] == "b"
                and a.data[4] < 13
            )  # type: ignore

    for i, v in enumerate(a.data):
        if type(v) != type(b.data[i]):
            if a.data[2] == "W":
                log.error(
                    f"Неочаквана препратка към Виенски ръкопис на {a}. Подредбата на адресите в съответното слово трябва да бъде изрично зададена."
                )
            if b.data[2] == "W":
                log.error(
                    f"Неочаквана препратка към Виенски ръкопис на {b}. Подредбата на адресите в съответното слово трябва да бъде изрично зададена."
                )
            log.warn(f"Азбучното подреждане между адреси {a} и {b} може да е грешно.")
            return False

        if v < b.data[i]:  # type: ignore
            return True
        if v > b.data[i]:  # type: ignore
            return False
    if a.end:
        return a.end < b.end if b.end else True
    return b.end is not None


Index.maxlen = [2, 1, 3, 3, 2, 2]
Index._less = address_less

# see setup_test.py>test_ranges for interpretation of column indices
sl_sem = MainLangSemantics(
    FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
)
gr_sem = MainLangSemantics(
    TO_LANG, 11, [12, 13, 14, 15], VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20])
)
