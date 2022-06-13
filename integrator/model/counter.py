from typing import Dict, Iterable, List, Set, Tuple, Union
from dataclasses import dataclass, field

from sortedcontainers import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG
from config import VAR_GR, VAR_SL

from .address import Index
from .model import Usage, UsageContent
from .source import Source


def _present(a: Usage, s: Iterable[Usage], trans: bool = False) -> bool:
    present = False
    for e in s:
        if e.colocated(a, trans):
            present = True
    return present


@dataclass
class Counter:
    orig_main: Set[Usage] = field(default_factory=lambda: set())
    orig_var: Set[Usage] = field(default_factory=lambda: set())
    trans_main: Set[Usage] = field(default_factory=lambda: set())
    trans_var: Set[Usage] = field(default_factory=lambda: set())

    def __iadd__(self, other: "Counter") -> "Counter":
        self.orig_main |= other.orig_main
        self.orig_var |= other.orig_var
        self.trans_main |= other.trans_main
        self.trans_var |= other.trans_var
        return self

    def get_counts(self, trans: bool = False) -> Tuple[int, int]:
        print()
        m = self.trans_main if trans else self.orig_main
        v = self.trans_var if trans else self.orig_var
        print(m)
        print(v)
        ml: List[Usage] = []
        for s in m:
            if not _present(s, ml, trans):
                ml += [s]
        vl: List[Usage] = []
        for s in v:
            if not _present(s, m, trans) and not _present(s, vl, trans):
                vl += [s]
        print(ml)
        print(vl)
        return (len(ml), len(vl))

    @staticmethod
    def get_set_counts(s: Set[Usage]) -> "Counter":
        """
        >>> from model import Index, Usage, UsageContent
        >>> i = [Index(ch=1, alt=True, page=168, col='c', row=7), Index(ch=1, alt=True, page=169, col='c', row=7)]
        >>> s = SortedSet([Usage(n, UsageContent(FROM_LANG)) for n in i])
        >>> c = Counter.get_set_counts(s)
        >>> c.get_counts(True)
        (2, 0)
        >>> c.get_counts(False)
        (2, 0)

        >>> i = Index(ch=1, alt=True, page=168, col='c', row=7)
        >>> s = SortedSet([Usage(i, UsageContent("sl", Source("W"))), Usage(i, UsageContent("sl", cnt=2), UsageContent("gr", cnt=2))])
        >>> c = Counter.get_set_counts(s)
        >>> c.get_counts(False)
        (1, 1)
        >>> c.get_counts(True)
        (2, 0)
        """
        lang = next(iter(s)).orig.lang
        orig_var = VAR_SL if lang == FROM_LANG else VAR_GR
        trans_var = VAR_GR if lang == FROM_LANG else VAR_SL
        r = Counter()
        for nxt in s:
            assert nxt.orig.lang == lang

            found = False
            for v in Source(orig_var):
                if v in Source(nxt.orig.var):
                    r.orig_var.add(nxt)
                    found = True
                    break
            if not found:
                r.orig_main.add(nxt)

            found = False
            for v in Source(trans_var):
                if v in Source(nxt.orig.var):
                    r.trans_var.add(nxt)
                    found = True
                    break
            if not found:
                r.trans_main.add(nxt)

        return r

    @staticmethod
    def get_dict_counts(d: Union[SortedDict, Dict]) -> "Counter":
        """
        >>> from model import Index, Usage, UsageContent

        >> c = Counter.get_dict_counts({})
        >> c.get_counts(True)
        (0, 0)
        >> c.get_counts(False)
        (0, 0)

        >>> u = Usage(Index(ch=1, alt=False, page=5, col='a', row=5), UsageContent(FROM_LANG))
        >>> d = SortedDict({'pass. >> ἀγνοέω': {('не бѣ ꙗвленъ•', 'ἠγνοεῖτο'): SortedSet([u])}})
        >>> c = Counter.get_dict_counts(d)
        >>> c.get_counts(True)
        (1, 0)
        >>> c.get_counts(False)
        (1, 0)

        >>> u1 = Usage(Index(ch=1, alt=False, page=8, col='a', row=3), UsageContent(FROM_LANG))
        >>> u2 = Usage(Index(ch=1, alt=False, page=6, col='b', row=7), UsageContent(FROM_LANG))
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
        if type(any) is SortedSet or type(any) is set:
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
