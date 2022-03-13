from typing import Any, Dict, List, Optional
from dataclasses import dataclass

import re

from const import BRACE_OPEN
from regex import address_regex


def _cnt_str(idx: "Index") -> str:
    p1 = f"[{idx.ocnt}]" if idx.ocnt > 1 else ""
    p2 = f"{{{idx.tcnt}}}" if idx.tcnt > 1 else ""
    return p1 + p2


def _merge_counts(pval: int, reval: Any) -> int:
    # We don't know if counters come from corresponding columns or index postfix.
    # TODO: Make sure to investigate and fix this, so they're not messed up
    result = int(reval) if reval else None
    assert result == None or pval == 1 or result == pval
    if result:
        return result
    return pval


@dataclass(frozen=True)
class Index:
    """Index only indicates if it is from a variant.
    Alternative variable (alt) means alternative indexing (as in Vienna scroll).
    Not related to alternative variants
    Contrast these to Usage."""

    ch: int = 1
    alt: bool = False
    page: int = 0
    col: str = ""
    row: int = 0
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
        m = re.search(address_regex, value)
        assert m
        # print(m.groups())
        ch = int(m.group(1)) if m.group(1) else 1
        # alt puts W at end of ch1 and at start of ch2
        alt = (bool(m.group(2)) if ch % 2 else not m.group(2)) if ch < 3 else False
        page = int(m.group(3)) if m.group(3) else 0
        col = m.group(4) if m.group(4) else ""
        row = int(m.group(5)) if m.group(5) else 0

        ocnt = _merge_counts(ocnt, m.group(7))
        tcnt = _merge_counts(tcnt, m.group(9))

        end = None
        if m.group(18):
            e_ocnt = _merge_counts(ocnt, m.group(20))
            e_tcnt = _merge_counts(tcnt, m.group(22))

            e_ch = ch
            e_alt = alt
            e_page = page
            e_col = col
            e_row = int(m.group(18))
            if m.group(17):
                e_col = m.group(17)
                if m.group(16):
                    e_page = int(m.group(16))
                    if m.group(14):
                        e_ch = int(m.group(14))
                    e_alt = (
                        (bool(m.group(15)) if e_ch % 2 else not m.group(15))
                        if e_ch < 3
                        else False
                    )
            end = Index(
                e_ch,
                e_alt,
                e_page,
                e_col,
                e_row,
                e_ocnt,
                e_tcnt,
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
        # TODO: distinguish between symbols for ocnt and tcnt
        cnt = _cnt_str(self)
        start = f"{self.ch}/{w}{self.page}{self.col}{self.row}{cnt}"
        if self.end:
            if self.end.ch != self.ch:
                return f"{start}-{str(self.end)}"
            ecnt = _cnt_str(self.end)
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
        cnt = _cnt_str(self)
        start = f"{self.ch:02d}/{w}{self.page:03d}{self.col}{self.row:02d}{cnt}"
        if self.end:
            if self.end.ch != self.ch:
                return f"{start}-{self.end.longstr()}"
            ecnt = _cnt_str(self.end)
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

    def __lt__(self, other) -> bool:
        if not other:
            return False

        if self.ch < other.ch:
            return True
        if self.ch > other.ch:
            return False

        if self.alt < other.alt:
            return True
        if self.alt > other.alt:
            return False

        if self.page < other.page:
            return True
        if self.page > other.page:
            return False

        if self.col < other.col:
            return True
        if self.col > other.col:
            return False

        if self.row < other.row:
            return True
        if self.row > other.row:
            return False

        if other.end and self.end < other.end:
            return True
        if not other.end or self.end > other.end:
            return False

        return self.word < other.word

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other
