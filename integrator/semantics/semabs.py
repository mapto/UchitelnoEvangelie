"""Functions for LangSemantics"""
from typing import Dict, List, Tuple

from const import NON_LEMMAS
from config import DEFAULT_SOURCES
from model import Alternative, Path, Source

from .util import remove_repetitions


def alternatives(self, row: List[str], my_var: Source) -> Alternative:
    m = len(self.lemmas) - 1
    alt_main = ("", "", 1)
    alt_var: Tuple[Dict[Source, str], Dict[Source, Tuple[str, int]]] = ({}, {})
    for l in range(m, -1, -1):
        if not alt_main[0]:
            alt_main = self.level_main_alternatives(row, my_var, l)
            if alt_main[0] in NON_LEMMAS:
                alt_main = ("", "", 1)
        if not alt_var[0]:
            alt_var = self.level_var_alternatives(row, my_var, l)
            for v in alt_var[0].values():
                if v in NON_LEMMAS:
                    alt_var = ({}, {})
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
