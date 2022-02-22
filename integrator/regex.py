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

source_regex = r"([A-Z]\w*)"

multiword_regex = r"^([^A-Z]+)(" + source_regex + r"+)(.*)$"
multilemma_regex = r"^([^A-Z\+]+)(\+\s\w+\.)?(" + source_regex + r"+)?(\s*[\&\/])?(.*)$"
