from typing import List

import sys
from os import path
import re

source_regex = r"^([A-Z][a-z]?)(.*)$"

# languages
FROM_LANG = "sl"
TO_LANG = "gr"
other_lang = {TO_LANG: FROM_LANG, FROM_LANG: TO_LANG}


bin_path = path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__)
source_cfg = path.join(path.dirname(bin_path), "{}-sources.txt")


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

DEFAULT_SOURCES = {TO_LANG: DEFAULT_GR, FROM_LANG: DEFAULT_SL}
VAR_SOURCES = {TO_LANG: VAR_GR, FROM_LANG: VAR_SL}


if __name__ == "__main__":
    print(__file__)
    print(path.dirname(__file__))
    print(path.abspath(__file__))
    print(path.dirname(path.abspath(__file__)))
    import sys

    print(path.dirname(sys.argv[0]))
    print(path.abspath(sys.argv[0]))
    print(path.dirname(path.abspath(sys.argv[0])))
