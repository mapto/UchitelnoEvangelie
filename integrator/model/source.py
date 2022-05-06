from typing import Dict, List, Optional, Set

import re

from const import VAR_SOURCES, VAR_SEP
from config import FROM_LANG, TO_LANG


class Source:
    """Represents a list of sources, could be one or two letter symbols"""

    src: str = ""

    def __init__(self, other=None) -> None:
        if type(other) == str:
            self.src = other
        elif type(other) == Source:
            self.src = other.src

    def _sort_vars(self) -> str:
        """
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
        res = ""
        for lang in [FROM_LANG, TO_LANG]:
            for s in Source(VAR_SOURCES[lang]):
                if s in self:
                    res += str(s)
        return res

    def values(self) -> Set[str]:
        """
        >>> Source('MP').values() == {'P', 'M'}
        True
        >>> Source('MPaPb').values() == {'Pb', 'Pa', 'M'}
        True
        """
        split = set()
        prev = ""
        for c in self.src:
            if c == c.lower():
                split.add(prev + c)
                prev = ""
            else:
                if prev:
                    split.add(prev)
                prev = c
        if prev:
            split.add(prev)
        return split

    def __eq__(self, other) -> bool:
        """
        >>> Source('A') == Source('B')
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
        return self._sort_vars() == Source(other)._sort_vars()

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __str__(self) -> str:
        return self._sort_vars()

    def __repr__(self) -> str:
        return f"Source('{self.src}')"
        # return f"'{self.src}'"

    def __len__(self) -> int:
        return len(self.src)

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
        result = []
        rest = self.src.replace(VAR_SEP, "")
        iter_regex = r"^([A-Z][a-z0-9]?)(.*)$"
        found = re.match(iter_regex, rest)
        while found and found.group(1):
            result += [found.group(1)]
            rest = found.group(2)
            found = re.match(iter_regex, rest)
        return iter(result)

    def __contains__(self, other) -> bool:
        """
        >>> Source('GH') in Source('GWH')
        True
        >>> Source('HW') in Source('WH')
        True
        >>> Source('WH') in Source('HW')
        True
        >>> Source('PaPb') in Source('MPaPb')
        True
        >>> Source('MP') in Source('MPaPb')
        False
        >>> Source('D') in Source('GWH')
        False
        """
        if len(other) > len(self):
            return False
        return all(c in self.values() for c in Source(other).values())

    def __bool__(self) -> bool:
        """
        >>> True if Source() else False
        False
        >>> True if Source("") else False
        False
        >>> True if Source("A") else False
        True
        """
        return bool(self.src.strip())

    def inside(self, iterable) -> Optional["Source"]:
        """
        >>> Source("A").inside([Source("AB"), Source("C")])
        Source('AB')
        >>> Source("A").inside({Source("AB"): 1, Source("C"): 2})
        Source('AB')
        >>> Source("F").inside("ABCDEF")
        Source('ABCDEF')
        >>> Source("AF").inside(["ABCDEF"])
        Source('ABCDEF')
        >>> Source("A").inside([Source("AB"), Source("C")])
        Source('AB')
        >>> Source("Pz").inside(Source("PwPxPyPz"))
        Source('PwPxPyPz')
        >>> Source("").inside([Source("")])
        Source('')
        >>> Source("").inside([Source("A")])
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
