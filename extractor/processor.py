#!/usr/bin/env python3

from typing import Optional
import logging as log
import re

from const import LINE_CH
from model import Word, WordList


def dehyphenate(words: WordList) -> WordList:
    result = WordList()
    w: Optional[Word] = words[0]
    while w:
        while w.word and w.next and w.word[-1] == "-":
            log.debug(w)
            w.word = w.word[:-1] + w.next.word
            if w.next.variant:
                if (
                    w.variant
                    and LINE_CH not in w.variant
                    and not w.variant.startswith("om.")
                ):
                    log.error(f"Неочакван вариант на {w.index()}: {w.variant}")
                    # raise SyntaxError(f"Unexpected variant: {w.variant}")
                if w.variant:
                    w.variant = w.variant.replace(LINE_CH, w.next.variant)
                else:
                    w.variant = w.next.variant
            log.debug(w.next)
            w.prependTo(w.next.next)
        result += w
        w = w.next
    return result


def condense(words: WordList) -> WordList:
    """Remove empty words"""
    result = WordList()
    result += words
    for w in words:
        if not w.word.strip() and not w.variant.strip():
            result.remove(w)
    return result


def integrate_words(words: WordList) -> WordList:
    """Merge words that were split by comments"""
    result = WordList()
    token: Optional[Word] = words[0]
    while token:
        line = re.split(r"\s", token.line_context)
        log.debug(f"word: {token}")
        log.debug(f"line: {line}")
        for word in line:
            log.debug(word)
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
                    log.debug(token)
                    log.debug(token.variant)
                    log.debug(token.next.variant)

                if not token.variant:
                    token.variant = token.next.variant
                token.prependTo(token.next.next)
            log.debug(token.word)
        result += token
        token = token.next
    return result
