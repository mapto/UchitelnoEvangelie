from typing import List, Tuple

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
    >>> parse_source_line('Ma   M208 München, BSB, Gr. 208, f. 60v ff ')
    'Ma'
    >>> parse_source_line('Cs  Cramer supplementum, default variant')
    'Cs'
    >>> parse_source_line('#Cs  Cramer supplementum, default variant')
    ''
    >>> parse_source_line(' Cs  Cramer supplementum, default variant')
    ''
    >>> parse_source_line(None)
    ''
    >>> parse_source_line('   ')
    ''
    """
    if not l or not l[0].isalpha() or not l.strip():
        return ""
    m = re.search(source_regex, l)
    if not m:
        raise ValueError(f"No valid source detected: {l}")
    return m.group(1).strip()


def parse_sources(lang: "str") -> Tuple[str, List[str]]:
    fname = source_cfg.format(lang)
    if not path.exists(fname):
        FileNotFoundError(f"File not found: {fname}")

    with open(fname, "r") as fcfg:
        smain = ""
        svar: List[str] = []
        for l in fcfg:
            if not smain:
                smain = parse_source_line(l)
                continue
            nxt = parse_source_line(l)
            if not nxt:
                continue
            if nxt not in svar:
                svar += [nxt]

    return smain, svar


MAIN_SL, VAR_SL = parse_sources(FROM_LANG)
ALT_SL = "W"  # for Wiener
DEFAULT_SL: str = "".join(VAR_SL)
assert DEFAULT_SL == "WGH"

MAIN_GR, VAR_GR = parse_sources(TO_LANG)
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
