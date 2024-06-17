"""To debug use:
https://www.debuggex.com/ for visualisation
https://regex101.com/ for breakdown
"""
import logging as log
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
lemma_regex = r"([^A-Za-z\r\n\t\f\v\+]*)"
word_regex = r"([^([A-Za-z](a-z)?)\r\n\t\f\v]*)"
annot_regex = r"\w+\."
# sources_regex = r"([A-Z]\w*)"

# The regex parser is greedy. Thus we want "Ma" to show before "M", so that it gets it.
UNIFIED_SOURCES = VAR_SL + VAR_GR
UNIFIED_SOURCES.sort()
sources_regex = r"(" + "|".join(UNIFIED_SOURCES[::-1]) + ")"

# multiword_regex = r"^([^A-Z]+)(" + sources_regex + r"+)(.*)$"
# multiword_regex = r"^(\w[^A-Z]*)(" + sources_regex + r"+)(.*)$"
multiword_regex = r"^" + word_regex + "(" + sources_regex + r"+)(.*)$"
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
multilemma_regex = (
    # r"^([^A-Z\+]+)(\+\s\w+\.\s?)?("
    r"^"
    + "("
    + sem_regex
    + lemma_regex
    + ")"
    + r"( ?(\+ )?"
    + annot_regex
    + r"\s?)?("
    + sources_regex
    + r"+)?(\s*["
    + f"\\{V_LEMMA_SEP}\\{H_LEMMA_SEP}"
    + r"])?(.*)$"
)
log.debug(f"multilemma regex: {multilemma_regex}")
