from typing import List
from dataclasses import dataclass, field

import re

from const import PATH_SEP, SPECIAL_CHARS
from regex import l_annot_regex, sem_regex


@dataclass(frozen=True)
class Alternative:
    """Word occurences in a line are counted.
    For main alternative this is in a separate variable,
    but for variants, it's part of the dictionary.

    In case of semantic relationships (see README.md#semantic-relationships),
    these are stored in the model, and interpreted during export.
    Currently, this is not the approach used in the broader alignment.

    For indices a dedicated logic is defined in the lemma() method.
    For lists, the word is being shown.
    """

    # Working only with last lemma
    word: str = ""
    # lemma: str = ""
    # TODO: keep full lemmas stack
    lemmas: List[str] = field(default_factory=lambda: [])
    cnt: int = 1
    # SPECIAL_CHARS indicate what type of correspondence it is, when non exact
    semantic: str = ""

    def __hash__(self):
        # vl = "/".join([f"{v} {k}" for k, v in self.var_lemmas.items()])
        # vw = "/".join([f"{v[0]}{v[1]} {k}" for k, v in self.var_words.items()])
        return hash((tuple(self.lemmas), self.word, self.cnt))

    def __bool__(self) -> bool:
        """
        >>> bool(Alternative())
        False
        >>> bool(Alternative("аще", ["аще"]))
        True
        """
        return bool(self.lemmas)

    def __lt__(self, other) -> bool:
        """
        >>> Alternative("аще", ["аще"]) < Alternative("\ue205", ["\ue205 conj."])
        True
        """
        if self.word < other.word:
            return True
        elif self.word > other.word:
            return False

        if self.cnt < other.cnt:
            return True
        elif self.cnt > other.cnt:
            return False

        return False

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other

    def same(self, other: "Alternative") -> bool:
        """Tolerates differences in word use, but not in lemmas"""
        return (
            tuple(self.lemmas) == tuple(other.lemmas)
            and self.cnt == other.cnt
            and self.semantic == other.semantic
        )

    def lemma(self) -> str:
        """The lemma that is needed for generating indices
        >>> a = Alternative("не твор\ue205т\ue205", ["не & твор\ue205т\ue205", "не твор\ue205т\ue205"], semantic="≈")
        >>> a.lemma()
        '≈ не твор\ue205т\ue205'

        >>> a = Alternative("не створ\ue205т\ue205 H", ["не & сътвор\ue205т\ue205", "не сътвор\ue205т\ue205"], semantic="≈")
        >>> a.lemma()
        '≈ не сътвор\ue205т\ue205'
        """
        # print(self.semantic)
        result = f"{self.semantic} " if self.semantic else ""
        if len(self.lemmas) == 1:
            result += self.lemmas[0]
        elif re.match(r"^" + l_annot_regex + "$", self.lemmas[-1]):
            result += f"{self.lemmas[-2]} {self.lemmas[-1]}"
        else:
            result += self.lemmas[-1]
        return result


@dataclass
class Path:
    """The full collection of lemmas is considered a backtracking path in the final usage hierarchy.
    Gramatical annotation is handled exceptionally.
    >>> Path(['# υἱός'])
    Path(parts=['# υἱός'], annotation='', semantics='')
    >>> Path(["θεός", "Gen."])
    Path(parts=['θεός', 'Gen.'], annotation='', semantics='')
    """

    parts: List[str] = field(default_factory=lambda: [])
    annotation: str = ""
    semantics: str = ""

    def __iadd__(self, s: str):
        self.parts += [s]
        return self

    def __len__(self):
        return len(self.parts)

    def __str__(self):
        """We want to see results in reverse order.
        Also, if last part is special character, display it smarter
        >>> str(Path(["θεός", "Gen."]).compile())
        'θεός Gen.'
        >>> str(Path(['съкаꙁат\ue205', 'съкаꙁа\ue201мо', '≈']).compile())
        '≈ съкаꙁа\ue201мо → съкаꙁат\ue205'
        >>> str(Path(['# υἱός']).compile())
        '# υἱός'
        >>> str(Path(['Χαναάν', 'Gen.']).compile())
        'Χαναάν Gen.'
        >>> str(Path(['Χαναάν', '≠ Gen.']).compile())
        '≠ Χαναάν Gen.'

        >>> str(Path(['Χαναάν', 'Gen.']).compile())
        'Χαναάν Gen.'

        >>> str(Path(['Χαναάν', '≠ Gen.']).compile())
        '≠ Χαναάν Gen.'

        >>> str(Path(['pass.']).compile())
        'pass.'
        """
        prefix = f"{self.semantics} " if self.semantics else ""
        content = PATH_SEP.join(self.parts[::-1])
        annotation = f" {self.annotation}" if self.annotation else ""
        return f"{prefix}{content}{annotation}".strip()

    def __contains__(self, other) -> bool:
        """
        Annotations are taken only from last lemma.
        >>> '≈ ἀμελέω' in Path(['ἀμελέω'], semantics='≈')
        True

        >>> 'не & твор\ue205т\ue205' in Path(['не & твор\ue205т\ue205', 'не твор\ue205т\ue205'], semantics='≈')
        True

        >>> 'pass.' in Path([], 'pass.')
        True

        >>> 'бꙑт\ue205 & подъ & \ue205 pron.' in Path(['бꙑт\ue205 & подъ & \ue205 pron.', 'сꙑ подъ н\ue205м\ue205'])
        True

        >>> 'μετά' in Path(parts=['μετά', 'μετά + Acc.'])
        True
        """
        if type(other) != str:
            return False
        if other[0] in SPECIAL_CHARS and other[0] != self.semantics:
            return False
        word = other[2:] if other[0] in SPECIAL_CHARS else other

        if not self.parts:
            return other == self.annotation

        if self.annotation and self.parts[-1][-1] == ".":
            lparts = self.parts[-1].split(" ")
            if lparts[-1] != self.annotation:
                return False
            if " ".join(lparts[:-1]) == word:
                return True

        return word in self.parts or (not word and not self.parts)

    def compile(self) -> "Path":
        """Remove empty steps, extract annotations.
        It is necessary that this is done post-construction,
        because there are modifications taking place during parsing.
        In other words, class is not immutable, and compilation should be done at end.

        >> Path(['# υἱός']).compile()
        Path(parts=['υἱός'], annotation='', semantics='#')

        >>> Path(['≈ ἀμελέω']).compile()
        Path(parts=['ἀμελέω'], annotation='', semantics='≈')

        >>> Path(["θεός", "Gen."]).compile()
        Path(parts=['θεός'], annotation='Gen.', semantics='')

        >>> Path(['Χαναάν', 'Gen.']).compile()
        Path(parts=['Χαναάν'], annotation='Gen.', semantics='')

        >>> Path(['Χαναάν', '≠ Gen.']).compile()
        Path(parts=['Χαναάν'], annotation='Gen.', semantics='≠')

        >>> Path(['бꙑт\ue205 & подъ & \ue205 pron.', 'сꙑ подъ н\ue205м\ue205']).compile()
        Path(parts=['бꙑт\ue205 & подъ & \ue205 pron.', 'сꙑ подъ н\ue205м\ue205'], annotation='', semantics='')
        """
        regex = r"^" + sem_regex + l_annot_regex + "$"
        result = []
        for cur, lem in enumerate(self.parts[::-1]):
            if not lem:
                continue

            if re.match(regex, lem):
                last = lem
                if last[0] in SPECIAL_CHARS:
                    self.semantics = last[0]
                    self.annotation = last[2:]
                else:
                    self.annotation = last
                continue

            if lem[0] in SPECIAL_CHARS:
                self.semantics = lem[0]
                if len(lem) > 2:
                    result += [lem[2:]]
                continue

            result += [lem]

        self.parts = result[::-1]

        return self
