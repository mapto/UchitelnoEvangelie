#!/usr/bin/env python3
"""To debug use:
https://www.debuggex.com/ for visualisation
https://regex101.com/ for breakdown
"""
from typing import Final
import logging as log

if __name__ == "__main__":
    log.DEBUG = 100

from const import V_LEMMA_SEP, H_LEMMA_SEP, SPECIAL_CHARS
from config import VAR_GR, VAR_SL

# two numbers encoding repetition index: in original and in translation
counter_regex = r"(\[(\d)\])?(\{(\d)\})?"

address_regex = (
    r"(\d{1,3})\W(W)?(\d{1,3})?([a-d])?(\d{1,2})?"
    + counter_regex
    + r"(-((((\d{1,3})\W)?(W)?(\d{1,3}))?([a-d]))?(\d{1,2})"
    + counter_regex
    + r")?"
)

# uppercase Latin letters and + have special function,
# thus used as delimiters in regex, even if reading continues in lemmas
sem_regex = r"([" + "".join(SPECIAL_CHARS) + "] )?"
# word_regex = r"([^A-Z\r\n\t\f\v\+]+)"
lemma_regex = r"([^A-Za-z\r\n\t\f\v\+^\(]*)"
w_annot_regex = r"\w+\."
l_annot_regex = r"(\w+\.|\(.*\))"
word_regex = r"(([^A-Za-z\r\n\t\f]|" + w_annot_regex + ")+)"
# sources_regex = r"([A-Z]\w*)"

# The regex parser is greedy. Thus we want "Ma" to show before "M", so that it gets it.
UNIFIED_SOURCES = VAR_SL + VAR_GR
UNIFIED_SOURCES.sort()
sources_regex = r"(" + "|".join(UNIFIED_SOURCES[::-1]) + ")"
sources_block_regex = r"(" + sources_regex + r"+)?"

# When modifying this, make sure to reindex groups in semvar->multiword()
# multiword_regex = r"^([^A-Z]+)(" + sources_regex + r"+)(.*)$"
# multiword_regex = r"^(\w[^A-Z]*)(" + sources_regex + r"+)(.*)$"
multiword_regex = r"^" + word_regex + sources_block_regex + "(.*)$"
# multiword_regex = (
#     r"^"
#     + lemma_regex
#     + r"( ?"
#     + annot_regex
#     + r"\s?)?("
#     + sources_regex
#     + r"+)?(.*)$"
# )
log.debug(f"multiword regex:  {multiword_regex}")


# TODO: accepting both & and / as separators is not neccessary
# TODO: & is not expected to be used
# Only last lemma could contain semantics
# When modifying this, make sure to reindex groups below
multilemma_regex = (
    # r"^([^A-Z\+]+)(\+\s\w+\.\s?)?("
    r"^"
    + "("
    + sem_regex
    + lemma_regex
    + ")"
    + r"( ?(\+ )?"
    + l_annot_regex
    + r"\s?)?"
    + sources_block_regex
    + r"(\s*["
    + f"\\{V_LEMMA_SEP}\\{H_LEMMA_SEP}"
    + r"])?(.*)$"
)
log.debug(f"multilemma regex: {multilemma_regex}")

# Lemma positions (LP):
# Prefix
LP_PRE: Final = 2
# Lemma
LP_LEM: Final = 3
# Annotation
LP_ANN: Final = 4
# Sources
LP_SRC: Final = 7
# Separator
LP_SEP: Final = 9
# Next lemma combination
LP_OTHER: Final = 10
