from typing import Tuple, List

from sortedcontainers import SortedDict  # type: ignore

html = """
<html>
<head>
<style>
.sl {
    font-family: CyrillicaOchrid10U
}

.gr {
    font-family: Times New Roman
}
</style>
</head>
<body>
%s
</body>
</html>
"""


def html_usage(key: Tuple[str, str], usage: List[str]) -> str:
    u = ",".join(usage)
    return (
        f"""<span class="sl">{key[0]}</span>/<span class="gr">{key[1]}</span>({u});"""
    )


def export_html(d: SortedDict, fname: str) -> None:
    # TODO: swap styles for greek
    body = ""
    for l1, d1 in d.items():
        body += f"<h1>{l1}</h1>\n"
        for l2, d2 in d1.items():
            if l2:
                body += f"<h2>{l2}</h2>\n"
            for l3, d3 in d2.items():
                if l3:
                    body += f"<h3>{l3}</h3>\n"
                body += "".join([html_usage(key, u) for key, u in d3.items()]) + "\n"
    with open(fname, "w") as f:
        f.write(html % body)
