from typing import Dict, Set, Tuple, Union
from dataclasses import dataclass, field

from sortedcontainers import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG
from config import VAR_GR, VAR_SL

from .address import Index


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

    @staticmethod
    def get_set_counts(s: SortedSet) -> "Counter":
        """
        >>> from model import Index, Usage
        >>> i = [Index(ch=1, alt=True, page=168, col='c', row=7), Index(ch=1, alt=True, page=169, col='c', row=7)]
        >>> s = SortedSet([Usage(n, FROM_LANG) for n in i])
        >>> c = Counter.get_set_counts(s)
        >>> c.get_counts(True)
        (2, 0)
        >>> c.get_counts(False)
        (2, 0)

        >>> i = [Index(ch=1, alt=True, page=168, col='c', row=7), Index(ch=1, alt=True, page=168, col='c', row=7, ocnt=2)]
        >>> s = SortedSet([Usage(n, FROM_LANG, "W" if x == 0 else "") for x, n in enumerate(i)])
        >>> c = Counter.get_set_counts(s)
        >>> c.get_counts(False)
        (1, 1)
        >>> c.get_counts(True)
        (2, 0)
        """
        lang = next(iter(s)).lang
        orig_var = VAR_SL if lang == FROM_LANG else VAR_GR
        trans_var = VAR_GR if lang == FROM_LANG else VAR_SL
        r = Counter()
        for nxt in s:
            assert nxt.lang == lang

            found = False
            for v in orig_var:
                if v in nxt.var:
                    r.orig_var.add(nxt.idx)
                    found = True
                    break
            if not found:
                r.orig_main.add(nxt.idx)

            found = False
            for v in trans_var:
                if v in nxt.var:
                    r.trans_var.add(nxt.idx)
                    found = True
                    break
            if not found:
                r.trans_main.add(nxt.idx)

        return r

    @staticmethod
    def get_dict_counts(d: Union[SortedDict, dict]) -> "Counter":
        """
        >>> from model import Index, Usage

        >> c = Counter.get_dict_counts({})
        >> c.get_counts(True)
        (0, 0)
        >> c.get_counts(False)
        (0, 0)

        >>> u = Usage(Index(ch=1, alt=False, page=5, col='a', row=5), FROM_LANG)
        >>> d = SortedDict({'pass. >> ἀγνοέω': {('не бѣ ꙗвленъ•', 'ἠγνοεῖτο'): SortedSet([u])}})
        >>> c = Counter.get_dict_counts(d)
        >>> c.get_counts(True)
        (1, 0)
        >>> c.get_counts(False)
        (1, 0)

        >>> u1 = Usage(Index(ch=1, alt=False, page=8, col='a', row=3), FROM_LANG)
        >>> u2 = Usage(Index(ch=1, alt=False, page=6, col='b', row=7), FROM_LANG)
        >>> d = SortedDict({'lem2': SortedDict({'lem1': SortedDict({'τοσоῦτος': {('тол\ue205ко•', 'τοσοῦτοι'): SortedSet([u1]), ('тол\ue205ка', 'τοσαῦτα'): SortedSet([u2])}})})})
        >>> c = Counter.get_dict_counts(d)
        >>> c.get_counts(True)
        (2, 0)
        >>> c.get_counts(False)
        (2, 0)
        """
        # print(dict(d))
        r = Counter()
        # if not d:
        #    return r
        any = next(iter(d.values()))
        if type(any) is SortedSet:
            for n in d.values():
                r += Counter.get_set_counts(n)
        else:  # type(any) is SortedDict or type(any) is dict:
            for k, n in d.items():
                try:
                    r += Counter.get_dict_counts(n)
                except StopIteration as si:
                    print(f"ГРЕШКА: При генериране неуспешно преброяване на {k}")
                    raise si
        return r
