from typing import Dict, List, Set

import re

from const import LINE_CH
from model import Comment, Index, Word


def merge(head: List[Word], tail: List[Word]) -> List[Word]:
    """Returns first parameter"""
    if head:
        head[-1].prependTo(tail[0])
    head += tail
    return head


def link_tokens(tokens: List[Word]) -> List[Word]:
    """
    >>> link_tokens([])
    []

    >>> t = [Word(Index(0,"",0))]
    >>> t = link_tokens(t)
    >>> len(t) == 1 and t[0].prev == t[0].next == None
    True

    >>> t = [Word(Index(0,"",0)), Word(Index(0,"",0))]
    >>> t = link_tokens(t)
    >>> len(t) == 2 and t[0].prev == None and t[0].next == t[1] and t[1].prev == t[0] and t[1].next == None
    True

    >>> t = [Word(Index(0,"",0)), Word(Index(0,"",0)), Word(Index(0,"",0))]
    >>> t = link_tokens(t)
    >>> len(t) == 3 and t[0].next == t[1] and t[1].prev == t[0] and t[1].next == t[2] and t[2].prev == t[1]
    True
    
    >>> l = [Word(_index=Index(ch=1, page='4b', row=10), word='ѿ', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=10), word='\ue205', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=10), word='оана', line_context='ѿ \ue205оана⁘', variant=''), \
        Word(_index=Index(ch=1, page='4b', row=10), word='', line_context='ѿ \ue205оана⁘', variant=' на вь\ue010скрсен\ue205\ue201 ї\ue010с хⷭ҇а H'),\
        Word(_index=Index(ch=1, page='4b', row=10), word='⁘', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=11), word='\ue20cьсо', line_context='\ue20cьсо рад\ue205 \ue205н\ue205', variant='')]
    >>> l = link_tokens(l)
    >>> r = [Word(_index=Index(ch=1, page='4b', row=10), word='ѿ', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=10), word='\ue205', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=10), word='оана', line_context='ѿ \ue205оана⁘', variant=''), \
        Word(_index=Index(ch=1, page='4b', row=10), word='', line_context='ѿ \ue205оана⁘', variant=' на вь\ue010скрсен\ue205\ue201 ї\ue010с хⷭ҇а H'),\
        Word(_index=Index(ch=1, page='4b', row=10), word='⁘', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=11), word='\ue20cьсо', line_context='\ue20cьсо рад\ue205 \ue205н\ue205', variant='')]
    >>> [v for i, v in enumerate(l) if v != r[i]]
    []

    """
    if not tokens:
        return tokens
    for i in range(len(tokens)):
        if i == len(tokens) - 1:
            break
        tokens[i].next = tokens[i + 1]
        tokens[i + 1].prev = tokens[i]
    return tokens


class Buffer:
    buff = ""
    line = ""
    line_words: List[Word] = []
    comments: Set[int] = set()

    def __init__(self, buffer: str = ""):
        self.reset()
        self.buff = buffer

    def add(self, text: str) -> None:
        self.buff += text

    def reset(self) -> None:
        self.buff = ""
        self.line = ""
        self.line_words = []

    def compile_words(self, idx: Index, comment: str) -> List[Word]:
        result: List[Word] = []
        words = re.split(r"\s", self.buff)
        for w in words:
            new_word = Word(idx, w, self.buff, variant=comment)
            if result:
                new_word.appendTo(result[-1])
            result.append(new_word)
        return result

    def compile_buffer(self, idx: Index, comments: Dict[int, Comment]) -> List[Word]:
        parts = set()
        for c in self.comments:
            if comments[c].annotation:
                if comments[c].annotation.startswith("om"):
                    parts.add(comments[c].annotation)
                else:
                    parts.add(LINE_CH)
        comment = ",".join(parts)
        return self.compile_words(idx, comment)

    def swap(self) -> None:
        self.line += self.buff

    def swap_clean(self) -> None:
        self.swap()
        self.buff = ""

    def build_context(self, new_words: List[Word]) -> None:
        words = merge(self.line_words, new_words)
        self.line_words = words
        for w in self.line_words:
            w.line_context = self.line

    def extract_comment(self, comments: Dict[int, Comment]) -> str:
        comment_parts = set([comments[c].annotation for c in self.comments])
        return ",".join(comment_parts)

    def __eq__(self, other) -> bool:
        if not other or type(other) != Buffer:
            return False
        if self.buff != other.buff or self.line != other.line:
            return False
        if len(self.line_words) != len(other.line_words) or len(
            self.comments != other.comments
        ):
            return False
        for i, w in enumerate(self.line_words):
            if w != other.line_words[i]:
                return False
        for i, c in enumerate(self.comments):
            if c != other.comments[i]:
                return False
        return True
