IDX_COL = 4
EXAMPLE_COL = 6
STYLE_COL = 26

PATH_SEP = " → "  # used to show path in hierarchy
CF_SEP = "»"  # used to indicate details about alternatives to a usage
H_LEMMA_SEP = "/"  # indicates multiple variants provided together
V_LEMMA_SEP = "&"  # indicates lemmas merged from several rows
VAR_SEP = "-"  # used to separate the two language in variant source annotation

MISSING_CH = "ₓ"
EMPTY_CH = "Ø"  # used when text is original, so no translation
SPECIAL_CHARS = ["*", "≠", "≈"]

# first letter is main variant
MAIN_SL = "S"  # for Synodal
VAR_SL = "WGH"
DEFAULT_SL = VAR_SL
MAIN_GR = ""  # "C" for Cramer
VAR_GR = "BCMPaPbPc"  # for Paris x
DEFAULT_GR = "C"  # for Cramer

main_source = {"gr": MAIN_GR, "sl": MAIN_SL}
# var_sources = {"gr": VAR_GR, "sl": VAR_SL}
default_sources = {"gr": DEFAULT_GR, "sl": DEFAULT_SL}
