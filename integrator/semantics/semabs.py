"""Functions for LangSemantics"""
from typing import Dict, List, Tuple
from sortedcontainers import SortedDict  # type: ignore

from const import NON_LEMMAS, SPECIAL_CHARS, EMPTY_CH
from config import DEFAULT_SOURCES, ORDERED_SOURCES
from model import Alternative, Path, Source

from .util import simplify_alternatives


def var_alt_lemmas(self, row: List[str]) -> Dict[Source, List[str]]:
    assert self.var, "non-null value required by mypy"
    # vars = self.multiword(row)
    # print(row)
    result: Dict[Source, List[str]] = {}
    # for v in vars.keys():
    for l, _ in enumerate(self.var.lemmas):
        ml = self.var.multilemma(row, l)
        # for s in v:
        for k, v in ml.items():
            if not v:
                continue
            for s in k:
                if s not in result:
                    assert (
                        l == 0
                    ), f"Source {s} is not initialised in {result}. But this should be done in first lemma, not at level {l}"
                    result[s] = []
                result[s] += [v]
    return result


def alternatives(
    self, row: List[str], my_var: Source = Source()
) -> Tuple[Alternative, Dict[Source, Alternative]]:
    """
    my_var is required for VarLangSemantics and ignored for MainLangSemantics
    """
    # lemma, word, repetition
    alt_main = Alternative()
    # sources to lemmas, sources to words, repetition (TODO: unclear how to interpret this one)
    alt_var = SortedDict()

    # main
    if self.main.lemmas[0] and self.main.word not in NON_LEMMAS:
        main_lemmas = self.main_alt_lemmas(row, my_var)
        semantic = ""
        # print(main_lemmas)
        if main_lemmas:
            if main_lemmas[-1][0] in SPECIAL_CHARS:
                semantic = main_lemmas[-1][0]
                if len(main_lemmas[-1]) > 2:
                    main_lemmas[-1] = main_lemmas[-1][2:]
                else:
                    main_lemmas.pop(-1)
            alt_main = Alternative(
                row[self.main.word], main_lemmas, int(row[self.main.cnt_col]), semantic
            )

    # var
    if row[self.var.lemmas[0]]:
        vml = self.var.multiword(row)
        var_lemmas = self.var_alt_lemmas(row)
        for mw_src, mw_word in vml.items():
            if mw_word == EMPTY_CH:
                continue
            for s in mw_src:
                # if variant in word usages, but not in lemmas, ignore it?
                if s not in var_lemmas:
                    continue
                # if s in my_var:
                #     continue
                semantic = ""
                # print(var_lemmas)
                if var_lemmas[s][-1][0] in SPECIAL_CHARS:
                    semantic = var_lemmas[s][-1][0]
                    # if remainder contains actual lemma (i.e. not empty or source only)
                    if len(var_lemmas[s][-1]) > 2 and any(
                        s for s in var_lemmas[s][-1][2:] if s not in ORDERED_SOURCES
                    ):
                        var_lemmas[s][-1] = var_lemmas[s][-1][2:]
                    else:
                        var_lemmas[s].pop(-1)
                # print(self.var.cnt_col)
                alt_var[s] = Alternative(
                    mw_word, var_lemmas[s], int(row[self.var.cnt_col]), semantic
                )
                # print(alt_var)

    my_alt = alt_main if self.main == self else alt_var[next(iter(my_var))]

    # remove equal to mine
    if my_alt.same(alt_main):
        alt_main = Alternative()
    alt_var = {s: a for s, a in alt_var.items() if not a.same(my_alt)}
    alt_var = simplify_alternatives(alt_var)

    # print(alt_var)
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

    # WIP
    for k, path in paths.items():
        path.compile()

    return list(paths.values())
