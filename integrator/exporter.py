from typing import Tuple, List

from sortedcontainers import SortedDict  # type: ignore

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
    u = ",".join(usage)
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
    run.add_text(key[1])

    run = par.add_run()
    run.add_text(f"({u}); ")


def export_docx(d: SortedDict, src_style: str, fname: str) -> None:
    other_style = "gr" if src_style == "sl" else "sl"
    doc = Document()
    for l1, d1 in d.items():
        run = doc.add_paragraph().add_run()
        run.font.name = fonts[src_style]
        run.font.size = Pt(18)
        run.add_text(l1)
        for l2, d2 in d1.items():
            if l2:
                run = doc.add_paragraph().add_run()
                run.font.name = fonts[src_style]
                run.font.size = Pt(16)
                run.add_text("| " + l2)
            for l3, d3 in d2.items():
                if l3:
                    run = doc.add_paragraph().add_run()
                    run.font.name = fonts[src_style]
                    run.font.size = Pt(14)
                    run.add_text("|| " + l3)
                for t, d4 in d3.items():
                    par = doc.add_paragraph()
                    par.paragraph_format.left_indent = Pt(20)
                    par.paragraph_format.first_line_indent = Pt(-10)
                    run = par.add_run()
                    run.font.name = fonts[other_style]
                    run.add_text(t + ": ")
                    for key, u in d4.items():
                        docx_usage(par, key, u, src_style)

    doc.save(fname)
