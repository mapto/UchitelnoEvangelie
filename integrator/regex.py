# built with regex101.com
idx_regex = (
    r"(\d{1,2})\/(W)?(\d{1,3})([a-d])(\d{1,2})(\{(\d)\})?(\{(\d)\})?"
    + r"(-((((\d{1,2})\/)?(W)?(\d{1,3}))?([a-d]))?(\d{1,2})(\{(\d)\})?(\{(\d)\})?)?"
)
source_regex = r"([A-Z]\w*)"
multiword_regex = r"^([^A-Z]+)(" + source_regex + r"+)(.*)$"
multilemma_regex = r"^([^A-Z\+]+)(\+\s\w+\.)?(" + source_regex + r"+)?(\s*[\&\/])?(.*)$"
