#!/usr/bin/env python3
"""These utilities are also used by the object-oriented model,
so to avoid circular references they cannot use it"""


from typing import Dict, List, Set, Tuple
import unicodedata
from sortedcontainers import SortedSet, SortedDict  # type: ignore

from model import Alignment, Alternative, Path, Source


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
    return [group[i][col].strip() for i in range(len(group)) if group[i][col]]


def regroup(d: Dict[Source, str], glue: str = " ") -> Dict[Source, str]:
    """Used in merger/grouper

    >>> regroup({Source('H'): 'шьств\ue205ꙗ', Source('G'): 'шьст\ue205ꙗ', Source('GH'): 'пꙋт\ue205'})
    {Source('G'): 'шьст\ue205ꙗ пꙋт\ue205', Source('H'): 'шьств\ue205ꙗ пꙋт\ue205'}
    >>> regroup({Source('H'): 'шьств\ue205\ue201', Source('G'): 'шьст\ue205\ue201', Source('GH'): 'пѫть'}, " & ")
    {Source('G'): 'шьст\ue205\ue201 & пѫть', Source('H'): 'шьств\ue205\ue201 & пѫть'}
    >>> regroup({Source('G'): 'престьнц б•', Source('H'): 'престнц б•', Source('W'): 'боудемь W'})
    {Source('W'): 'боудемь W', Source('G'): 'пр\ue205\ue20dестьн\ue205ц\ue205 б•', Source('H'): 'пр\ue205\ue20dестн\ue205ц\ue205 б•'}
    >>> regroup({Source('H'): 'ход\ue205т\ue205 с пѣн\ue205\ue201мь', Source('WG'): 'хⷪ҇домь спѣюще'})
    {Source('WG'): 'хⷪ҇домь спѣюще', Source('H'): 'ход\ue205т\ue205 с пѣн\ue205\ue201мь'}
    >>> regroup({Source('WG'): 'хⷪ҇домь спѣюще', Source('H'): 'ход\ue205т\ue205 с пѣн\ue205\ue201мь'})
    {Source('WG'): 'хⷪ҇домь спѣюще', Source('H'): 'ход\ue205т\ue205 с пѣн\ue205\ue201мь'}
    >>> regroup({Source('G'): 'ꙗко обраꙁомь', Source('H'): 'ꙗко \ue205 обраꙁомь', Source('W'): 'ꙗко обраꙁомь'})
    {Source('WG'): 'ꙗко обраꙁомь', Source('H'): 'ꙗко \ue205 обраꙁомь'}
    >>> regroup({Source('Mi'): 'τὰ ἑξῆς', Source('Pc'): 'τὰ ἑξῆς', Source('Pd'): 'τὰ ἑξῆς', Source('Pe'): 'τὰ ἑξῆς', Source('Pg'): 'τὰ ἑξῆς', Source('Ph'): 'τὰ ἑξῆς', Source('Pi'): 'τὰ ἑξῆς', Source('Pk'): 'τὰ ἑξῆς', Source('Pp'): 'τὰ ἑξῆς', Source('T'): 'τὰ ἑξῆς', Source('V'): 'τὰ ἑξῆς', Source('Va'): 'τὰ ἑξῆς', Source('Vb'): 'τὰ ἑξῆς', Source('Vd'): 'τὰ ἑξῆς', Source('Y'): 'τὰ ἑξῆς', Source('Za'): 'τὰ ἑξῆς', Source('A'): 'τὰ ἑξῆς', Source('Fd'): 'τὰ ἑξῆς', Source('L'): 'τὰ ἑξῆς', Source('B'): 'τὰ ἑξῆς', Source('Pa'): 'τὰ ἑξῆς', Source('Po'): 'τὰ ἑξῆς', Source('Sp'): 'τὰ ἑξῆς'})
    {Source('MiPcPdPePgPhPiPkPpTVVaVbVdYZaAFdLBPaPoSp'): 'τὰ ἑξῆς'}
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

    listed: Dict[Source, List[str]] = {s: [d[s]] for s in basic}
    for l in compound:
        for s in basic:
            if s in l and d[l]:
                listed[s] += [d[l]]
    # Complicated for backwards compatibility with python3.7 (see build.sh -> cdrx)
    reversed_sources = reversed(list(listed.keys()))
    result = {k: glue.join(listed[k]) for k in reversed_sources if listed[k]}

    # merge variants that are equal
    flipped: Dict[str, Source] = {}
    for k, v in result.items():
        if v not in flipped:
            flipped[v] = k
        else:
            flipped[v] += k

    return {
        Source(v): k
        for k, v in sorted(flipped.items(), key=lambda x: Source(x[1]).key())
    }


def simplify_alternatives(alts: Dict[Source, Alternative]) -> Dict[Source, Alternative]:
    """Used as post-processing at end of aggregator
    >>> simplify_alternatives({'G': Alternative(word='пр\ue205\ue20dестьн\ue205ц\ue205 быт\ue205', lemmas=['пр\ue205\ue20dѧстьн\ue205къ & бꙑт\ue205', 'пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205'], cnt=1, semantic=''), 'H': Alternative(word='пр\ue205\ue20dестн\ue205ц\ue205 быт\ue205', lemmas=['пр\ue205\ue20dѧстьн\ue205къ & бꙑт\ue205', 'пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205'], cnt=1, semantic='')})
    {Source('GH'): Alternative(word='пр\ue205\ue20dестьн\ue205ц\ue205 быт\ue205 G пр\ue205\ue20dестн\ue205ц\ue205 быт\ue205 H', lemmas=['пр\ue205\ue20dѧстьн\ue205къ & бꙑт\ue205', 'пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205'], cnt=1, semantic='')}

    >>> simplify_alternatives({'G': Alternative(word='шьст\ue205ꙗ пꙋт\ue205', lemmas=['шьст\ue205\ue201 & пѫть', 'шьст\ue205\ue201 пѫт\ue205'], cnt=1, semantic=''), 'H': Alternative(word='шьств\ue205ꙗ пꙋт\ue205', lemmas=['шьств\ue205\ue201 & пѫть', 'шьств\ue205\ue201 пѫт\ue205'], cnt=1, semantic='')})
    {Source('G'): Alternative(word='шьст\ue205ꙗ пꙋт\ue205 G', lemmas=['шьст\ue205\ue201 & пѫть', 'шьст\ue205\ue201 пѫт\ue205'], cnt=1, semantic=''), Source('H'): Alternative(word='шьств\ue205ꙗ пꙋт\ue205 H', lemmas=['шьств\ue205\ue201 & пѫть', 'шьств\ue205\ue201 пѫт\ue205'], cnt=1, semantic='')}

    >>> simplify_alternatives({'G': Alternative(word='хⷪ҇домь спѣюще', lemmas=['ходъ & спѣт\ue205', 'ходомь спѣт\ue205'], cnt=1, semantic=''), 'W': Alternative(word='хⷪ҇домь спѣюще', lemmas=['ходъ & спѣт\ue205', 'ходомь спѣт\ue205'], cnt=1, semantic='')})
    {Source('WG'): Alternative(word='хⷪ҇домь спѣюще WG', lemmas=['ходъ & спѣт\ue205', 'ходомь спѣт\ue205'], cnt=1, semantic='')}

    >>> simplify_alternatives({'G': Alternative(word='шьст\ue205ꙗ пꙋт\ue205', lemmas=['шьст\ue205\ue201', 'шьст\ue205\ue201 пѫт\ue205'], cnt=1, semantic='')})
    {Source('G'): Alternative(word='шьст\ue205ꙗ пꙋт\ue205 G', lemmas=['шьст\ue205\ue201', 'шьст\ue205\ue201 пѫт\ue205'], cnt=1, semantic='')}
    """
    # print(alts)
    sources: dict[str, Source] = {}
    words: dict[str, dict[str, set[Source]]] = {}
    cnts: dict[str, int] = {}
    sems: dict[str, str] = {}
    lemmas: dict[str, list[str]] = {}
    for s, a in alts.items():
        w = a.word
        l = a.lemmas[-1]
        lemmas[l] = a.lemmas
        if l in sources:
            sources[l] += Source(s)
            if w not in words[l]:
                words[l][w] = set()
            words[l][w] |= {s}
            assert (
                a.cnt == cnts[l]
            ), f"Misaligned counts. So far: {a.cnt}, now: {cnts[l]}"
            assert (
                not sems[l] or a.semantic == sems[l]
            ), f"Misaligned semantics. So far: {a.semantic}, now: {sems[l]}"
        else:
            sources[l] = Source(s)
            words[l] = {w: {s}}
            cnts[l] = a.cnt
            sems[l] = a.semantic

    res = SortedDict()
    for l in sources.keys():
        # fwords = SortedDict()
        # for k,v in words[l].items():
        #     fwords[Source(''.join(v))] = k
        fwords = SortedDict(
            {Source("".join(str(v) for v in s)): k for k, s in words[l].items()}
        )
        compiled_words = " ".join(f"{w} {s}" for s, w in fwords.items())
        res[sources[l]] = Alternative(compiled_words, lemmas[l], cnts[l], sems[l])

    # return dict(reversed(res.items()))
    return dict(res.items())


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
