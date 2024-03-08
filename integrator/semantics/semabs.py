"""Functions for LangSemantics"""
from typing import Dict, List, Tuple

from const import NON_LEMMAS
from config import DEFAULT_SOURCES
from model import Alternative, Path, Source


def alternatives(
    self, row: List[str], my_var: Source = Source()
) -> Tuple[Alternative, Dict[Source, Alternative]]:
    """
    my_var is required for VarLangSemantics and ignored for MainLangSemantics
    """
    m = len(self.lemmas) - 1
    # lemma, word, repetition
    alt_main = Alternative()
    # sources to lemmas, sources to words, repetition (TODO: unclear how to interpret this one)
    alt_var: Dict[Source, Alternative] = {}

    # main
    # print(row)
    for l in range(m, -1, -1):
        if alt_main.lemma:
            break
        alt_main = self.level_main_alternatives(row, my_var, l)
        # print(alt_main)
        if alt_main.word in NON_LEMMAS:
            alt_main = Alternative()

    # var
    for l in range(m, -1, -1):
        # print(l)
        lvl_var = self.level_var_alternatives(row, my_var, l)
        for v in lvl_var.values():
            if v.lemma in NON_LEMMAS:
                alt_var = {}
                lvl_var = {}
        for v in lvl_var.keys():
            rem = v.remainder(alt_var.keys())
            if rem:
                alt_var[rem] = lvl_var[v]
                # iterate over sources in words, to catch all that are covered by this lemma
                for lv in lvl_var.keys():
                    if lv in v:
                        if rem in alt_var:
                            # print("if")
                            # TODO: what to do with repetitions
                            lem = (
                                alt_var[rem].lemma
                                if alt_var[rem].lemma
                                else lvl_var[lv].lemma
                            )
                            if alt_var[rem].semantic and lem.startswith(
                                alt_var[rem].semantic
                            ):
                                lem = lem[2:]
                            assert (
                                alt_var[rem].cnt == lvl_var[lv].cnt
                            ), f"Mismatch in counters at different levels between {alt_var} and {lvl_var}"
                            # sem = new_var[lv].semantic if new_var[lv].semantic else alt_var[rem].semantic
                            alt_var[lv] = Alternative(
                                alt_var[rem].word,
                                lem,
                                alt_var[rem].cnt,
                                alt_var[rem].semantic,
                            )
                            # alt_var[1][rem] = (
                            #     f"{alt_var[1][rem][0]} {new_var[1][lv][0]}",
                            #     alt_var[1][rem][1],
                            # )
                        else:
                            alt_var[rem] = lvl_var[lv]
            else:
                if v in alt_var:
                    if not alt_var[v].lemma:
                        alt_var[v] = Alternative(
                            alt_var[v].word,
                            lvl_var[v].lemma,
                            alt_var[v].cnt,
                            alt_var[v].semantic,
                        )
                else:
                    for var in alt_var.keys():
                        if var in v:
                            alt_var[var] = Alternative(
                                alt_var[var].word,
                                lvl_var[v].lemma,
                                alt_var[var].cnt,
                                alt_var[var].semantic,
                            )

    # print(alt_var)
    # return Alternative(alt_main[0], alt_var[0], alt_main[1], alt_var[1], alt_main[2])
    return (alt_main, alt_var)


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
            s = [str(k) for k in paths.keys()]
            keys = Source(s)
            multilemmas = {keys: next(iter(multilemmas.values()))}

        for k, v in multilemmas.items():
            for pk, path in paths.items():
                if pk.inside([k]) is not None:
                    path += v.strip()

    for k, path in paths.items():
        path.compile()

    return list(paths.values())
