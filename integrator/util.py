#!/usr/bin/env python3
"""These utilities are also used by the object-oriented model,
so to avoid circular references they cannot use it"""


from typing import Dict, List, Set
import unicodedata
from const import EMPTY_CH, MAIN_SL, ALT_SL, MAIN_GR, SPECIAL_CHARS, V_LEMMA_SEP
from sortedcontainers import SortedSet  # type: ignore

from alphabet import remap, reduce


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


'''
def cmp_chr(a: str, b: str) -> int:
    """
    >>> cmp_chr("а", "б")
    -1

    >>> cmp_chr("", "к")
    -1

    >>> cmp_chr("ꙁ", "")
    -1

    >>> sl = "а б в г д е ж ꙃ ꙁ \ue205 к л м н о п р с т ѹ ф х ш ц \ue20d щ ъ ꙑ ь ѣ ю ꙗ \ue201 ѧ ѫ ѩ ѭ ѯ ѱ ѳ у"
    >>> sl2 = sl.split()
    >>> sl2.sort(key=_ord)
    >>> sl == " ".join(sl2)
    True

    >>> sl = "а б в г д е ж ꙅ ꙁ і к л м н о п р с т ꙋ ф х ш ц  щ ъ ы ь ѣ ю ꙗ  ѧ ѫ ѩ ѭ ѯ ѱ ѳ ѵ"
    >>> sl2 = sl.split()
    >>> sl2.sort(key=_ord)
    >>> sl == " ".join(sl2)
    True

    >>> sl = "а б в г д е ж ѕ ꙁ и к л м н о п р с т ѹ ф х ш ц  щ ъ ꙑ ь ѣ ю ꙗ  ѧ ѫ ѩ ѭ ѯ ѱ ѳ ѵ"
    >>> sl2 = sl.split()
    >>> sl2.sort(key=_ord)
    >>> sl == " ".join(sl2)
    True

    >>> sl = "α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ ϕ χ ψ ω"
    >>> sl2 = sl.split()
    >>> sl2.sort(key=_ord)
    >>> sl == " ".join(sl2)
    True

    >>> sl = "α β γ δ ε ζ η ϑ ι ϰ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω"
    >>> sl2 = sl.split()
    >>> sl2.sort(key=_ord)
    >>> sl == " ".join(sl2)
    True
    """
    assert len(a) == len(b) == 1

    return 0 if _ord(a) - _ord(b) == 0 else 1 if _ord(a) > _ord(b) else -1
    # return _ord(a) - _ord(b)
'''


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
    a.replace("оу", "ѹ")
    if max_len <= len(a):
        print(a)
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


if __name__ == "__main__":
    print(ord_word(" conj.: н*"))
    print(ord_word(" conj."))
    print(ord_word("*"))


def collect(group: List[List[str]], col: int) -> List[str]:
    """Collects the actual content in the group column"""
    return [group[i][col] for i in range(len(group)) if group[i][col]]


def main_source(lang: str, alt: bool):
    if lang == "gr":
        return MAIN_GR
    assert lang == "sl"
    if alt:
        return ALT_SL
    return MAIN_SL


def subscript(cnt: int, lang: str) -> str:
    if cnt == 1:
        return ""
    if lang == "sl":
        return chr(ord("0") + cnt)
    return chr(ord("α") + cnt - 1)
