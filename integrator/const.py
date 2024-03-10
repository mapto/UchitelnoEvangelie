from config import FROM_LANG, TO_LANG

IDX_COL = 4  # E
EXAMPLE_COL = 6  # G
STYLE_COL = 26  # at end of content columns

PATH_SEP = " → "  # used to show path in hierarchy
CF_SEP = "»"  # used to indicate details about alternatives to a usage
H_LEMMA_SEP = "/"  # indicates multiple variants provided together
V_LEMMA_SEP = "&"  # indicates lemmas merged from several rows
VAR_SEP = "-"  # used to separate the two language in variant source annotation
HILITE_PREFIX = "hl"
STYLE_SEP = ":"

INDENT_CH = "|"
BULLET_CH = "∙"  # or ●
SAME_CH = "="
MISSING_CH = "ₓ"  # used when untranslatable
EMPTY_CH = "Ø"  # used when text has intended to have no translation

# Meaning of special characters is documented in README.md#semantic-relationships
# Warning: In case of refactoring, be careful that at some places this is treated as List[str],
# so just str (array of chars) would behave differently
SPECIAL_CHARS = ["#", "≈", "≠", "*"]

OMMIT_SUBLEMMA = "om."

NON_COUNTABLE = [EMPTY_CH, MISSING_CH, OMMIT_SUBLEMMA]
NON_LEMMAS = ["gramm."]

BRACE_OPEN = {FROM_LANG: "[", TO_LANG: "{"}
BRACE_CLOSE = {FROM_LANG: "]", TO_LANG: "}"}
