# languages
FROM_LANG = "sl"
TO_LANG = "gr"

# first letter is main variant
MAIN_SL = "S"  # for Synodal
ALT_SL = "W"  # for Wiener
VAR_SL = "WGH"
DEFAULT_SL = VAR_SL
MAIN_GR = ""  # "C" for Cramer
VAR_GR = "BCM" + "".join(f"P{chr(ord('a')+c)}" for c in range(26))  # for Paris x
DEFAULT_GR = "C"  # for Cramer
