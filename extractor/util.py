from typing import Dict, List, Set, Union

import re

from const import LINE_CH
from model import Comment, Index, Word


def link_tokens(tokens: List[Word]) -> List[Word]:
    if not tokens:
        return tokens
    for i in range(len(tokens)):
        if i == len(tokens) - 1:
            break
        tokens[i].next = tokens[i + 1]
        tokens[i + 1].prev = tokens[i]
    return tokens


def merge(head: List[Word], tail: List[Word]) -> List[Word]:
    """Returns first parameter"""
    if head:
        head[-1].prependTo(tail[0])
    head += tail
    return head


class WordList:
    """ linked list of Word objects"""

    def __init__(self):
        self._words = []

    def __iadd__(self, other: Union["WordList", Word]) -> "WordList":
        if type(other) == WordList:
            old_len = len(self._words)
            self._words = merge(self._words, other._words)  # type: ignore
            assert len(self._words) == old_len + len(other._words)  # type: ignore
        elif type(other) == Word:
            old_len = len(self._words)
            if self._words:
                other.appendTo(self._words[-1])  # type: ignore
            self._words.append(other)  # type: ignore
            assert old_len + 1 == len(self._words)
        return self

    def __getitem__(self, i) -> Word:
        return self._words[i]

    def __setitem__(self, i, v):
        self._words[i] = v

    def __iter__(self):
        return iter(self._words)

    def __len__(self) -> int:
        return len(self._words)

    def __str__(self) -> str:
        return ";".join([str(w) for w in self._words])

    def __repr__(self) -> str:
        return repr(self._words)


class Buffer:
    """ Handles processing of current text, lines and comments"""

    def __init__(self, buffer: str = ""):
        self.reset()
        self.comments: Set[int] = set()  # Currently open comments
        self.buff = buffer

    def add(self, text: str) -> None:
        self.buff += text

    def reset(self) -> None:
        self.buff = ""
        self.line = ""
        self.line_words = WordList()

    def compile_words(self, idx: Index, comment: str) -> WordList:
        result = WordList()
        words = re.split(r"\s", self.buff)
        for w in words:
            result += Word(idx, w, self.buff, variant=comment)
        return result

    def compile_buffer(self, idx: Index, comments: Dict[int, Comment]) -> WordList:
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

    def build_context(self, new_words: WordList) -> None:
        self.line_words += new_words
        for w in self.line_words:
            w.line_context = self.line

    def extract_comment(self, comments: Dict[int, Comment]) -> str:
        # TODO: should this follow the same logic as the one in compile_buffer?
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
