"""ref to diagram ../docs/usage.png"""

from typing import Dict, List
from dataclasses import dataclass, field


from .address import Index
from .source import Source
from .model import Alternative


@dataclass(frozen=True)
class Usage:
    """Here alt means other transcriptions (main or var)"""

    lang: str = ""
    var: Source = field(default_factory=lambda: Source())
    word: str = ""
    lemmas: List[str] = field(default_factory=lambda: [])
    cnt: int = 1
    main_alt: Alternative = field(default_factory=lambda: Alternative())
    var_alt: Dict[Source, Alternative] = field(default_factory=lambda: {})

    # def __eq__(self, other) -> bool:
    #     if type(other) != "Usage":
    #         return False
    #     return (self.lang == other.lang
    #         and self.var == other.var
    #         and self.alt == other.alt
    #         and self.cnt == other.cnt)

    def has_alternatives(self) -> bool:
        """
        >>> Usage("sl", word="аще", lemmas=["аще"]).has_alternatives()
        False
        >>> Usage("sl", Source("WH"), word="аще", lemmas=["аще"], main_alt=Alternative("om. WH", "om.")).has_alternatives()
        True
        >>> Usage("sl", word="аще", lemmas=["аще"], var_alt={Source("WH"):Alternative("om. WH", "om.")}).has_alternatives()
        True
        """
        return bool(self.main_alt) or bool(self.var_alt)

    def __hash__(self) -> int:
        vl = "/".join([f"{v} {k}" for k, v in self.var_alt.items()])
        return hash(
            (
                self.lang,
                self.var,
                self.main_alt,
                vl,
                self.word,
                tuple(self.lemmas),
                self.cnt,
            )
        )

    def __lt__(self, other) -> bool:
        """
        >>> s = Source("WH")
        >>> a = Usage("sl", s, "om.", main_alt=Alternative("аще", "аще"))
        >>> b = Usage("sl", s, "om.", main_alt=Alternative("\ue205", "\ue205 conj."))
        >>> a < b
        True

        >>> s = Source("GH")
        >>> a = Usage("sl", s, "оуслышат\ue205 GH", main_alt=Alternative("слꙑшат\ue205", "слꙑшат\ue205"))
        >>> b = Usage("sl", s, "оуслышат\ue205 GH", main_alt=Alternative("послꙑшат\ue205", "послꙑшат\ue205"), cnt=2)
        >>> a < b
        True
        """
        return (
            self.cnt < other.cnt
            or self.cnt == other.cnt
            and len(self.var) < len(other.var)
            or self.cnt == other.cnt
            and len(self.var) == len(other.var)
            and self.main_alt < other.main_alt
            or self.cnt == other.cnt
            and len(self.var) == len(other.var)
            and self.main_alt == other.main_alt
            and self.var_alt.keys() < other.var_alt.keys()
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
    # SPECIAL_CHARS indicate what type of correspondence it is, when non exact
    semantic: str = ""

    def __hash__(self):
        return hash((self.idx, self.orig, self.trans))

    def __eq__(self, other) -> bool:
        """
        >>> tma1 = Alternative(lemma="\ue201д\ue205но\ue20dѧдъ")
        >>> tva1 = {"G": Alternative(lemma="\ue205но\ue20dѧдъ")}
        >>> tma2 = Alternative(lemma="\ue201д\ue205но\ue20dѧдъ")
        >>> tva2 = {"H": Alternative(lemma="\ue201д\ue205нородъ")}
        >>> a = Alignment(Index("1/W168a25"), Usage("gr", word="μονογενοῦς"), Usage("sl", Source("H"), main_alt=tma1, var_alt=tva1))
        >>> b = Alignment(Index("1/W168a25"), Usage("gr", word="μονογενοῦς"), Usage("sl", Source("G"), main_alt=tma2, var_alt=tva2))
        >>> a == b
        False

        >> oa1 = {Source("GH"): Alternative("пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G", "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205")}
        >> oa2 = Alternative(lemma="пр\ue205\ue20dьтьн\ue205къ быт\ue205", word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть")
        >> a = Alignment(Index("5/28c21-d1"), Usage("sl", var_alt=oa1, word="пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть"))
        >> b = Alignment(Index("5/28c21-d1"), Usage("sl", Source("GH"), main_alt=oa2, word="пр\ue205\ue20dестн\ue205ц\ue205 б• H пр\ue205\ue20dестьн\ue205ц\ue205 б• G"))
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

    def has_alternatives(self) -> bool:
        return self.orig.has_alternatives() or self.trans.has_alternatives()

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
        >>> a = Alignment(i, Usage("sl", s, "om.", main_alt=Alternative("аще", "аще")))
        >>> b = Alignment(i, Usage("sl", s, "om.", main_alt=Alternative("\ue205", "\ue205 conj.")))
        >>> a < b
        True

        >>> i = Index("5/22b5")
        >>> s = Source("GH")
        >>> a = Alignment(i, Usage("sl", s, "оуслышат\ue205 GH", main_alt=Alternative("слꙑшат\ue205", "слꙑшат\ue205")))
        >>> b = Alignment(i, Usage("sl", s, "оуслышат\ue205 GH", main_alt=Alternative("послꙑшат\ue205", "послꙑшат\ue205"), cnt=2))
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
