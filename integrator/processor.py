from typing import List

from sortedcontainers import SortedDict  # type: ignore

# from model import Usage
from util import ord_word


def aggregate(
    corpus: List[List[str]], word_col: int, trans_col: int, lem_col: int
) -> SortedDict:
    result = SortedDict(ord_word)
    for row in corpus:
        if not row[3]:
            continue
        # word = row[word_col]
        # translation = row[trans_col]
        l1 = row[lem_col].strip() if row[lem_col] else ""
        l2 = row[lem_col + 1].strip() if row[lem_col + 1] else ""
        l3 = row[lem_col + 2].strip() if row[lem_col + 2] else ""
        # TODO: multiple usages
        key = (
            row[word_col].strip() if row[word_col] else "",
            row[trans_col].strip() if row[trans_col] else "",
        )
        val = row[3]
        # usage = Usage(row[word_col], row[trans_col], [row[3]])
        if l1 in result:
            if l2 in result[l1]:
                if l3 in result[l1][l2]:
                    if key in result[l1][l2][l3]:
                        result[l1][l2][l3][key].append(val)
                    else:
                        result[l1][l2][l3][key] = [val]
                else:
                    result[l1][l2][l3] = {key: [val]}
            else:
                result[l1][l2] = SortedDict(ord_word, {l3: {key: [val]}})
        else:
            result[l1] = SortedDict(
                ord_word, {l2: SortedDict(ord_word, {l3: {key: [val]}})}
            )
    return result
