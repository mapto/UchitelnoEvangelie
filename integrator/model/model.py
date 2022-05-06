from typing import Dict, List, Tuple
from dataclasses import dataclass, field

import re

from const import PATH_SEP, SPECIAL_CHARS
from regex import source_regex

from .address import Index
from .source import Source


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
