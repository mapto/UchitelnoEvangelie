from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from abc import abstractmethod

import re

from const import PATH_SEP, SPECIAL_CHARS, PRIMES, PRIME_MAP
from const import idx_regex

from util import base_word


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


@dataclass(order=True, frozen=True)
class Index:
    """Index only indicates if it is from a variant.
    Alternative variable (alt) means alternative indexing (as in Vienna scroll).
    Not related to alternative variants
    Contrast these to Usage."""

    ch: int
    alt: bool
    page: int
    col: str
    row: int
    ocnt: int = 1
    tcnt: int = 1
    end: Optional["Index"] = None
    bold: bool = False
    italic: bool = False
    word: str = ""

    @staticmethod
    def unpack(
        value: str,
        b: bool = False,
        i: bool = False,
        word: str = "",
        ocnt: int = 1,
        tcnt: int = 1,
    ) -> "Index":
        """
        Parsing the format produced by exporter or merger.
        Thus, repetition indices external to the string,
        as they are stored in a separate column in the spreadsheet
        Regex using: https://regex101.com/
        """
        # TODO: derive regex from parts
        m = re.search(
            idx_regex,
            value,
        )
        assert m
        # print(m.groups())
        ch = int(m.group(1))
        # alt puts W at end of ch1 and at start of ch2
        alt = (bool(m.group(2)) if ch % 2 else not m.group(2)) if ch < 3 else False
        page = int(m.group(3))
        col = m.group(4)
        row = int(m.group(5))
        # cnt = PRIME_MAP[m.group(6)] if m.group(6) else 1
        end = None
        if m.group(16):
            e_ch = ch
            e_alt = alt
            e_page = page
            e_col = col
            e_row = int(m.group(16))
            # e_cnt = PRIME_MAP[m.group(18)] if m.group(18) else 1
            # e_var = m.group(18)
            if m.group(15):
                e_col = m.group(15)
                if m.group(14):
                    e_page = int(m.group(14))
                    if m.group(12):
                        e_ch = int(m.group(12))
                    e_alt = (
                        (bool(m.group(13)) if e_ch % 2 else not m.group(13))
                        if e_ch < 3
                        else False
                    )
            end = Index(
                e_ch,
                e_alt,
                e_page,
                e_col,
                e_row,
                ocnt,
                tcnt,
                bold=b,
                italic=i,
                word=word,
            )
        return Index(ch, alt, page, col, row, ocnt, tcnt, end, b, i, word=word)

    def __str__(self):
        """
        >>> str(Index(1, False, 6, "c", 4, end=Index(1, False, 6, "d", 4)))
        '1/6c4-d4'
        >>> str(Index(1, False, 6, "c", 4, end=Index(1, False, 6, "c", 11)))
        '1/6c4-11'

        Variants are not shown:
        >>> str(Index(1, False, 6, "c", 4, end=Index(1, False, 6, "d", 4)))
        '1/6c4-d4'

        >>> str(Index(1, True, 6, "c", 4))
        '1/W6c4'
        >>> str(Index(2, False, 6, "c", 4))
        '2/W6c4'
        """
        w = "W" if self.ch < 3 and bool(self.ch % 2) == self.alt else ""
        # TODO: distinguish between symbold for ocnt and tcnt
        cnt = PRIMES[self.ocnt - 1] + PRIMES[self.tcnt - 1]
        start = f"{self.ch}/{w}{self.page}{self.col}{self.row}{cnt}"
        if self.end:
            if self.end.ch != self.ch:
                return f"{start}-{str(self.end)}"
            ecnt = PRIMES[self.end.ocnt - 1]
            if self.end.alt != self.alt:
                ew = "W" if self.end.ch < 3 and self.end.alt and self.end.ch % 2 else ""
                return f"{start}-{ew}{self.end.page}{self.end.col}{self.end.row}{ecnt}"
            if self.end.page != self.page:
                return f"{start}-{self.end.page}{self.end.col}{self.end.row}{ecnt}"
            if self.end.col != self.col:
                return f"{start}-{self.end.col}{self.end.row}{ecnt}"
            if self.end.row != self.row:
                return f"{start}-{self.end.row}{ecnt}"
            if self.end.ocnt != self.ocnt:
                return f"{start}-{self.end.row}{ecnt}"
        return start

    def longstr(self):
        """
        >>> Index(1, False, 6, "c", 4, end=Index(2, True, 6, "c", 4)).longstr()
        '01/006c04-02/006c04'

        >> Index(1, False, 6, "c", 4, Index(2, True, 6, "c", 4)).longstr()
        '01/006c04WH-02/006c04'
        >> Index(1, False, 6, "c", 4, end=Index(2, True, 6, "c", 4)).longstr()
        '01/006c04-02/006c04WH'
        """
        w = "W" if self.ch < 3 and bool(self.ch % 2) == self.alt else ""
        cnt = PRIMES[self.ocnt - 1]
        start = f"{self.ch:02d}/{w}{self.page:03d}{self.col}{self.row:02d}{cnt}"
        if self.end:
            if self.end.ch != self.ch:
                return f"{start}-{self.end.longstr()}"
            ecnt = PRIMES[self.end.ocnt - 1]
            if self.end.alt != self.alt:
                ew = "W" if self.end.ch < 3 and self.end.alt and self.end.ch % 2 else ""
                return f"{start}-{ew}{self.end.page:03d}{self.end.col}{self.end.row:02d}{ecnt}"
            if self.end.page != self.page:
                return (
                    f"{start}-{self.end.page:03d}{self.end.col}{self.end.row:02d}{ecnt}"
                )
            if self.end.col != self.col:
                return f"{start}-" f"{self.end.col}{self.end.row:02d}{ecnt}"
            if self.end.row != self.row:
                return f"{start}-{self.end.row:02d}{ecnt}"
        return start


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

    def __eq__(self, other) -> bool:
        return self.idx == other.idx and len(self.var) == len(other.var)

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
