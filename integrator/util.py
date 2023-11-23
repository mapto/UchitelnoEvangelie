#!/usr/bin/env python3
"""These utilities are also used by the object-oriented model,
so to avoid circular references they cannot use it"""

from typing import Dict, List, Set

import re
import logging as log
import unicodedata
from sortedcontainers import SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from config import MAIN_SL, MAIN_GR
from config import ALT_SL
from const import SPECIAL_CHARS, V_LEMMA_SEP

from alphabet import gasps, number_postfix, remap, reduce


MAX_CHAR = ord("ѵ") - ord(" ") + 30
# max([max([len(str(e)) for e in r if e]) for r in i if [e for e in r if e]])

MAX_LEN = 100


def chars(cells: List[List[str]]) -> Set:
    s: Set[str] = set()
    for r in cells:
        if not r:
            continue
        for cell in [r[4], r[6], r[7], r[8], r[10], r[11], r[12], r[13]]:
            if not cell:
                continue
            s = s.union([ch for ch in cell])
    return s


def _ord(a: str) -> float:
    assert len(a) == 1
    # Latin letters are special annotation, they should show up after Cyrillic or Greek
    if "a" <= a <= "z":
        return ord("ѵ") - ord("a") + 1 + ord(a)
    if a in SPECIAL_CHARS:
        return ord("ѵ") + 2 + SPECIAL_CHARS.index(a)
    if a in remap:
        return remap[a]
    return ord(a)


def base_word(w: str) -> str:
    if not w:
        return ""
    w = w.strip()
    # w.replace("оу", "ѹ")
    w = unicodedata.normalize("NFKC", w)
    return w


def clean_word(w: str) -> str:
    """
    Remove fake ambiguities due to OCR

    >>> clean_word("λέγω")
    'λέγω'
    >>> clean_word("εἰμί")
    'εἰμί'
    >>> clean_word("δέ")
    'δέ'
    """
    for k in reduce.keys():
        if k in w:
            w = w.replace(k, reduce[k])
    return w


def ord_word(w: str, max_len=MAX_LEN) -> int:
    """Order needs to be:
    1. Greek or Cyrillic lemmas
    2. Special annotations (using Latin alphabet)
    3. Combined lemmas in Greek or Cyrilic
    """
    a = base_word(w).lower()
    a = a.replace("оу", "ѹ")
    for ch in gasps + number_postfix:
        a = a.replace(ch, "")
    if max_len <= len(a):
        log.info(f"Unexpectedly long word: {a}")
    assert max_len > len(a)
    base = 2 * MAX_CHAR
    # if combined lemma, order after all other
    r = 1 if V_LEMMA_SEP in a else 0
    for ch in a:
        r = r * base + int(2 * _ord(ch))
        # print("%s%d"%(ch,r))
    # print(max_len - len(a))
    r *= base ** (max_len - len(a))
    # print(r)
    return r


def extract_letters(corpus: List[List[str]], col: int) -> Dict[str, int]:
    letters = SortedSet()
    for row in corpus:
        if row[col]:
            letters = letters.union(
                [ch for ch in unicodedata.normalize("NFKC", row[col].lower())]
            )
    return {l: ord(l) for l in letters}


def main_source(lang: str, alt: bool):
    """Returns the main source according to language, i.e. S for sl and C for gr.
    In cases where address is 1/W168a34, the main source needs to become W."""
    if lang == TO_LANG:
        return MAIN_GR
    assert lang == FROM_LANG
    if alt:
        return ALT_SL
    return MAIN_SL


def subscript(cnt: int, lang: str) -> str:
    if cnt == 1:
        return ""
    if lang == FROM_LANG:
        return chr(ord("0") + cnt)
    return chr(ord("α") + cnt - 1)
