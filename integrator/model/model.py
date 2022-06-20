from typing import Dict, List, Tuple
from dataclasses import dataclass, field

import re

from const import PATH_SEP, SPECIAL_CHARS
from config import other_lang
from regex import source_regex

from .address import Index
from .source import Source


@dataclass(frozen=True)
class Alternative:
    """Word occurences in a line are counted.
    For main alternative this is in a separate variable,
    but for variants, it's part of the dictionary
    """

    main_lemma: str = ""
    var_lemmas: Dict[Source, str] = field(default_factory=lambda: {})
    main_word: str = ""
    var_words: Dict[Source, Tuple[str, int]] = field(default_factory=lambda: {})
    main_cnt: int = 1

    def __hash__(self):
        vl = "/".join([f"{v} {k}" for k, v in self.var_lemmas.items()])
        vw = "/".join([f"{v[0]}{v[1]} {k}" for k, v in self.var_words.items()])
        return hash((self.main_lemma, vl, self.main_word, vw, self.main_cnt))

    def __bool__(self) -> bool:
        return bool(self.main_lemma) or bool(self.var_lemmas)

    def __lt__(self, other) -> bool:
        """
        >>> Alternative("аще", main_word="аще") < Alternative("\ue205 conj.", main_word="\ue205")
        True
        """
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
class UsageContent:
    """Here alt means other transcriptions (main or var)"""

    lang: str = ""
    var: Source = field(default_factory=lambda: Source())
    alt: Alternative = field(default_factory=lambda: Alternative())
    word: str = ""
    lemmas: List[str] = field(default_factory=lambda: [])
    cnt: int = 1

    # def __eq__(self, other) -> bool:
    #     if type(other) != "UsageContent":
    #         return False
    #     return (self.lang == other.lang
    #         and self.var == other.var
    #         and self.alt == other.alt
    #         and self.cnt == other.cnt)

    def __hash__(self) -> int:
        return hash(
            (self.lang, self.var, self.alt, self.word, tuple(self.lemmas), self.cnt)
        )

    def __lt__(self, other) -> bool:
        """
        >>> s = Source("WH")
        >>> a = UsageContent("sl", s, Alternative("аще", main_word="аще"), "om.")
        >>> b = UsageContent("sl", s, Alternative("\ue205 conj.", main_word="\ue205"), "om.")
        >>> a < b
        True

        >>> s = Source("GH")
        >>> a = UsageContent("sl", s, Alternative("слꙑшат\ue205", main_word="слꙑшат\ue205"), "оуслышат\ue205 GH")
        >>> b = UsageContent("sl", s, Alternative("послꙑшат\ue205", main_word="послꙑшат\ue205"), "оуслышат\ue205 GH", cnt=2)
        >>> a < b
        True
        """
        return (
            self.cnt < other.cnt
            or self.cnt == other.cnt
            and len(self.var) < len(other.var)
            or self.cnt == other.cnt
            and len(self.var) == len(other.var)
            and self.alt < other.alt
        )

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other

    # def __repr__(self) -> str:
    #     params = [f'"{self.lang}"']
    #     if self.var:
    #         params += [f"var={repr(self.var)}"]
    #     if self.alt:
    #         params += [f"alt={self.alt}"]
    #     cnt = f", cnt={self.cnt}" if self.cnt > 1 else ""
    #     return f"UsageContent({', '.join(params)}, word='{self.word}', lemmas={self.lemmas}{cnt})"


@dataclass(frozen=True)
class Usage:
    idx: Index
    orig: UsageContent = field(default_factory=lambda: UsageContent())
    trans: UsageContent = field(default_factory=lambda: UsageContent())
    bold: bool = False
    italic: bool = False

    def __hash__(self):
        return hash((self.idx, self.orig, self.trans))

    def __eq__(self, other) -> bool:
        """
        >>> ta1 = Alternative("\ue201д\ue205но\ue20dѧдъ", {"G": "\ue205но\ue20dѧдъ"})
        >>> ta2 = Alternative("\ue201д\ue205но\ue20dѧдъ", {"H": "\ue201д\ue205нородъ"})
        >>> a = Usage(Index.unpack("1/W168a25"), UsageContent("gr", word="μονογενοῦς"), UsageContent("sl", Source("H"), ta1))
        >>> b = Usage(Index.unpack("1/W168a25"), UsageContent("gr", word="μονογενοῦς"), UsageContent("sl", Source("G"), ta2))
        >>> a == b
        False

        >> vl = {Source("GH"): "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205"}
        >> vw = {Source("GH"): ("пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G", 1)}
        >> oa1 = Alternative(var_lemmas=vl, var_words=vw)
        >> oa2 = Alternative(main_lemma="пр\ue205\ue20dьтьн\ue205къ быт\ue205", main_word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть")
        >> a = Usage(Index.unpack("5/28c21-d1"), UsageContent("sl", alt=oa1, word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть"))
        >> b = Usage(Index.unpack("5/28c21-d1"), UsageContent("sl", Source("GH"), oa2, "пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G"))
        >> a == b
        False
        """
        if type(other) != Usage:
            return False
        return (
            self.idx == other.idx
            and self.orig == other.orig
            and self.trans == other.trans
            and self.orig == other.orig
            and self.trans == other.trans
        )

    def var(self) -> Source:
        return self.orig.var + self.trans.var

    def colocated(self, other, transl: bool = False):
        """
        A loose type of coincidence, used for occurence counting:
        if the same lemma and in the same language-specific address, considering also repetitions,
        usage should not be counted a second time
        see counter.py::_present
        """
        if type(other) != Usage:
            return False
        mine = self.orig
        hers = other.orig
        # wordmatch = self.trans.word == other.trans.word if transl else mine.word == hers.word
        # mine = self.trans if transl else self.orig
        # hers = other.trans if transl else other.orig
        l = self.orig.lang
        return (
            self.idx == other.idx
            and l == hers.lang
            and bool(self.var().by_lang(l)) == bool(other.var().by_lang(l))
            and mine.word == hers.word
            and mine.lemmas == hers.lemmas
            and mine.cnt == hers.cnt
        )

    def __lt__(self, other) -> bool:
        """
        >>> i = Index(1, False, 7, "c", 6)
        >>> s = Source("WH")
        >>> a = Usage(i, UsageContent("sl", s, Alternative("аще", main_word="аще"), "om."))
        >>> b = Usage(i, UsageContent("sl", s, Alternative("\ue205 conj.", main_word="\ue205"), "om."))
        >>> a < b
        True

        >>> i = Index(5, False, 22, "b", 5)
        >>> s = Source("GH")
        >>> a = Usage(i, UsageContent("sl", s, Alternative("слꙑшат\ue205", main_word="слꙑшат\ue205"), "оуслышат\ue205 GH"))
        >>> b = Usage(i, UsageContent("sl", s, Alternative("послꙑшат\ue205", main_word="послꙑшат\ue205"), "оуслышат\ue205 GH", cnt=2))
        >>> a < b
        True
        """
        return self.idx < other.idx or self.idx == other.idx and self.orig < other.orig

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other

    # def __repr__(self) -> str:
    #     return f"Usage({repr(self.idx)}, {self.orig}, {self.trans})"
    #     # return f"Usage(Index.unpack('{repr(self.idx)}'), {self.orig}, {self.trans})"


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
