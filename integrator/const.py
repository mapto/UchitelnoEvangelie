from config import FROM_LANG, TO_LANG
from config import VAR_SL, VAR_GR
from config import DEFAULT_SL, DEFAULT_GR

IDX_COL = 4
EXAMPLE_COL = 6
STYLE_COL = 26  # at end of content columns

PATH_SEP = " → "  # used to show path in hierarchy
CF_SEP = "»"  # used to indicate details about alternatives to a usage
H_LEMMA_SEP = "/"  # indicates multiple variants provided together
V_LEMMA_SEP = "&"  # indicates lemmas merged from several rows
VAR_SEP = "-"  # used to separate the two language in variant source annotation

SAME_CH = "="
MISSING_CH = "ₓ"
EMPTY_CH = "Ø"  # used when text is original, so no translation
SPECIAL_CHARS = ["*", "≠", "≈", "#"]  # # - for contextual translation

ERR_SUBLEMMA = "err. pro"
OMMIT_SUBLEMMA = "om."

NON_COUNTABLE = [EMPTY_CH, MISSING_CH, OMMIT_SUBLEMMA]

BRACE_OPEN = {FROM_LANG: "[", TO_LANG: "{"}
BRACE_CLOSE = {FROM_LANG: "]", TO_LANG: "}"}

VAR_SOURCES = {TO_LANG: VAR_GR, FROM_LANG: VAR_SL}
DEFAULT_SOURCES = {TO_LANG: DEFAULT_GR, FROM_LANG: DEFAULT_SL}
