"""Functions for LangSemantics"""
from typing import Dict, List, Tuple

from const import NON_LEMMAS
from config import DEFAULT_SOURCES
from model import Alternative, Path, Source

from .util import remove_repetitions


def alternatives(self, row: List[str], my_var: Source = Source()) -> Alternative:
    """
    my_var is required for VarLangSemantics and ignored for MainLangSemantics
    """
    m = len(self.lemmas) - 1
    # lemma, word, repetition
    alt_main = ("", "", 1)
    # sources to lemmas, sources to words, repetition (TODO: unclear how to interpret this one)
    alt_var: Tuple[Dict[Source, str], Dict[Source, Tuple[str, int]]] = ({}, {})
    for l in range(m, -1, -1):
        if alt_main[0]:
            break
        alt_main = self.level_main_alternatives(row, my_var, l)
        if alt_main[0] in NON_LEMMAS:
            alt_main = ("", "", 1)

    for l in range(m, -1, -1):
        new_var = self.level_var_alternatives(row, my_var, l)
        for v in new_var[0].values():
            if v in NON_LEMMAS:
                alt_var = ({}, {})
                new_var = ({}, {})
        for v in new_var[0].keys():
            rem = v.remainder(alt_var[0].keys())
            if rem:
                alt_var[0][rem] = new_var[0][v]
                alt_var[1][rem] = new_var[1][v]

    return Alternative(alt_main[0], alt_var[0], alt_main[1], alt_var[1], alt_main[2])


def build_paths(self, row: List[str]) -> List[Path]:
    """Build the multipaths (due to multilemma) relevant to the current row"""
    # first lemma in variant could contain multilemma
    multilemmas = self.multilemma(row)
    if not multilemmas:
        return [Path()]
    paths = {k: Path([v.strip()]) for k, v in multilemmas.items()}
    if self.is_variant() and len(paths) == 1 and next(iter(paths.keys())) == "":
        keys = Source(DEFAULT_SOURCES[self.lang])
        paths = {keys: next(iter(paths.values()))}

    # other lemmas could contain multilemmas with less sources
    for c in range(1, len(self.lemmas)):
        w = row[self.lemmas[c]].strip()
        if not w:
            continue
        multilemmas = self.multilemma(row, c)
        if (
            self.is_variant()
            and len(multilemmas) == 1
            and next(iter(multilemmas.keys())) == ""
        ):
            s = {str(k) for k in paths.keys()}
            keys = Source(remove_repetitions("".join(s)))
            multilemmas = {keys: next(iter(multilemmas.values()))}

        for k, v in multilemmas.items():
            for pk, path in paths.items():
                if pk.inside([k]) is not None:
                    path += v.strip()

    for k, path in paths.items():
        path.compile()

    return list(paths.values())
