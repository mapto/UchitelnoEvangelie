#!/usr/bin/env python3

from typing import List, Tuple, Dict

import re


def transform_clean(
    lines_index: Dict[str, Tuple[str, List[int]]]
) -> List[Tuple[str, str, List[int]]]:
    """Transforms Dict to List and merges hyphened words into their first line.
    Returns line_num, line, comment_indices"""
    transformed = []
    prevline = ""
    pli = ""
    for nli in lines_index.keys():
        nextline = lines_index[nli][0]
        if prevline:
            if prevline[-1] == "-":
                prevwords = re.split(r"\s", prevline)
                nextwords = re.split(r"\s", nextline)
                assert len(nextwords) > 0
                assert len(prevwords) > 0
                prevwords[-1] = prevwords[-1][:-1] + nextwords[0]
                prevline = " ".join(prevwords)
                nextline = " ".join(nextwords[1:])
                lines_index[pli] = (prevline, lines_index[pli][1])
                lines_index[nli] = (nextline, lines_index[nli][1])
            transformed.append((pli, prevline, lines_index[pli][1]))
        prevline = nextline
        pli = nli

    transformed.append((pli, prevline, lines_index[pli][1]))

    return transformed


def split_rows(
    book_index: List[Tuple[str, str, List[int]]], comments: Dict[int, str]
) -> List[Tuple[str, str, str, str]]:
    """Returns line_num, word, line, comment"""
    # TODO: insert comments
    word_index = []
    for line in book_index:
        k = line[0]
        words = re.split(r"\s", line[1])
        for w in words:
            word_index.append((k, w, line[1], ""))
    return word_index
