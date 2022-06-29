"""like config, but depends on models"""

from config import FROM_LANG, TO_LANG
from model import Index
from semantics import MainLangSemantics, VarLangSemantics

def address_less(a: Index, b: Index) -> bool:
    if a.data[0] == b.data[0] == 1 and a.data[2] == "W" and b.data[2] != "W":
        return False
    if a.data[0] == b.data[0] == 1 and a.data[2] != "W" and b.data[2] == "W":
        return True
    if a.data[0] == b.data[0] == 2 and a.data[2] == "W" and b.data[2] != "W":
        return True
    if a.data[0] == b.data[0] == 2 and a.data[2] != "W" and b.data[2] == "W":
        return False
    for i, v in enumerate(a.data):
        try:
            if v < b.data[i]:
                return True
            if v > b.data[i]:
                return False
        except TypeError as te:
            print(
                f"ГРЕШКА: Сравнение на несравними стойности {v} и {b.data[i]}"
            )
            print(te)
            break
    if a.end:
        return a.end < b.end if b.end else True
    else:
        return b.end is not None

Index.maxlen = [2,1,3,3,2,2]
Index._less = address_less

sl_sem = MainLangSemantics(
    FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
)
gr_sem = MainLangSemantics(
    TO_LANG, 11, [12, 13, 14, 15], VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20])
)

