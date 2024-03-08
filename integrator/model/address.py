"""The Index class is actually an address up to a line.
Not to be confused with a word index which is the complete output of the indexgenerator"""

from typing import Callable, List, Optional, Union
import logging as log
import re

IDX_SEP = "-"  # used to show index/address ranges

# for indices/addresses
alpha = r"^([A-Za-z]*)(.*)$"
numeric = r"^([0-9]*)(.*)$"


class Index:
    _less: Optional[Callable] = None
    # end: Optional["Index"] = None
    maxlen: List[int] = []

    def __init__(self, value: str) -> None:
        """
        >>> Index.maxlen = [2,1,2,3,1,2]
        >>> i = Index("1/5a5")
        >>> i.data
        [1, '/', 5, 'a', 5]

        >>> i = Index("2/W169b26")
        >>> i.data
        [2, '/', 'W', 169, 'b', 26]

        >>> Index.maxlen = [3,1,2]
        >>> i = Index("554.26")
        >>> i.data
        [554, '.', 26]

        >>> Index.maxlen = [2,1,3,3,2,2]
        >>> i = Index("3/15a5-b1")
        >>> i.data
        [3, '/', 15, 'a', 5]
        >>> i.end
        Index('3/15b1')
        >>> i.end.data
        [3, '/', 15, 'b', 1]
        """
        self.data: List[Union[str, int]] = []
        self.end: Optional[Index] = None

        rest = value
        restlen = len(rest)
        while rest:
            # print(Index.maxlen)
            # print(len(self.data))
            if rest[0].isnumeric():
                m = re.search(numeric, rest)
                if not m:
                    raise ValueError(f"Invalid address: {value}")
                v = m.group(1)
                """
                if len(Index.maxlen) == len(self.data):
                    # print(v)
                    Index.maxlen += [len(v)]
                    # print(Index.maxlen)
                elif len(v) > Index.maxlen[ci]:
                    # print(v)
                    Index.maxlen[ci] = len(v)
                    # print(Index.maxlen)
                """
                self.data += [int(v)]
                rest = m.group(2)
                if restlen == len(rest):
                    raise ValueError(f"Invalid address: {value}")
                else:
                    restlen = len(rest)
            elif rest[0].isalpha():
                m = re.search(alpha, rest)
                assert m, f"Expected regex token is missing: {m}"
                v = m.group(1)
                """
                if len(Index.maxlen) == len(self.data):
                    Index.maxlen += [len(v)]
                    # print(Index.maxlen)
                elif len(v) > Index.maxlen[ci]:
                    Index.maxlen[ci] = len(v)
                    # print(Index.maxlen)
                """
                self.data += [v]
                rest = m.group(2)
                if restlen == len(rest):
                    raise ValueError(f"Invalid address: {value}")
                else:
                    restlen = len(rest)
            elif rest[0] == IDX_SEP:
                self.end = Index(rest[1:])
                le = len(self.end.data)
                ls = len(self.data)
                if le < ls:
                    edata = self.data[:-le] + self.end.data
                    self.end.data = edata
                    # i = "".join(str(d) for d in edata)
                    # self.end = Index(i)
                if self.data == self.end.data:
                    self.end = None
                break
            else:
                # if len(Index.maxlen) == len(self.data):
                #     Index.maxlen += [1]
                self.data += [rest[0]]
                rest = rest[1:]

    def __hash__(self):
        return hash((tuple(self.data), self.end))

    def __eq__(self, other) -> bool:
        if type(other) != Index:
            return False
        return self.data == other.data

    def __lt__(self, other) -> bool:
        if Index._less is not None:
            return Index._less(self, other)
        for i, v in enumerate(self.data):
            try:
                if v < other.data[i]:
                    return True
                if v > other.data[i]:
                    return False
            except TypeError as te:
                log.error(f"Сравнение на несравними стойности {v} и {other.data[i]}")
                log.error(te)
                break
        if self.end:
            return self.end < other.end if other.end else True
        else:
            return other.end is not None

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other

    def __str__(self) -> str:
        """
        >>> str(Index("1/5a5"))
        '1/5a5'

        >>> str(Index("2/W169b26"))
        '2/W169b26'

        >>> str(Index("554.26"))
        '554.26'
        """
        s = "".join(str(d) for d in self.data)
        if not self.end:
            return s
        for i, v in enumerate(self.end.data):
            if self.data[i] != v:
                return s + "-" + "".join(str(d) for d in self.end.data[i:])
        raise Exception(f"ГРЕШКА: Съвпадащи начален и краен адрес/индекс")

    def longstr(self) -> str:
        # print(Index.maxlen)
        # print(self.data)
        # if self.end:
        # print(self.end.data)
        ld: List[str] = []
        for i, d in enumerate(self.data):
            if type(d) == int:
                f = f"{{:0{Index.maxlen[i]}d}}"
                ld += [f.format(d)]
            else:
                assert (
                    type(d) == str
                ), f"{type(d)} is currently not supported for Address components"
                ld += [d]  # type: ignore
        s = "".join(ld)
        if not self.end:
            return s
        for i, v in enumerate(self.end.data):
            # print(f"{i}: {self.data[i]}/{v}")
            if self.data[i] != v:
                lde = []
                for j in range(i, len(self.end.data)):
                    # print(f"{j}: {self.data[j]}/{self.end.data[j]}")
                    if type(self.end.data[j]) == int:
                        f = f"{{:0{Index.maxlen[j]}d}}"
                        lde += [f.format(self.end.data[j])]
                    else:
                        e = self.end.data[j]
                        assert (
                            type(e) == str
                        ), f"{type(d)} is currently not supported for Address components"
                        lde += [e]  # type: ignore
                return s + "-" + "".join(lde)
        raise Exception(f"ГРЕШКА: Съвпадащи начален и краен адрес/индекс")

    def __repr__(self) -> str:
        """
        >>> Index("1/5a5")
        Index('1/5a5')
        """
        return f"Index('{self}')"
