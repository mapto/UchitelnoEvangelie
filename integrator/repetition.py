from typing import Dict, List

from const import IDX_COL
from setup import sl_sem, gr_sem


class Repetitions:
    """Manages counting of repetitions within a single address,
    i.e. distinguishing the different occurences of the same lemma (and possibly word) on the same line of the original document.
    Done for first lemmas of all four groups.
    Notice that order of counts is always the same, regardless of direction of merging.
    Note: Repetitions might not be detected well if first instance does not have row number."""

    orig = gr_sem
    trans = sl_sem

    def __init__(self) -> None:
        self.prev_idx = ""
        self.orig_main: Dict[str, int] = {}
        self.orig_var: Dict[str, int] = {}
        self.trans_main: Dict[str, int] = {}
        self.trans_var: Dict[str, int] = {}

    def update(self, row: List[str]):
        """If line changes reset counters. Then independently check if already present, and if so augment respective counter.
        Adds 4 columns at end of row *IN PLACE*
        """
        # initialize counters
        if self.prev_idx != row[IDX_COL]:
            self.prev_idx = row[IDX_COL]
            self.orig_main = {}
            self.orig_var = {}
            self.trans_main = {}
            self.trans_var = {}

        # based on lemma column expand data with it with count in a column at the end
        self.orig_main = self.orig.add_count(row, self.orig_main)
        self.orig_var = self.orig.other().add_count(row, self.orig_var)
        self.trans_main = self.trans.add_count(row, self.trans_main)
        self.trans_var = self.trans.other().add_count(row, self.trans_var)

    def __str__(self) -> str:
        return f"{self.orig.lang}: [{self.orig_main}; {self.orig_var}]; {self.trans.lang}: [{self.trans_main}; {self.trans_var}]"
