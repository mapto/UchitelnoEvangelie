from const import V_LEMMA_SEP, H_LEMMA_SEP

# built with regex101.com

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
word_regex = r"(\S[^A-Z\+]*)"

sources_regex = r"([A-Z]\w*)"

# multiword_regex = r"^([^A-Z]+)(" + sources_regex + r"+)(.*)$"
# multiword_regex = r"^(\w[^A-Z]*)(" + sources_regex + r"+)(.*)$"
multiword_regex = r"^" + word_regex + "(" + sources_regex + r"+)(.*)$"

# TODO: accepting both & and / as separators is not neccessary
# TODO: & is not expected to be used
multilemma_regex = (
    # r"^([^A-Z\+]+)(\+\s\w+\.\s?)?("
    r"^"
    + word_regex
    + r"(\+\s?\w+\.?\s?)?("
    + sources_regex
    + r"+)?(\s*["
    + f"\\{V_LEMMA_SEP}\\{H_LEMMA_SEP}"
    + r"])?(.*)$"
)
