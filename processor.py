#!/usr/bin/env python3

from typing import List, Tuple, Dict

import re


def clean_hyphens(book_index: Dict[str, str]) -> Dict[str, str]:
    to_remove = []
    prevline = None
    pli = None
    for nli in book_index.keys():
        nextline = book_index[nli]
        if prevline and prevline[-1] == "-":
            prevwords = re.split("\s", prevline)
            nextwords = re.split("\s", nextline)
            assert len(nextwords) > 0
            assert len(prevwords) > 0
            prevwords[-1] = prevwords[-1][:-1] + nextwords[0]
            prevline = " ".join(prevwords)
            nextline = " ".join(nextwords[1:])
            book_index[pli] = prevline
            book_index[nli] = nextline
        elif pli and not prevline:
            to_remove.append(pli)
        prevline = nextline
        pli = nli

    for k in to_remove:
        book_index.pop(k, None)

    return book_index


def split_rows(book_index: Dict[str, str]) -> List[Tuple[str]]:
    word_index = []
    for k in book_index.keys():
        words = re.split("\s", book_index[k])
        for w in words:
            word_index.append((k, w, book_index[k]))
    return word_index
