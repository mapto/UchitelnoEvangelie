IDX_COL = 3
EXAMPLE_COL = 5
STYLE_COL = 23

PATH_SEP = " → "  # used to show path in hierarchy
CF_SEP = "»"
H_LEMMA_SEP = "/"  # indicates multiple variants provided together
V_LEMMA_SEP = "&"  # indicates lemmas merged from several rows
VAR_SEP = "//"  # or "-"
MISSING_CH = "ₓ"
EMPTY_CH = "Ø"

# first letter is main variant
MAIN_SL = "S"
VAR_SL = "WGH"
DEFAULT_SL = VAR_SL
MAIN_GR = "C"
VAR_GR = "C"
DEFAULT_GR = "C"

main_source = {"gr": MAIN_GR, "sl": MAIN_SL}
var_sources = {"gr": VAR_GR, "sl": VAR_SL}
default_sources = {"gr": DEFAULT_GR, "sl": DEFAULT_SL}
