#!/usr/bin/env python3
"""These utilities are also used by the object-oriented model,
so to avoid circular references they cannot use it"""


from typing import Dict, List, Set, Tuple
import unicodedata
from sortedcontainers import SortedSet, SortedDict  # type: ignore

from model import Path, Source, Alignment


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


def extract_letters(corpus: List[List[str]], col: int) -> Dict[str, int]:
    letters = SortedSet()
    for row in corpus:
        if row[col]:
            letters = letters.union(
                [ch for ch in unicodedata.normalize("NFKC", row[col].lower())]
            )
    return {l: ord(l) for l in letters}


def collect(group: List[List[str]], col: int) -> List[str]:
    """Collects the actual content in the group column"""
    return [group[i][col] for i in range(len(group)) if group[i][col]]


def remove_repetitions(src: str = "") -> str:
    split = set()
    prev = ""
    for c in src:
        if c == c.lower():
            split.add(prev + c)
            prev = ""
        else:
            split.add(prev)
            prev = c
    if prev:
        split.add(prev)
    return "".join(split)


def regroup(d: Dict[Source, str], glue: str = " ") -> Dict[Source, str]:
    """
    >>> regroup({Source('H'): 'шьств\ue205ꙗ', Source('G'): 'шьст\ue205ꙗ', Source('GH'): 'пꙋт\ue205'})
    {Source('G'): 'шьст\ue205ꙗ пꙋт\ue205', Source('H'): 'шьств\ue205ꙗ пꙋт\ue205'}
    >>> regroup({Source('H'): 'шьств\ue205\ue201', Source('G'): 'шьст\ue205\ue201', Source('GH'): 'пѫть'}, " & ")
    {Source('G'): 'шьст\ue205\ue201 & пѫть', Source('H'): 'шьств\ue205\ue201 & пѫть'}
    >>> regroup({Source('G'): 'престьнц б•', Source('H'): 'престнц б•', Source('W'): 'боудемь W'})
    {Source('G'): 'пр\ue205\ue20dестьн\ue205ц\ue205 б•', Source('H'): 'пр\ue205\ue20dестн\ue205ц\ue205 б•', Source('W'): 'боудемь W'}
    >>> regroup({Source('H'): 'ход\ue205т\ue205 с пѣн\ue205\ue201мь', Source('WG'): 'хⷪ҇домь спѣюще'})
    {Source('WG'): 'хⷪ҇домь спѣюще', Source('H'): 'ход\ue205т\ue205 с пѣн\ue205\ue201мь'}
    >>> regroup({Source('WG'): 'хⷪ҇домь спѣюще', Source('H'): 'ход\ue205т\ue205 с пѣн\ue205\ue201мь'})
    {Source('WG'): 'хⷪ҇домь спѣюще', Source('H'): 'ход\ue205т\ue205 с пѣн\ue205\ue201мь'}
    """
    if not d:
        return d
    basic = []
    compound = []
    for l in d.keys():
        b = True
        for s in d.keys():
            if s != l and s in l:
                b = False
        if b:
            basic += [l]
        else:
            compound += [l]

    result: Dict[Source, List[str]] = SortedDict({s: [d[s]] for s in basic})
    for l in compound:
        for s in basic:
            if s in l and d[l]:
                result[s] += [d[l]]
    return {k: glue.join(result[k]) for k in reversed(result) if result[k]}


def _add_usage(
    val: Alignment, nxt: Path, key: Tuple[str, str], d: SortedDict
) -> SortedDict:
    """*IN PLACE*"""
    path = str(nxt)
    if path in d:
        if key not in d[path]:
            d[path][key] = SortedSet()
        d[path][key].add(val)
    else:
        d[path] = {key: SortedSet([val])}
    return d
