#!/usr/bin/env python3

from typing import List, Tuple, Dict, Optional

import re

from model import Comment, Word


def dehyphenate(words: List[Word]) -> List[Word]:
    result: List[Word] = []
    w: Optional[Word] = words[0]
    while w:
        # print(w)
        while w.word and w.next and w.word[-1] == "-":
            # print(w)
            w.word = w.word[:-1] + w.next.word
            if w.next.variant:
                assert not w.variant or "↓" in w.variant or w.variant.startswith("om.")
                if w.variant:
                    w.variant = w.variant.replace("↓", w.next.variant)
                else:
                    w.variant = w.next.variant
            # print(w.next)
            if w.next.next:
                w.prependTo(w.next.next)
            else:
                w.next = None
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
    result = list(words)
    token: Optional[Word] = words[0]
    while token:
        line = re.split(r"\s", token.line_context)
        # print(f"word: {token}")
        # print(f"line: {line}")
        for word in line:
            # print(word)
            while word.startswith(token.word) and word != token.word and token.next:
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
                if token.next.next:
                    token.prependTo(token.next.next)
                else:
                    token.next = None
            # print(token.word)
        token = token.next
    return result
