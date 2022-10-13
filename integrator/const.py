from config import FROM_LANG, TO_LANG
from config import VAR_SL, VAR_GR
from config import DEFAULT_SL, DEFAULT_GR

IDX_COL = 4  # E
EXAMPLE_COL = 6  # G
STYLE_COL = 26  # at end of content columns

PATH_SEP = " → "  # used to show path in hierarchy
CF_SEP = "»"  # used to indicate details about alternatives to a usage
H_LEMMA_SEP = "/"  # indicates multiple variants provided together
V_LEMMA_SEP = "&"  # indicates lemmas merged from several rows
VAR_SEP = "-"  # used to separate the two language in variant source annotation

INDENT_CH = "|"
BULLET_CH = "∙"  # or ●
SAME_CH = "="
MISSING_CH = "ₓ"  # used when untranslatable
EMPTY_CH = "Ø"  # used when text has intended to have no translation
SPECIAL_CHARS = ["*", "≠", "≈", "#"]  # # - for contextual translation

ERR_SUBLEMMA = "err. pro"
OMMIT_SUBLEMMA = "om."

NON_COUNTABLE = [EMPTY_CH, MISSING_CH, OMMIT_SUBLEMMA]
NON_LEMMAS = ["gramm."]

BRACE_OPEN = {FROM_LANG: "[", TO_LANG: "{"}
BRACE_CLOSE = {FROM_LANG: "]", TO_LANG: "}"}
