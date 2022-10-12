from typing import List
import re
from os import path

source_regex = r"^([A-Z][a-z]?)(.*)$"

# languages
FROM_LANG = "sl"
TO_LANG = "gr"

# first letter is main variant

source_cfg = path.dirname(path.abspath(__file__)) + path.sep + "{}-sources.txt"


def parse_source_line(l: str) -> str:
    """
    >>> parse_source_line('S   Synodal, main text')
    'S'
    >>> parse_source_line('Cs  Cramer supplementum, default variant')
    'Cs'
    """
    m = re.search(source_regex, l)
    if not m:
        raise ValueError(f"No valid source detected: {l}")
    return m.group(1).strip()


if not path.exists(source_cfg.format(FROM_LANG)):
    FileNotFoundError(f"File not found: {source_cfg.format(FROM_LANG)}")
VAR_SL: List[str] = []
with open(source_cfg.format(FROM_LANG), "r") as fcfg:
    MAIN_SL = parse_source_line(fcfg.readline())
    nxt = parse_source_line(fcfg.readline())
    while nxt:
        VAR_SL += [nxt]
        l = fcfg.readline()
        nxt = parse_source_line(l) if l else ""

if not path.exists(source_cfg.format(TO_LANG)):
    FileNotFoundError(f"File not found: {source_cfg.format(TO_LANG)}")
VAR_GR: List[str] = []
with open(source_cfg.format(TO_LANG), "r") as fcfg:
    MAIN_GR = parse_source_line(fcfg.readline())
    nxt = parse_source_line(fcfg.readline())
    while nxt:
        VAR_GR += [nxt]
        l = fcfg.readline()
        nxt = parse_source_line(l) if l else ""

ALT_SL = "W"  # for Wiener
DEFAULT_SL: str = "".join(VAR_SL)
assert DEFAULT_SL == "WGH"
DEFAULT_GR: str = VAR_GR[0]
assert DEFAULT_GR == "Cs"

other_lang = {TO_LANG: FROM_LANG, FROM_LANG: TO_LANG}


if __name__ == "__main__":
    print(__file__)
    print(path.dirname(__file__))
    print(path.abspath(__file__))
    print(path.dirname(path.abspath(__file__)))
    import sys

    print(path.dirname(sys.argv[0]))
    print(path.abspath(sys.argv[0]))
    print(path.dirname(path.abspath(sys.argv[0])))
