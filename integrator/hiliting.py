from typing import List, Optional

from const import HILITE_PREFIX, STYLE_COL

from semantics import LangSemantics, MainLangSemantics


def _hilited_col(row: List[str], col: int) -> Optional[str]:
    """highlighting implemented via background colour.
    If column visibly highlighted, return its non-white color, else None

    >>> r = [""] * 4 + ["02/W169b26", "на", "ма же \ue201д\ue205нь ѿ ѡбою на де-", "на", "на + Loc."] + [""] * 17 + ["hl00:FFFFFFFF|hl05:AAAAAAAA|hl08:BBBBBBBB|bold|italic"]
    >>> _hilited_col(r, 5)
    'AAAAAAAA'
    >>> _hilited_col(r, 8)
    'BBBBBBBB'
    >>> _hilited_col(r, 9)
    >>> _hilited_col(r, 0)
    """
    style = row[STYLE_COL]
    if f"{HILITE_PREFIX}{col:02d}" in style:
        pos = style.index(f"{HILITE_PREFIX}{col:02d}")
        # log.debug(style[pos + 5 : pos + 13])
        if style[pos + 5 : pos + 11].upper() == "FFFFFF":
            return None
        return style[pos + 5 : pos + 13]
    return None


def _hilited_local(osem: LangSemantics, tsem: LangSemantics, row: List[str]) -> bool:
    """highlighting in third lemma and further.
    This highlighting has impact on variants. If undesired better create separate rows in variants.
    This highlighted sublemma is relevant only to this usage and not to the whole phrase.
    """
    cols = [
        osem.lemmas[2],
        osem.other().lemmas[2],
        tsem.lemmas[2],
        tsem.other().lemmas[2],
    ]
    return any(_hilited_col(row, c) for c in cols)


def _hilited_irrelevant(sem: LangSemantics, row: List[str]) -> bool:
    """highlighting in second lemma. This is asymmetric annotation.
    Also checks if passed column is in second lemma, if passed at all.
    The usage is part of to the phrase, but is lexicographically irrelevant (i.e. does not need to show up in the phrase).
    """
    return _hilited_col(row, sem.lemmas[1]) != None


class Hiliting:
    def __init__(
        self,
        group: List[List[str]],
        orig: LangSemantics,
        trans: MainLangSemantics,
    ):
        self.group = group

        # Numbers of rows that are not indicated as grammatical
        self.merge_rows = set(
            i for i, r in enumerate(group) if not _hilited_local(orig, trans, r)
        )

        # Rows that are not indicated as grammatical
        self.non_local_group = [group[i] for i in self.merge_rows]

        # Rows that are not indicated as grammatical or union
        # self.relevant_group = [
        #     r for r in self.non_local_group #if not _hilited_irrelevant(orig, trans, r)
        # ]

        # if not hilited words, means grouping is caused by SAME_CH
        self.hilited = any(
            _hilited_col(self.group[0], c) != None
            for c in orig.word_cols() + trans.word_cols()
        )

    def relevant_group(self, sem: LangSemantics):
        return [r for r in self.non_local_group if not _hilited_irrelevant(sem, r)]

    def __str__(self) -> str:
        return f"Grouping is due to {'hiliting' if self.hilited else 'sameness'}"
