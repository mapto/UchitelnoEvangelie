#!/usr/bin/env python3

from typing import List, Set
import unicodedata
from alphabet import reduce, remap

max_char = ord("ѵ") - ord(" ") + 1
# max([max([len(str(e)) for e in r if e]) for r in i if [e for e in r if e]])

max_len = 65


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
    # if a in reduce:
    #     a = reduce[a]
    if a in remap:
        return remap[a]
    return ord(a)


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


def base_word(w: str) -> str:
    if not w:
        return ""
    w = w.strip()
    # w.replace("оу", "ѹ")
    w = unicodedata.normalize("NFKC", w)
    # return "".join([reduce[c] if c in reduce else c for c in w.strip()])
    return w


def ord_word(w: str, max_len=max_len) -> int:
    """
    >>> ord_word("свѣтъ") < ord_word("свѧтъ")
    True
    >>> ord_word("μαρτυρέω") == ord_word("μαρτυρέω")
    True
    >>> ord_word("διαλεγομαι") < ord_word("διαλεγω") < ord_word("διατριβω")
    True
    >>> ord_word("а conj.") > ord_word("а")
    True
    >>> ord_word("на + Acc.") > ord_word("на")
    True
    >>> ord_word("*") > ord_word(" conj.: н*") > ord_word(" conj.")
    True
    """
    a = base_word(w).lower()
    a.replace("оу", "ѹ")
    assert max_len > len(a)
    base = 2 * max_char
    r = 0
    for ch in a:
        r = r * base + int(2 * _ord(ch))
        # print("%s%d"%(ch,r))
    # print(max_len - len(a))
    r *= base ** (max_len - len(a))
    # print(r)
    return r


if __name__ == "__main__":
    print(ord_word(" conj.: н*"))
    print(ord_word(" conj."))
    print(ord_word("*"))
