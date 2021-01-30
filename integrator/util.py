from typing import List, Set

from alphabet import remap

max_char = ord("ѵ") - ord("α") + 1
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
    if a in remap:
        return remap[a] - ord("α")
    return ord(a) - ord("α")


def cmp_chr(a: str, b: str) -> int:
    """
    >>> cmp_chr("а", "б")
    -1

    >>> cmp_chr("", "к")
    -1

    >>> cmp_chr("ꙁ", "")
    -1

    >>> sl = "а б в г д е ж ꙃ ꙁ  к л м н о п р с т ѹ ф х ш ц  щ ъ ꙑ ь ѣ ю ꙗ  ѧ ѫ ѩ ѭ ѯ ѱ ѳ у"
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

    return 0 if _ord(a) - _ord(b) == 0 else 1 if _ord(a) - _ord(b) > 0 else -1
    # return _ord(a) - _ord(b)


def ord_word(a: str, max_len=max_len) -> int:
    """
    >>> ord_word("свѣтъ",6)
    6956114563282
    >>> ord_word("свѧтъ",6)
    6956122790790
    >>> ord_word("свѣтъ") < ord_word("свѧтъ")
    True
    """
    a = a.lower()
    a.replace("оу", "ѹ")
    assert max_len > len(a)
    base = 2 * max_char
    r = 0
    for ch in a:
        r = r * base + int(2 * _ord(ch))
    r *= (max_len - len(a)) ** base
    return r
