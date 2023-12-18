from typing import Dict, List, Optional, Set

from const import HILITE_PREFIX, IDX_COL, STYLE_COL, V_LEMMA_SEP

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
        if style[pos + 5 : pos + 11] == "FFFFFF":
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


def _hilited_irrelevant(
    osem: LangSemantics, tsem: LangSemantics, row: List[str], col: int = -1
) -> bool:
    """highlighting in second lemma. Also checks if passed column is in second lemma, if passed at all.
    The usage is part of to the phrase, but is lexicographically irrelevant (i.e. does not need to show up in the phrase).
    """
    cols = [
        osem.lemmas[1],
        osem.other().lemmas[1],
        tsem.lemmas[1],
        tsem.other().lemmas[1],
    ]
    if col != -1 and col not in cols:
        return False
    return any(_hilited_col(row, c) for c in cols)


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
        # self.merge_rows_main = set(
        #     i for i, r in enumerate(group) if not _hilited_gram(orig, trans, r)
        # )
        # self.merge_rows_var = set(
        #     i for i, r in enumerate(group) if not _hilited_gram(orig, trans.other(), r)
        # )
        # self.merge_rows_other = self.merge_rows_main | self.merge_rows_var

        # Rows that are not indicated as grammatical
        self.non_gram_group = [group[i] for i in self.merge_rows]
        # self.non_gram_group_main = [group[i] for i in self.merge_rows_main]
        # self.non_gram_group_var = [group[i] for i in self.merge_rows_var]
        # self.non_gram_group_other = [group[i] for i in self.merge_rows_other]

        # Rows that are not indicated as grammatical or union
        self.non_union_group = [
            r for r in self.non_gram_group if not _hilited_irrelevant(orig, trans, r)
        ]
        # self.non_union_group_main = [
        #     r for r in self.non_gram_group_main if not _hilited_union(orig, trans, r)
        # ]
        # self.non_union_group_var = [
        #     r for r in self.non_gram_group_var if not _hilited_union(orig, trans.other(), r)
        # ]
        # TODO: Actually not used
        # self.non_union_group_other = [
        #     r for r in self.non_gram_group_other if not _hilited_union(orig.other(), trans.other(), r)
        # ]

        # if not hilited words, means grouping is caused by SAME_CH
        self.hilited = any(
            _hilited_col(self.group[0], c) != None
            for c in orig.word_cols() + trans.word_cols()
        )

    def __str__(self) -> str:
        return f"Grouping is due to {'hiliting' if self.hilited else 'sameness'}"
