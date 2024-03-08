from typing import List
from dataclasses import dataclass, field

import re

from const import PATH_SEP, SPECIAL_CHARS


@dataclass(frozen=True)
class Alternative:
    """Word occurences in a line are counted.
    For main alternative this is in a separate variable,
    but for variants, it's part of the dictionary.

    In case of semantic relationships (see README.md#semantic-relationships),
    these are stored in the model, and interpreted during export.
    Currently, this is not the approach used in the broader alignment
    """

    # Working only with last lemma
    word: str = ""
    lemma: str = ""
    # TODO: keep full lemmas stack
    # lemmas: List[str] = field(default_factory=lambda: [])
    cnt: int = 1
    # SPECIAL_CHARS indicate what type of correspondence it is, when non exact
    semantic: str = ""

    def __hash__(self):
        # vl = "/".join([f"{v} {k}" for k, v in self.var_lemmas.items()])
        # vw = "/".join([f"{v[0]}{v[1]} {k}" for k, v in self.var_words.items()])
        return hash((self.lemma, self.word, self.cnt))

    def __bool__(self) -> bool:
        """
        >>> bool(Alternative())
        False
        >>> bool(Alternative("аще", "аще"))
        True
        """
        return bool(self.lemma)

    def __lt__(self, other) -> bool:
        """
        >>> Alternative("аще", "аще") < Alternative("\ue205", "\ue205 conj.")
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

    def __contains__(self, item: str):
        return item in self.parts or item == self.annotation

    def __str__(self):
        """We want to see results in reverse order.
        Also, if last part is special character, display it smarter
        >>> str(Path(["θεός", "Gen."]))
        'Gen. → θεός'
        >>> str(Path(['съкаꙁат\ue205', 'съкаꙁа\ue201мо', '≈']))
        '≈ съкаꙁа\ue201мо → съкаꙁат\ue205'
        >>> str(Path(['# υἱός']))
        '# υἱός'
        """
        parts = self.parts.copy()
        if len(parts) > 1:
            if parts[-1][0] in SPECIAL_CHARS:
                self.semantics = parts[-1][0]
                if len(parts[-1]) == 1:
                    parts[-2] = f"{parts[-1]} {parts[-2]}"
                    parts.pop(-1)
                elif parts[-1].endswith(parts[-2]):
                    parts.pop(-2)
            content = PATH_SEP.join(parts[::-1])
            prefix = f"{self.semantics} " if self.semantics else ""
            return (
                f"{prefix}{content} {self.annotation}" if self.annotation else content
            )
        elif len(parts) == 1:
            return f"{parts[0]} {self.annotation}" if self.annotation else parts[0]
        return self.annotation if self.annotation else ""

    def compile(self):
        """Remove empty steps, extract annotations"""
        for cur in range(len(self.parts) - 1, -1, -1):
            if not self.parts[cur]:
                self.parts.pop(cur)
            elif re.match(r"^[a-zA-z\.]+$", self.parts[cur]):
                self.annotation = self.parts.pop(cur)
