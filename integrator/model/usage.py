"""ref to diagram ../docs/usage.png"""

from typing import List
from dataclasses import dataclass, field

from config import other_lang

from .address import Index
from .source import Source
from .model import Alternative


@dataclass(frozen=True)
class Usage:
    """Here alt means other transcriptions (main or var)"""

    lang: str = ""
    var: Source = field(default_factory=lambda: Source())
    alt: Alternative = field(default_factory=lambda: Alternative())
    word: str = ""
    lemmas: List[str] = field(default_factory=lambda: [])
    cnt: int = 1

    # def __eq__(self, other) -> bool:
    #     if type(other) != "Usage":
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
        >>> a = Usage("sl", s, Alternative("аще", main_word="аще"), "om.")
        >>> b = Usage("sl", s, Alternative("\ue205 conj.", main_word="\ue205"), "om.")
        >>> a < b
        True

        >>> s = Source("GH")
        >>> a = Usage("sl", s, Alternative("слꙑшат\ue205", main_word="слꙑшат\ue205"), "оуслышат\ue205 GH")
        >>> b = Usage("sl", s, Alternative("послꙑшат\ue205", main_word="послꙑшат\ue205"), "оуслышат\ue205 GH", cnt=2)
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
    #     return f"Usage({', '.join(params)}, word='{self.word}', lemmas={self.lemmas}{cnt})"


@dataclass(frozen=True)
class Alignment:
    idx: Index
    orig: Usage = field(default_factory=lambda: Usage())
    trans: Usage = field(default_factory=lambda: Usage())
    bold: bool = False
    italic: bool = False

    def __hash__(self):
        return hash((self.idx, self.orig, self.trans))

    def __eq__(self, other) -> bool:
        """
        >>> ta1 = Alternative("\ue201д\ue205но\ue20dѧдъ", {"G": "\ue205но\ue20dѧдъ"})
        >>> ta2 = Alternative("\ue201д\ue205но\ue20dѧдъ", {"H": "\ue201д\ue205нородъ"})
        >>> a = Alignment(Index("1/W168a25"), Usage("gr", word="μονογενοῦς"), Usage("sl", Source("H"), ta1))
        >>> b = Alignment(Index("1/W168a25"), Usage("gr", word="μονογενοῦς"), Usage("sl", Source("G"), ta2))
        >>> a == b
        False

        >> vl = {Source("GH"): "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205"}
        >> vw = {Source("GH"): ("пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G", 1)}
        >> oa1 = Alternative(var_lemmas=vl, var_words=vw)
        >> oa2 = Alternative(main_lemma="пр\ue205\ue20dьтьн\ue205къ быт\ue205", main_word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть")
        >> a = Alignment(Index("5/28c21-d1"), Usage("sl", alt=oa1, word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть"))
        >> b = Alignment(Index("5/28c21-d1"), Usage("sl", Source("GH"), oa2, "пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G"))
        >> a == b
        False
        """
        if type(other) != Alignment:
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
        if type(other) != Alignment:
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
        >>> i = Index("1/7c6")
        >>> s = Source("WH")
        >>> a = Alignment(i, Usage("sl", s, Alternative("аще", main_word="аще"), "om."))
        >>> b = Alignment(i, Usage("sl", s, Alternative("\ue205 conj.", main_word="\ue205"), "om."))
        >>> a < b
        True

        >>> i = Index("5/22b5")
        >>> s = Source("GH")
        >>> a = Alignment(i, Usage("sl", s, Alternative("слꙑшат\ue205", main_word="слꙑшат\ue205"), "оуслышат\ue205 GH"))
        >>> b = Alignment(i, Usage("sl", s, Alternative("послꙑшат\ue205", main_word="послꙑшат\ue205"), "оуслышат\ue205 GH", cnt=2))
        >>> a < b
        True
        """
        return (
            self.idx < other.idx
            or self.idx == other.idx
            and self.orig < other.orig
            or self.idx == other.idx
            and self.orig == other.orig
            and self.trans < other.trans
        )

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other

    # def __repr__(self) -> str:
    #     return f"Alignment({repr(self.idx)}, {self.orig}, {self.trans})"
    #     # return f"Alignment(Index('{repr(self.idx)}'), {self.orig}, {self.trans})"
