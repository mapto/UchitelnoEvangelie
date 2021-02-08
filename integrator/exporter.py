from typing import Tuple, List

from sortedcontainers import SortedDict, SortedList  # type: ignore

from docx import Document  # type: ignore
from docx.shared import RGBColor, Pt  # type: ignore

html = """
<html>
<head>
</head>
<body>
%s
</body>
</html>
"""

fonts = {"gr": "Times New Roman", "sl": "CyrillicaOchrid10U"}
colors = {"gr": RGBColor(0x55, 0x00, 0x00), "sl": RGBColor(0x00, 0x00, 0x55)}


def html_usage(key: Tuple[str, str], usage: List[str], src_style: str) -> str:
    u = ",".join(usage)
    other_style = "gr" if src_style == "sl" else "sl"
    return (
        f"""<span style="font-family: {fonts[src_style]}">{key[0]}</span>/<span class="font-family: {fonts[other_style]}">{key[1]}</span>({u});"""
        # f"""<span class="{src_style}">{key[0]}</span>/<span class="{other_style}">{key[1]}</span>({u}); """
    )


def export_html(d: SortedDict, src_style: str, fname: str) -> None:
    # TODO: swap styles for greek
    body = ""
    for l1, d1 in d.items():
        body += f"""<h2 style="font-family: {fonts[src_style]}">{l1}</h1>\n"""
        for l2, d2 in d1.items():
            if l2:
                body += f"""<h3 style="font-family: {fonts[src_style]}">| {l2}</h2>\n"""
            for l3, d3 in d2.items():
                if l3:
                    body += f"""<h4 style="font-family: {fonts[src_style]}">|| {l3}</h3>\n"""
                body += (
                    "<ul><li>"
                    + " ".join([html_usage(key, u, src_style) for key, u in d3.items()])
                    + "</li></ul>\n"
                )
    with open(fname, "w") as f:
        f.write(html % body)


def docx_usage(par, key: Tuple[str, str], usage: List[str], src_style: str) -> None:
    """
    key: (word,translation)
    usage: list of indices of usages also containing their styles
    """
    other_style = "gr" if src_style == "sl" else "sl"

    run = par.add_run()
    run.font.name = fonts[src_style]
    run.font.color.rgb = colors[src_style]
    run.add_text(key[0])

    run = par.add_run()
    run.add_text("/")

    run = par.add_run()
    run.font.name = fonts[other_style]
    run.font.color.rgb = colors[other_style]
    run.add_text(f"{key[1]} (")

    first = True
    for next in usage:
        if not first:
            run = par.add_run()
            run.add_text(", ")
        run = par.add_run()
        # extract style from string
        (idx, style) = next.split("~")
        run.font.bold = "bold" in style
        run.font.italic = "italic" in style
        run.add_text(idx)
        first = False
    run = par.add_run()
    run.add_text("); ")


def _export_line(level: int, lang: str, d: SortedDict, doc: Document):
    """Builds the hierarchical entries of the dictionary. Recursion ensures that this works with variable depth.

    Args:
        level (int): 0-indexed depth, runs along with dict depth
        lang (str): original language
        d (SortedDict): level of dictionary to be exported
        doc (Document): export document
    """
    for li, next_d in d.items():
        if li:
            run = doc.add_paragraph().add_run()
            run.font.name = fonts[lang]
            run.font.size = Pt(18 - 2 * level)
            run.add_text(f"{'| '*level} {li}")
        any_child = next(iter(next_d.values()))
        any_of_any = next(iter(any_child.values()))
        if type(any_of_any) is SortedList:
            trans_lang = "gr" if lang == "sl" else "sl"
            for t, bottom_d in next_d.items():
                par = doc.add_paragraph()
                par.paragraph_format.left_indent = Pt(20)
                par.paragraph_format.first_line_indent = Pt(-10)
                run = par.add_run()
                run.font.name = fonts[trans_lang]
                run.add_text(t + ": ")
                for key, usage in bottom_d.items():
                    docx_usage(par, key, usage, lang)
        else:
            _export_line(level + 1, lang, next_d, doc)


def export_docx(d: SortedDict, lang: str, fname: str) -> None:
    doc = Document()
    _export_line(0, lang, d, doc)
    doc.save(fname)
