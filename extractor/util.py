from typing import Dict, List, Set

import re

from const import LINE_CH
from model import Comment, Index, Word, WordList


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
