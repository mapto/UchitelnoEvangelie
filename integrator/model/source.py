from typing import Dict, List, Optional, Set

from config import FROM_LANG, TO_LANG, VAR_SOURCES


def _values(src: str) -> List[str]:
    """
    >>> _values(VAR_SOURCES[FROM_LANG] + VAR_SOURCES[TO_LANG])
    ['W', 'G', 'H', 'Cs', 'Ab', 'Fa', 'Fb', 'Fc', 'La', 'M', 'Mi', 'Md', 'Pb', 'Pc', 'Pd', 'Pe', 'Pf', 'Pg', 'Ph', 'Pi', 'Pk', 'Pl', 'Pp', 'R', 'T', 'V', 'Va', 'Vb', 'Vc', 'Vd', 'Y', 'Za', 'A', 'Fd', 'L', 'Ma', 'B', 'P', 'Pa', 'Po', 'Sp', 'Z', 'Pm', 'Pn', 'Ve', 'Ch', 'Nt', 'S']
    >>> _values('MB')
    ['M', 'B']
    >>> _values('V')
    ['V']
    """
    split = []
    prev = ""
    for c in src:
        if c.islower() or c.isnumeric():
            split += [prev + c]
            prev = ""
        else:
            if prev:
                split += [prev]
            prev = c
    if prev:
        split += [prev]
    return split


# ORDERED_SOURCES = _values(VAR_SOURCES[FROM_LANG] + VAR_SOURCES[TO_LANG])
ORDERED_SOURCES = VAR_SOURCES[FROM_LANG] + VAR_SOURCES[TO_LANG]


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


class Source:
    """Represents a list of sources, could be one or two letter symbols
    >>> Source('MB').data
    ['M', 'B']
    >>> Source('D')
    Traceback (most recent call last):
    ...
    KeyError: "Source unknown: ['D']"
    """

    src: str = ""
    data: List[str] = []

    def __init__(self, other=None) -> None:
        if type(other) == list or type(other) == set:
            self.src = remove_repetitions("".join(other))
        elif type(other) == str:
            self.src = remove_repetitions(other)
        elif type(other) == Source:
            self.src = other.src
        raw_values = _values(self.src.replace("-", ""))
        if not all([s in ORDERED_SOURCES for s in raw_values]):
            out = [s for s in raw_values if s not in ORDERED_SOURCES]
            raise KeyError(f"Source unknown: {out}")
        self.data = [v for v in ORDERED_SOURCES if v in raw_values]

    def _sort_vars(self) -> str:
        """
        >>> Source('Ch')._sort_vars()
        'Ch'
        >>> Source('GHW')._sort_vars()
        'WGH'
        >>> Source('PaPb')._sort_vars()
        'PbPa'
        >>> Source('CsMBSpCh')._sort_vars()
        'CsMBSpCh'
        >>> Source('WH')._sort_vars()
        'WH'
        >>> Source('CsMBSpChHW')._sort_vars()
        'WHCsMBSpCh'
        """
        return "".join(self.data)

    def values(self) -> List[str]:
        """
        >>> Source('MB').values()
        ['M', 'B']
        >>> Source('MPaPb').values()
        ['M', 'Pb', 'Pa']
        """
        return self.data

    def __eq__(self, other) -> bool:
        """
        >>> Source('M') == Source('L')
        False
        >>> Source('HW') == Source('WH')
        True
        >>> hash(Source('HW')) == hash(Source('HW'))
        True
        >>> hash(Source('HW')) == hash(Source('WH'))
        True
        >>> Source('HW') in {Source('HW')}
        True
        >>> Source('HW') in {Source('WH')}
        True
        >>> Source('HW') in {Source('WH'): '\ue201д\ue205но\ue20dѧдъ'}
        True
        """
        if type(other) not in [Source, str]:
            return False
        return self.data == Source(other).data

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __str__(self) -> str:
        return self._sort_vars()

    def __repr__(self) -> str:
        return f"Source('{self}')"
        # return f"'{self.src}'"

    def __len__(self) -> int:
        if not self.src:
            return len("".join(VAR_SOURCES))
        l = 0
        for s in self:
            l += 1
        return l

    def __add__(self, other) -> "Source":
        """
        >>> (Source('G') + 'W')._sort_vars()
        'WG'
        """
        # this if serves only to enable the sum() function
        if type(other) == int and other == 0:
            return self
        return Source(self.src + str(other))

    def __radd__(self, other) -> "Source":
        return self + other

    def __sub__(self, other) -> "Source":
        """
        >>> Source("WGH") - "G"
        Source('WH')
        >>> Source("PPaPb") - "Pa"
        Source('PbP')
        >>> Source("PPaPb") - "P"
        Source('PbPa')
        >>> Source("PPaPb") - "M"
        Source('PbPPa')
        >>> Source("WGHPPaPb") - "GP"
        Source('WHPbPa')
        """
        result = ""
        sother = Source(other)
        for lang in [FROM_LANG, TO_LANG]:
            # print(lang)
            if self.has_lang(lang) and sother.has_lang(lang):
                mine = self.by_lang(lang)
                # print(mine, sother.by_lang(lang))
                for s in mine:
                    if s not in sother.by_lang(lang):
                        result += s
                # print(result)
        return Source(result)

    def __invert__(self):
        """
        >>> ~Source('WG')
        Source('H')
        """
        return Source(ORDERED_SOURCES) - self

    def __hash__(self) -> int:
        """
        >>> hash(Source('WH')) == hash(Source('HW'))
        True
        """
        return hash(self._sort_vars())

    def __iter__(self):
        """
        >>> [x for x in Source('BCsMSpCh')]
        ['Cs', 'M', 'B', 'Sp', 'Ch']
        >>> [x for x in Source('WGH-BCsMSpCh')]
        ['W', 'G', 'H', 'Cs', 'M', 'B', 'Sp', 'Ch']
        """
        # if not self.data:
        #     return ()
        # return (Source(i) for i in self.data)
        return iter(self.data)

    def __contains__(self, other) -> bool:
        """
        >> Source('Ch') in Source('Ch')
        True
        >> Source('GH') in Source('GWH')
        True
        >> Source('HW') in Source('WH')
        True
        >> Source('WH') in Source('HW')
        True
        >> Source('PaPb') in Source('MPaPb')
        True
        >> Source('MP') in Source('MPaPb')
        False
        >>> Source('V') in Source('Vd')
        False
        >>> Source('M') in Source('GWH')
        False
        >>> Source() in Source()
        True
        """
        if type(other) == str:
            other = Source(other)
        if len(other) > len(self):
            return False
        return all(c in self.values() for c in other.values())

    def __bool__(self) -> bool:
        """
        >>> True if Source() else False
        False
        >>> True if Source("") else False
        False
        >>> True if Source("G") else False
        True
        """
        return bool(self.src.strip())

    def __list__(self) -> List[str]:
        return self.data

    def __lt__(self, other) -> bool:
        """
        >>> Source("WHPaPb") > Source("WHPaPb")
        False
        >>> Source("WHPaPb") > Source("WHPa")
        True
        >>> Source("WHPb") < Source("WHPa")
        True
        """
        if len(other) > len(self):
            return True
        if len(other) < len(self):
            return False

        s = list(self)
        o = list(other)
        for i in range(len(s)):
            if o[i] > s[i]:
                return False
            if o[i] < s[i]:
                return True

        return False

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other

    def inside(self, iterable) -> Optional["Source"]:
        """
        >>> Source("G").inside([Source("GH"), Source("W")])
        Source('GH')
        >>> Source("G").inside({Source("GH"): 1, Source("W"): 2})
        Source('GH')
        >>> Source("Pf").inside("PaPbPcPdPePf")
        Source('PbPcPdPePfPa')
        >>> Source("PaPf").inside(["PaPbPcPdPePf"])
        Source('PbPcPdPePfPa')
        >>> Source("Pa").inside([Source("PaPb"), Source("Pc")])
        Source('PbPa')
        >>> Source("Pk").inside(Source("PkPmPnPo"))
        Source('PkPoPmPn')
        >>> Source("").inside([Source("")])
        Source('')
        >>> Source("").inside([Source("G")])
        """
        if type(iterable) == str:
            iterable = Source(iterable)
        if type(iterable) == list and all(type(e) == str for e in iterable):
            iterable = Source(iterable)
        if type(iterable) == Source:
            iterable = [iterable]
        if not self.src:
            for i in iterable:
                if not i:
                    return Source("")
            return None
        for i in iterable:
            if Source(self) in Source(i):
                return Source(i)
        return None

    def remainder(self, iterable) -> Optional["Source"]:
        """
        >> Source('GH').remainder([Source('G'), Source('H')])
        None
        >>> Source('GH').remainder([])
        Source('GH')
        >>> Source('WGH').remainder([Source('WH')])
        Source('G')
        >>> Source('WG').remainder([Source('H')])
        Source('WG')
        """
        result = []
        for before in self:
            inside = False
            for after in iterable:
                if Source(before).inside(after):
                    inside = True
                    break
            if not inside:
                result += [before]
        if len(result) > 0:
            return Source(result)
        return None

    def has_lang(self, lang: str) -> bool:
        """
        >>> Source("WPb").has_lang("sl")
        True
        >>> Source("WPb").has_lang("gr")
        True
        >>> Source("WGH").has_lang("sl")
        True
        >>> Source("WGH").has_lang("gr")
        False
        >>> Source("MPb").has_lang("sl")
        False
        >>> Source("MPb").has_lang("gr")
        True
        """
        for s in self:
            if Source(s).inside(Source(VAR_SOURCES[lang])):
                return True
        return False

    def by_lang(self, lang: str) -> "Source":
        """
        >>> Source("MPo").by_lang("gr")
        Source('MPo')
        >>> Source("WPb").by_lang("sl")
        Source('W')
        >>> Source("MPb").by_lang("gr")
        Source('MPb')
        >>> Source("HG").by_lang("sl")
        Source('GH')
        >>> Source("CsMBSpChHW").by_lang("sl")
        Source('WH')
        >>> Source("CsMBSpChHW").by_lang("gr")
        Source('CsMBSpCh')
        >>> Source("WGH").by_lang("sl")
        Source('WGH')
        >>> Source("GHW").by_lang("sl")
        Source('WGH')
        """
        res = ""
        for s in Source(VAR_SOURCES[lang]):
            if s in self:
                res += str(s)
        return Source(res)

    def key(self) -> int:
        """Sorting key for SortedDict"""
        if not self.data:
            return 0
        return ORDERED_SOURCES.index(self.data[0])
        # return len(ORDERED_SOURCES) - ORDERED_SOURCES.index(self.data[0])
