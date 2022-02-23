"""like config, but depends on models"""

from config import FROM_LANG, TO_LANG
from semantics import MainLangSemantics, VarLangSemantics

sl_sem = MainLangSemantics(
    FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
)
gr_sem = MainLangSemantics(
    TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
)
