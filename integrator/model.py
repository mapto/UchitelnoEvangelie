from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

import re

from const import PATH_SEP, SPECIAL_CHARS

from util import base_word

from address import Index


@dataclass(frozen=True)
class Source:
    """Represents a list of sources, could be one or two letter symbols"""

    src: str = ""

    def _sort_vars(self) -> str:
        """
        >>> Source('WGH')._sort_vars()
        'GHW'
        >>> Source('PbPa')._sort_vars()
        'PaPb'
        >>> Source('CMB')._sort_vars()
        'BCM'
        >>> Source('WH')._sort_vars()
        'HW'
        >>> Source('HW')._sort_vars()
        'HW'
        """
        return "".join(sorted(self.values()))

    def values(self) -> Set[str]:
        split = set()
        prev = ""
        for c in self.src:
            if c == c.lower():
                split.add(prev + c)
                prev = ""
            else:
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
        return self._sort_vars() == Source(str(other))._sort_vars()

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __str__(self) -> str:
        return self.src

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
        # print("-"*8)
        # print(self._sort_vars())
        # print((self._sort_vars()).__hash__())
        # print(hash((self._sort_vars())))
        return hash(self._sort_vars())

    def __iter__(self):
        return iter(self.src)

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
        return all(c in self.values() for c in Source(str(other)).values())

    def __bool__(self) -> bool:
        """
        >>> True if Source() else False
        False
        >>> True if Source("") else False
        False
        >>> True if Source("A") else False
        True
        """
        return bool(self.src)

    def inside(self, iterable) -> Optional["Source"]:
        """
        >>> Source("A").inside([Source("AB"), Source("C")])
        Source('AB')
        >>> Source("A").inside({Source("AB"): 1, Source("C"): 2})
        Source('AB')
        >>> Source("F").inside(["ABCDEF"])
        'ABCDEF'
        >>> Source("AF").inside(["ABCDEF"])
        'ABCDEF'
        >>> Source("A").inside([Source("AB"), Source("C")])
        Source('AB')
        """
        for i in iterable:
            if Source(str(self)) in Source(str(i)):
                return i
        return None


@dataclass(frozen=True)
class Alternative:
    """Word occurences in a line are counted.
    For main alternative this is in a separate variable,
    but for variants, it's part of the dictionary"""

    main_lemma: str = ""
    var_lemmas: Dict[Source, str] = field(default_factory=lambda: {})
    main_word: str = ""
    var_words: Dict[Source, Tuple[str, int]] = field(default_factory=lambda: {})
    main_cnt: int = 1

    def __bool__(self) -> bool:
        return bool(self.main_lemma) or bool(self.var_lemmas)


@dataclass(frozen=True)
class Usage:
    """Variant is not only indicative, but also nominative - which variant.
    Here alt means other other transcriptions (main or var).
    Contrast these to Index"""

    idx: Index
    lang: str
    var: Source = field(default_factory=lambda: Source(""))
    orig_alt: Alternative = field(default_factory=lambda: Alternative())
    trans_alt: Alternative = field(default_factory=lambda: Alternative())

    def __hash__(self):
        return hash((self.idx, self.lang, self.var))

    def __lt__(self, other) -> bool:
        return (
            self.idx < other.idx
            or self.idx == other.idx
            and len(self.var) < len(other.var)
        )

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other


@dataclass
class Path:
    """The full collection of lemmas is considered a backtracking path in the final usage hierarchy.
    Gramatical annotation is handled exceptionally.
    """

    parts: List[str] = field(default_factory=lambda: [])
    annotation: str = ""

    def __iadd__(self, s: str):
        self.parts += [s]
        return self

    def __len__(self):
        return len(self.parts)

    def __contains__(self, item: str):
        return item in self.parts or item == self.annotation

    def __str__(self):
        """We want to see results in reverse order.
        Also, if last part is special character, display it smarter"""
        parts = self.parts.copy()
        if parts:
            if parts[-1][0] in SPECIAL_CHARS and parts[-1].endswith(parts[-2]):
                parts.pop(-2)
            content = PATH_SEP.join(parts[::-1])
            return f"{content} {self.annotation}" if self.annotation else content
        return self.annotation if self.annotation else ""

    def compile(self):
        """Remove empty steps, extract annotations"""
        for cur in range(len(self.parts) - 1, -1, -1):
            if not self.parts[cur]:
                self.parts.pop(cur)
            elif re.match(r"^[a-zA-z\.]+$", self.parts[cur]):
                self.annotation = self.parts.pop(cur)


@dataclass
class Counter:
    orig_main: Set[Index] = field(default_factory=lambda: set())
    orig_var: Set[Index] = field(default_factory=lambda: set())
    trans_main: Set[Index] = field(default_factory=lambda: set())
    trans_var: Set[Index] = field(default_factory=lambda: set())

    def __iadd__(self, other: "Counter") -> "Counter":
        self.orig_main = self.orig_main.union(other.orig_main)
        self.orig_var = self.orig_var.union(other.orig_var)
        self.trans_main = self.trans_main.union(other.trans_main)
        self.trans_var = self.trans_var.union(other.trans_var)
        return self

    def get_counts(self, trans: bool = False) -> Tuple[int, int]:
        if trans:
            return (len(self.trans_main), len(self.trans_var))
        return (len(self.orig_main), len(self.orig_var))
