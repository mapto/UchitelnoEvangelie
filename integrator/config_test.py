# TODO: test that verifies that same source siglas are not used for different languages

from config import parse_sources, source_cfg


def test_parse_sources():
    """This depends on source configuration files. TODO parse separately"""
    gr_sources = parse_sources("gr")
    assert gr_sources == (
        "C",
        [
            "Cs",
            "Ab",
            "Fa",
            "Fb",
            "Fc",
            "La",
            "M",
            "Mi",
            "Md",
            "Pb",
            "Pc",
            "Pd",
            "Pe",
            "Pf",
            "Pg",
            "Ph",
            "Pi",
            "Pk",
            "Pl",
            "Pp",
            "R",
            "T",
            "V",
            "Va",
            "Vb",
            "Vc",
            "Vd",
            "Y",
            "Za",
            "A",
            "Fd",
            "L",
            "Ma",
            "B",
            "P",
            "Pa",
            "Po",
            "Sp",
            "Z",
            "Pm",
            "Pn",
            "Ve",
            "Ch",
            "Nt",
            "S",
        ],
    )

    sl_sources = parse_sources("sl")
    sl_sources == ("S", ["W", "G", "H"])
