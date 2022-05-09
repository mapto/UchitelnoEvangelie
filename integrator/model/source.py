from typing import Dict, List, Optional, Set

from const import VAR_SOURCES, VAR_SEP
from config import FROM_LANG, TO_LANG


def _values(src: str) -> List[str]:
    """
    >>> _values(VAR_SOURCES[FROM_LANG] + VAR_SOURCES[TO_LANG])
    ['W', 'G', 'H', 'B', 'C', 'M', 'As', 'Ch', 'P', 'Pa', 'Pb', 'Pc', 'Pd', 'Pe', 'Pf', 'Pg', 'Ph', 'Pi', 'Pj', 'Pk', 'Pl', 'Pm', 'Pn', 'Po', 'Pp', 'Pq', 'Pr', 'Ps', 'Pt', 'Pu', 'Pv', 'Pw', 'Px', 'Py', 'Pz']
    >>> _values('MP')
    ['M', 'P']
    >>> _values('D')
    ['D']
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


ORDERED_SOURCES = _values(VAR_SOURCES[FROM_LANG] + VAR_SOURCES[TO_LANG])


class Source:
    """Represents a list of sources, could be one or two letter symbols
    >>> Source('MP').data
    ['M', 'P']
    >>> Source('D')
    Traceback (most recent call last):
    ...
    KeyError: "Source unknown: ['D']"
    """

    src: str = ""
    data: List[str] = []

    def __init__(self, other=None) -> None:
        if type(other) == str:
            self.src = other
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
        >>> Source('PbPa')._sort_vars()
        'PaPb'
        >>> Source('CMBAsCh')._sort_vars()
        'BCMAsCh'
        >>> Source('WH')._sort_vars()
        'WH'
        >>> Source('CMBAsChHW')._sort_vars()
        'WHBCMAsCh'
        """
        return "".join(self.data)

    def values(self) -> List[str]:
        """
        >>> Source('MP').values()
        ['M', 'P']
        >>> Source('MPaPb').values()
        ['M', 'Pa', 'Pb']
        """
        return self.data

    def __eq__(self, other) -> bool:
        """
        >>> Source('M') == Source('P')
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
        return f"Source('{self.src}')"
        # return f"'{self.src}'"

    def __len__(self) -> int:
        if not self.src:
            return len("".join(VAR_SOURCES.values()))
        l = 0
        for s in self:
            l += 1
        return l

    def __add__(self, other) -> "Source":
        return Source(self.src + str(other))

    def __hash__(self) -> int:
        """
        >>> hash(Source('WH')) == hash(Source('HW'))
        True
        """
        return hash(self._sort_vars())

    def __iter__(self):
        """
        >>> [x for x in Source('BCMAsCh')]
        ['B', 'C', 'M', 'As', 'Ch']
        >>> [x for x in Source('WGH-BCMAsCh')]
        ['W', 'G', 'H', 'B', 'C', 'M', 'As', 'Ch']
        """
        """
        result = []
        rest = self.src.replace(VAR_SEP, "")
        iter_regex = r"^([A-Z][a-z0-9]?)(.*)$"
        found = re.match(iter_regex, rest)
        while found and found.group(1):
            result += [found.group(1)]
            rest = found.group(2)
            found = re.match(iter_regex, rest)
        return iter(result)
        """
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
        for i, x in enumerate(self):
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
        Source('PaPbPcPdPePf')
        >>> Source("PaPf").inside(["PaPbPcPdPePf"])
        Source('PaPbPcPdPePf')
        >>> Source("Pa").inside([Source("PaPb"), Source("Pc")])
        Source('PaPb')
        >>> Source("Pz").inside(Source("PwPxPyPz"))
        Source('PwPxPyPz')
        >>> Source("").inside([Source("")])
        Source('')
        >>> Source("").inside([Source("G")])
        """
        if type(iterable) == str:
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
        >>> Source("MPz").by_lang("gr")
        Source('MPz')
        >>> Source("WPb").by_lang("sl")
        Source('W')
        >>> Source("MPb").by_lang("gr")
        Source('MPb')
        >>> Source("HG").by_lang("sl")
        Source('GH')
        >>> Source("CMBAsChHW").by_lang("sl")
        Source('WH')
        >>> Source("CMBAsChHW").by_lang("gr")
        Source('BCMAsCh')
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