#!/usr/bin/env python3

from typing import List, Tuple, Dict, Optional

import re

from const import LINE_CH
from model import Comment, Word


def dehyphenate(words: List[Word]) -> List[Word]:
    result: List[Word] = []
    w: Optional[Word] = words[0]
    while w:
        while w.word and w.next and w.word[-1] == "-":
            # print(w)
            w.word = w.word[:-1] + w.next.word
            if w.next.variant:
                assert (
                    not w.variant or LINE_CH in w.variant or w.variant.startswith("om.")
                )
                if w.variant:
                    w.variant = w.variant.replace(LINE_CH, w.next.variant)
                else:
                    w.variant = w.next.variant
            # print(w.next)
            w.prependTo(w.next.next)
        result.append(w)
        w = w.next
    return result


def condense(words: List[Word]) -> List[Word]:
    """Remove empty words"""
    result = list(words)
    for w in words:
        if not w.word.strip() and not w.variant.strip():
            result.remove(w)
    return result


def integrate_words(words: List[Word]) -> List[Word]:
    """Merge words that were split by comments"""
    result = []
    token: Optional[Word] = words[0]
    while token:
        line = re.split(r"\s", token.line_context)
        # print(f"word: {token}")
        # print(f"line: {line}")
        for word in line:
            # print(word)
            while (
                token.word
                and word.startswith(token.word)
                and word != token.word
                and token.next
            ):
                if not token.next.word and token.next.variant and token.next.next:
                    addition = token.next
                    extension = token.next.next
                    next = token.next.next.next
                    token.prependTo(extension)
                    extension.prependTo(addition)
                    addition.prependTo(next)

                token.word = token.word + token.next.word
                if (
                    token.variant
                    and token.next.variant
                    and token.variant not in token.next.variant
                ):
                    print(token)
                    print(token.variant)
                    print(token.next.variant)

                if not token.variant:
                    token.variant = token.next.variant
                token.prependTo(token.next.next)
            # print(token.word)
        result.append(token)
        token = token.next
    return result
