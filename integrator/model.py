from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

import re

from const import PATH_SEP, SPECIAL_CHARS
from const import VAR_SOURCES
from regex import source_regex
from config import FROM_LANG, TO_LANG

from util import base_word

from address import Index


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
        """
        result = []
        iter_regex = r"^([A-Z][a-z0-9]?)(.*)$"
        found = re.match(iter_regex, self.src)
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
        'ABCDEF'
        >>> Source("A").inside([Source("AB"), Source("C")])
        Source('AB')
        >>> Source("Pz").inside(Source("PwPxPyPz"))
        Source('PwPxPyPz')
        """
        if type(iterable) == str:
            iterable = Source(iterable)
        if type(iterable) == Source:
            iterable = [iterable]
        for i in iterable:
            if Source(self) in Source(i):
                return i
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
            if Source(s).inside(VAR_SOURCES[lang]):
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
        """
        res = ""
        for s in Source(VAR_SOURCES[lang]):
            if s in self:
                res += str(s)
        return Source(res)


@dataclass(frozen=True)
class Alternative:
    """Word occurences in a line are counted.
    For main alternative this is in a separate variable,
    but for variants, it's part of the dictionary
    >>> Alternative("аще", main_word="аще") < Alternative("\ue205 conj.", main_word="\ue205")
    True
    """

    main_lemma: str = ""
    var_lemmas: Dict[Source, str] = field(default_factory=lambda: {})
    main_word: str = ""
    var_words: Dict[Source, Tuple[str, int]] = field(default_factory=lambda: {})
    main_cnt: int = 1

    def __bool__(self) -> bool:
        return bool(self.main_lemma) or bool(self.var_lemmas)

    def __lt__(self, other) -> bool:
        if self.main_word < other.main_word:
            return True
        elif self.main_word > other.main_word:
            return False

        self_var_word_keys = str(Source("".join(str(k) for k in self.var_words.keys())))
        other_var_word_keys = str(
            Source("".join(str(k) for k in other.var_words.keys()))
        )
        if self_var_word_keys < other_var_word_keys:
            return True
        elif self_var_word_keys > other_var_word_keys:
            return False

        self_var_word_values = "".join(v[0] for v in self.var_words.values())
        other_var_word_values = "".join(v[0] for v in other.var_words.values())
        if self_var_word_values < other_var_word_values:
            return True
        elif self_var_word_values > other_var_word_values:
            return False

        if self.main_cnt < other.main_cnt:
            return True
        elif self.main_cnt > other.main_cnt:
            return False

        return False

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other


@dataclass(frozen=True)
class Usage:
    """Variant is not only indicative, but also nominative - which variant.
    Here alt means other other transcriptions (main or var).
    Contrast these to Index

    >>> i = Index(1, False, 7, "c", 6, word="om.")
    >>> s = Source("WH")
    >>> a = Usage(i, "gr", s, trans_alt=Alternative("аще", main_word="аще"))
    >>> b = Usage(i, "gr", s, trans_alt=Alternative("\ue205 conj.", main_word="\ue205"))
    >>> a < b
    True

    >>> i1 = Index(5, False, 22, "b", 5, word="оуслышат\ue205 GH")
    >>> i2 = Index(5, False, 22, "b", 5, 2, 2, word="оуслышат\ue205 GH")
    >>> s = Source("GH")
    >>> a = Usage(i1, "sl", s, Alternative("слꙑшат\ue205", main_word="слꙑшат\ue205"))
    >>> b = Usage(i2, "sl", s, Alternative("послꙑшат\ue205", main_word="послꙑшат\ue205"))
    >>> a < b
    True
    """

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
            or self.idx == other.idx
            and len(self.var) == len(other.var)
            and self.orig_alt < other.orig_alt
            or self.idx == other.idx
            and len(self.var) == len(other.var)
            and self.orig_alt == other.orig_alt
            and self.trans_alt < other.trans_alt
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
