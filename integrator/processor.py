from typing import List
import unicodedata
from sortedcontainers import SortedDict, SortedList, SortedSet  # type: ignore

# from model import Usage
from util import ord_word, base_word

ord_tuple = lambda x: ord_word(x[0])


def merge(corpus: List[List[str]]) -> List[List[str]]:
    result: List[List[str]] = []
    for row in corpus:
        presence = [e for e in row if e == "="]
        if presence:
            for col in range(len(row)):
                if row[col] and row[col] != "=":
                    if result[-1][col]:
                        result[-1][col] += " " + row[col]
                    else:
                        result[-1][col] = row[col]
        else:
            result.append(row)
    return result


def extract_letters(corpus: List[List[str]], col: int) -> SortedSet:
    letters = SortedSet()
    for row in corpus:
        if row[col]:
            letters = letters.union(
                [ch for ch in unicodedata.normalize("NFKC", row[col].lower())]
            )
            # letters = letters.union([ch for ch in row[col].lower()])
    return {l: ord(l) for l in letters}


def aggregate(
    corpus: List[List[str]],
    word_col: int,
    trans_col: int,
    lem_col: List[int],
    tlem_col: int,
) -> SortedDict:
    result = SortedDict(ord_word)
    for row in corpus:
        if not row[3]:
            continue
        # word = row[word_col]
        # translation = row[trans_col]
        l = [base_word(row[i]) for i in lem_col]
        t = base_word(row[tlem_col])
        key = (
            row[word_col].strip() if row[word_col] else "",
            row[trans_col].strip() if row[trans_col] else "",
        )
        val = row[3]
        # usage = Usage(row[word_col], row[trans_col], [row[3]])
        if l[0] in result:
            if l[1] in result[l[0]]:
                if l[2] in result[l[0]][l[1]]:
                    if t in result[l[0]][l[1]][l[2]]:
                        if key in result[l[0]][l[1]][l[2]]:
                            result[l[0]][l[1]][l[2]][t][key].append(val)
                        else:
                            result[l[0]][l[1]][l[2]][t][key] = SortedList([val])
                    else:
                        result[l[0]][l[1]][l[2]][t] = SortedDict(
                            ord_tuple, {key: SortedList([val])}
                        )
                else:
                    result[l[0]][l[1]][l[2]] = SortedDict(
                        ord_word,
                        {t: SortedDict(ord_tuple, {key: SortedList([val])})},
                    )
            else:
                result[l[0]][l[1]] = SortedDict(
                    ord_word,
                    {
                        l[2]: SortedDict(
                            ord_word,
                            {t: SortedDict(ord_tuple, {key: SortedList([val])})},
                        )
                    },
                )
        else:
            result[l[0]] = SortedDict(
                ord_word,
                {
                    l[1]: SortedDict(
                        ord_word,
                        {
                            l[2]: SortedDict(
                                ord_word,
                                {t: SortedDict(ord_tuple, {key: SortedList([val])})},
                            )
                        },
                    )
                },
            )
    return result
