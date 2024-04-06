from sortedcontainers import SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG, VAR_SOURCES
from model import Alternative, Index, Source, Alignment, Usage


def test_order_usage():
    assert Alignment(Index("1/6a8"), FROM_LANG) < Alignment(Index("1/6a17"), FROM_LANG)
    assert Alignment(Index("1/W167c4"), FROM_LANG) > Alignment(
        Index("1/6a8"), FROM_LANG
    )
    assert Alignment(Index("2/6a8"), FROM_LANG) > Alignment(
        Index("2/W167c4"), FROM_LANG
    )

    assert Alignment(Index("1/8b5-6"), FROM_LANG) > Alignment(Index("1/5a5"), FROM_LANG)
    assert Alignment(Index("1/5a5"), FROM_LANG) < Alignment(
        Index("3/11b2-3"), FROM_LANG
    )
    assert Alignment(Index("3/11b2-3"), FROM_LANG) > Alignment(
        Index("1/W168a14-15"), FROM_LANG
    )

    assert Alignment(Index("1/8a13"), FROM_LANG) > Alignment(
        Index("1/5d9(2)"), FROM_LANG
    )


def test_sort_usage():
    ss1 = SortedSet(
        [
            Alignment(Index("2/6a8"), Usage(FROM_LANG)),
            Alignment(Index("2/W167c4"), Usage(FROM_LANG)),
            Alignment(Index("1/W167c4"), Usage(FROM_LANG)),
            Alignment(Index("1/6a8"), Usage(FROM_LANG)),
        ]
    )
    assert ss1 == SortedSet(
        [
            Alignment(Index("1/6a8"), Usage(FROM_LANG)),
            Alignment(Index("1/W167c4"), Usage(FROM_LANG)),
            Alignment(Index("2/W167c4"), Usage(FROM_LANG)),
            Alignment(Index("2/6a8"), Usage(FROM_LANG)),
        ]
    )

    ss2 = SortedSet(
        [
            Alignment(
                Index("1/W168a25"),
                Usage(TO_LANG, word="μονογενοῦς"),
                Usage(
                    FROM_LANG,
                    Source("G"),
                    main_alt=Alternative(lemmas=["\ue201д\ue205но\ue20dѧдъ"]),
                    var_alt={"H": Alternative(lemmas=["\ue201д\ue205нородъ"])},
                ),
            ),
            Alignment(
                Index("1/5a4"),
                Usage(TO_LANG, word="μονογενὴς"),
                Usage(
                    FROM_LANG,
                    var_alt={"WH": Alternative(lemmas=["\ue201д\ue205но\ue20dѧдъ"])},
                ),
            ),
            Alignment(
                Index("1/4c15"),
                Usage(TO_LANG, word="μονογενοῦς"),
                Usage(
                    FROM_LANG,
                    var_alt={"WH": Alternative(lemmas=["\ue201д\ue205но\ue20dѧдъ"])},
                ),
            ),
            Alignment(
                Index("1/W168a25"),
                Usage(TO_LANG, word="μονογενοῦς"),
                Usage(
                    FROM_LANG,
                    Source("H"),
                    main_alt=Alternative(lemmas=["\ue201д\ue205но\ue20dѧдъ"]),
                    var_alt={"G": Alternative(lemmas=["\ue205но\ue20dѧдъ"])},
                ),
            ),
            Alignment(Index("1/W168a28"), Usage(TO_LANG, word="μονογενοῦς")),
            Alignment(
                Index("1/W168a25"),
                Usage(TO_LANG, word="μονογενοῦς"),
                Usage(
                    FROM_LANG,
                    var_alt={
                        "H": Alternative(lemmas=["\ue201д\ue205нородъ"]),
                        "G": Alternative(lemmas=["\ue205но\ue20dѧдъ"]),
                    },
                ),
            ),
            Alignment(
                Index("1/5a4"),
                Usage(TO_LANG, word="μονογενὴς"),
                Usage(
                    FROM_LANG,
                    Source("WH"),
                    main_alt=Alternative(lemmas=["\ue205но\ue20dѧдъ "]),
                ),
            ),
            Alignment(
                Index("1/4c15"),
                Usage(TO_LANG, word="μονογενοῦς"),
                Usage(
                    FROM_LANG,
                    Source("WH"),
                    main_alt=Alternative(lemmas=["\ue205но\ue20dѧдъ"]),
                ),
            ),
        ]
    )
    assert ss2 == SortedSet(
        [
            Alignment(
                Index("1/4c15"),
                Usage(TO_LANG, word="μονογενοῦς"),
                Usage(
                    FROM_LANG,
                    var_alt={"WH": Alternative(lemmas=["\ue201д\ue205но\ue20dѧдъ"])},
                ),
            ),
            Alignment(
                Index("1/4c15"),
                Usage(TO_LANG, word="μονογενοῦς"),
                Usage(
                    FROM_LANG,
                    Source("WH"),
                    main_alt=Alternative(lemmas=["\ue205но\ue20dѧдъ"]),
                ),
            ),
            Alignment(
                Index("1/5a4"),
                Usage(TO_LANG, word="μονογενὴς"),
                Usage(
                    FROM_LANG,
                    var_alt={"WH": Alternative(lemmas=["\ue201д\ue205но\ue20dѧдъ"])},
                ),
            ),
            Alignment(
                Index("1/5a4"),
                Usage(TO_LANG, word="μονογενὴς"),
                Usage(
                    FROM_LANG,
                    Source("WH"),
                    main_alt=Alternative(lemmas=["\ue205но\ue20dѧдъ "]),
                ),
            ),
            Alignment(
                Index("1/W168a25"),
                Usage(TO_LANG, word="μονογενοῦς"),
                Usage(
                    FROM_LANG,
                    var_alt={
                        "H": Alternative(lemmas=["\ue201д\ue205нородъ"]),
                        "G": Alternative(lemmas=["\ue205но\ue20dѧдъ"]),
                    },
                ),
            ),
            Alignment(Index("1/W168a28"), Usage(TO_LANG, word="μονογενοῦς")),
            Alignment(
                Index("1/W168a25"),
                Usage(TO_LANG, word="μονογενοῦς"),
                Usage(
                    FROM_LANG,
                    Source("G"),
                    main_alt=Alternative(lemmas=["\ue201д\ue205но\ue20dѧдъ"]),
                    var_alt={"H": Alternative(lemmas=["\ue201д\ue205нородъ"])},
                ),
            ),
            Alignment(
                Index("1/W168a25"),
                Usage(TO_LANG, word="μονογενοῦς"),
                Usage(
                    FROM_LANG,
                    Source("H"),
                    main_alt=Alternative(lemmas=["\ue201д\ue205но\ue20dѧдъ"]),
                    var_alt={"G": Alternative(lemmas=["\ue205но\ue20dѧдъ"])},
                ),
            ),
        ]
    )


def test_alternative():
    assert Alternative(
        "невел\ue205\ue20dан\ue205\ue201", ["невел\ue205\ue20dан\ue205\ue201"]
    ) != Alternative(
        "невел\ue205\ue20dан\ue205\ue201", ["невел\ue205\ue20dан\ue205\ue201"], 2
    )

    assert Alignment(
        Index("5/21a19"),
        Usage(
            FROM_LANG,
            Source("WGH"),
            "невел\ue205\ue20d\ue205\ue201 WGH",
            main_alt=Alternative(
                "невел\ue205\ue20dан\ue205\ue201", ["невел\ue205\ue20dан\ue205\ue201"]
            ),
        ),
        Usage(TO_LANG, cnt=2),
    ) != Alignment(
        Index("5/21a19"),
        Usage(
            FROM_LANG,
            Source("WGH"),
            "невел\ue205\ue20d\ue205\ue201 WGH",
            main_alt=Alternative(
                "невел\ue205\ue20dан\ue205\ue201",
                ["невел\ue205\ue20dан\ue205\ue201"],
                2,
            ),
        ),
        Usage(TO_LANG, cnt=2),
    )


def test_inside():
    assert Source("HGW").inside([Source("WGH")]) == Source("WGH")
    assert Source("M").inside(Source("M"))

    assert Source("").inside([Source("")]) == Source("")
    assert Source("").inside([Source("B")]) == None
    assert Source("Pa").inside(VAR_SOURCES["gr"]) == Source(VAR_SOURCES["gr"])
