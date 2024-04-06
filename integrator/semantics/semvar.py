"""Functions for VarLangSemantics"""
from typing import Dict, List, Tuple

import re
from sortedcontainers import SortedDict, SortedSet  # type: ignore

from const import NON_COUNTABLE, H_LEMMA_SEP
from const import EMPTY_CH
from config import DEFAULT_SOURCES
from model import Source

from regex import multiword_regex, multilemma_regex

from .const import UNSPECIFIED
from .util import regroup


def collect_word(self, group: List[List[str]], grouped=False) -> str:
    """Collects the content of the multiwords for a variant in a group into a single string.
    The output is conformant with the multiword syntax.
    Yet it might contain redundancies, due to the normalisation process (split of equal variants).
    If part of a group, implicit variants interpreted as equal to main. Otherwise ommitted.
    """
    collected: Dict[Source, List[str]] = {}
    for row in group:
        for k, v in self.multiword(row).items():
            if not v.strip():
                continue
            for si in k:
                s = Source(si)
                if s not in collected:
                    collected[s] = []
                collected[s] += [v.strip()]
    if grouped:
        flipped = {}
        for ki, v in collected.items():
            k = Source(ki)
            t = tuple(v)
            if t not in flipped:
                flipped[t] = k
            else:
                flipped[t] += k
        result = regroup(
            {
                v: " ".join(k)
                for k, v in sorted(flipped.items(), key=lambda e: e[1])
                if any(k)
            }
        )
    else:
        result = regroup(
            {Source(k): " ".join(collected[k]) for k in collected if any(collected[k])}
        )
    final = " ".join([f"{v} {k}" if k else v for k, v in result.items() if v])
    return final


def collect_lemma(
    self, group: List[List[str]], cidx: int = UNSPECIFIED, separator: str = ""
) -> str:
    if cidx == UNSPECIFIED:
        cidx = self.lemmas[0]
    multis = [self.multilemma(r, self.lemmas.index(cidx)) for r in group]
    collected: Dict[Source, List[str]] = SortedDict()

    # for each row in group
    for m in multis:
        # for each variants group in lemma
        for k, v in m.items():
            current = list(iter(k))
            # for each source in variants group
            for cur_si in current:
                cur_s = Source(cur_si)
                found = False
                # for each of the previously detected variant sources
                for srci in collected:
                    src = Source(srci)
                    if cur_s in src:
                        found = True
                        if cur_s != src:
                            collected[cur_s] = collected[src]
                            collected[src - cur_s] = collected[src]
                            collected.pop(src)

                if not found:
                    collected[cur_s] = []
                collected[cur_s] += [v]

    glue = f" {separator} " if separator else " "
    result = regroup({k: glue.join(collected[k]).strip() for k in collected}, glue)
    g = [f"{v} {k}" if k else v for k, v in result.items() if v]

    return f" {H_LEMMA_SEP} ".join(g)


def multiword(self, row: List[str]) -> Dict[Source, str]:
    result: Dict[Source, str] = SortedDict()
    m = re.search(multiword_regex, row[self.word].strip())
    while m:
        s = Source(m.group(2))
        v = m.group(1).strip()
        result[s] = " ".join([result[s], v]) if s in result else v
        rest = m.group(4).strip()
        m = re.search(multiword_regex, rest)
    if not result:
        return {Source(DEFAULT_SOURCES[self.lang]): row[self.word].strip()}
        # return {'': row[self.word].strip()}

    # for k in result:
    #     if result[k] == OMMIT_SUBLEMMA:
    #         result[Source(~sum(result.keys()))] = row[self.main.word]
    #         result.pop(k)
    #         break

    return regroup(result)


def multilemma(self, row: List[str], lidx: int = 0) -> Dict[Source, str]:
    """Extract contents of multiple variants in a lemma as a dictionary.
    Args:
        row: List[str]
        lidx: int - sublemma level, index in the semantics list
    """
    result = SortedDict()
    m = re.search(multilemma_regex, row[self.lemmas[lidx]].strip())
    while m:
        # semantic and lemma
        v = m.group(1) if m.group(1) else ""
        # lemma annotation with plus
        v = v + m.group(4) if m.group(4) else v
        v = v.strip()

        # sources
        k = m.group(5) if m.group(5) else ""
        result[Source(k)] = v

        # remainder for next iteration
        rest = m.group(8) if len(m.groups()) == 8 else ""
        m = re.search(multilemma_regex, rest.strip())

    # When lemma in variant does not have source, read source from word or previous lemma
    # When in some variants word is missing, get lemma for this variant from main
    # When different variants have same lemma, unite. Case present only when deduced from different multiwords
    # TODO: When sublemma for some variants missing...
    if len(result) == 1 and next(iter(result.keys())) == Source():
        previdx = lidx - 1
        # find previous level with content
        while not row[self.lemmas[previdx]] and previdx >= 0:
            previdx -= 1
        # get lemmas for previous level
        prev_multi = (
            self.multilemma(row, previdx) if previdx >= 0 else self.multiword(row)
        )
        s = [str(k) for k, v in prev_multi.items() if v != EMPTY_CH]
        keys = Source(s)
        # keys = ""
        # for k, v in self.multiword(row).items():
        #     if v != EMPTY_CH:
        #         keys += k

        # words = {k: v for k, v in self.multiword(row).items() if v != EMPTY_CH}
        # assert len(words) == 1
        # return {next(iter(words.keys())): result[""]}
        if not result[Source()]:
            return {}
        return {keys: result[Source()]}

    return result


def compile_words_by_lemma(self, row: List[str], var: Source) -> Tuple[str, int]:
    """returns:
    1. concatenated pairs (word, variant)
    2. lemmas without variants
    3. repetition index in row
    TODO: Consider introducing a new data class
    """
    vars = SortedSet()
    lemmas = SortedSet()
    multiword = self.multiword(row)
    multilemma = self.multilemma(row)
    for v in var:
        for kw in multiword.keys():
            if not kw and v in Source(DEFAULT_SOURCES[self.lang]):
                vars.add(f"{multiword[Source()]} {kw}")
                lemmas.add(multilemma[Source()])
            elif v in kw and kw in multiword:
                vars.add(f"{multiword[kw]} {kw}")
                for m in multilemma.keys():
                    if kw in m:
                        lemmas.add(multilemma[m])
                        break
    # TODO: multiword counts need to distinguish between variants
    return (" ".join(vars), int(row[self.cnt_col]))


def add_count(self, row: List[str], row_counts: Dict[str, int]) -> Dict[str, int]:
    """based on first lemma (in column) expand row it with counter
    *IN PLACE*
    Updates both row and row_counts"""
    # TODO: multilemma counts need to distinguish between variants
    if not self.cnt_col:
        self.cnt_col = len(row)
    while len(row) < self.cnt_col + 1:
        row += ["1"]

    # Counts should be ignored, as they clearly don't exist before coming here
    if not row[self.lemmas[0]]:
        return row_counts
    multilemma = self.multilemma(row)
    for k, v in multilemma.items():
        if v in NON_COUNTABLE:
            continue
        if v in row_counts:
            row_counts[v] += 1
            row[self.cnt_col] = str(row_counts[v])
        else:
            row_counts[v] = 1
            # result += [f"{v[0]}{' ' if k else ''}{k}"]
            # fallback to default value for cnt in Index
    # row[self.lemmas[0]] = " ".join(result)
    return row_counts
