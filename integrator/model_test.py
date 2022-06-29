from sortedcontainers import SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import VAR_SOURCES
from model import Alternative, Index, Source, Usage, UsageContent


def test_order_usage():
    assert Usage(Index("1/6a8"), FROM_LANG) < Usage(
        Index("1/6a17"), FROM_LANG
    )
    assert Usage(Index("1/6a8"), FROM_LANG) < Usage(
        Index("1/W167c4"), FROM_LANG
    )
    assert Usage(Index("2/6a8"), FROM_LANG) > Usage(
        Index("2/W167c4"), FROM_LANG
    )

    assert Usage(Index("1/8b5-6"), FROM_LANG) > Usage(
        Index("1/5a5"), FROM_LANG
    )
    assert Usage(Index("1/5a5"), FROM_LANG) < Usage(
        Index("3/11b2-3"), FROM_LANG
    )
    assert Usage(Index("3/11b2-3"), FROM_LANG) > Usage(
        Index("1/W168a14-15"), FROM_LANG
    )

    assert Usage(Index("1/8a13"), FROM_LANG) > Usage(
        Index("1/5d9(2)"), FROM_LANG
    )


def test_sort_usage():
    ss1 = SortedSet(
        [
            Usage(Index("2/6a8"), UsageContent(FROM_LANG)),
            Usage(Index("2/W167c4"), UsageContent(FROM_LANG)),
            Usage(Index("1/W167c4"), UsageContent(FROM_LANG)),
            Usage(Index("1/6a8"), UsageContent(FROM_LANG)),
        ]
    )
    assert ss1 == SortedSet(
        [
            Usage(Index("1/6a8"), UsageContent(FROM_LANG)),
            Usage(Index("1/W167c4"), UsageContent(FROM_LANG)),
            Usage(Index("2/W167c4"), UsageContent(FROM_LANG)),
            Usage(Index("2/6a8"), UsageContent(FROM_LANG)),
        ]
    )

    ss2 = SortedSet(
        [
            Usage(
                Index("1/W168a25"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
                UsageContent(
                    FROM_LANG,
                    Source("G"),
                    Alternative(
                        "\ue201д\ue205но\ue20dѧдъ", {"H": "\ue201д\ue205нородъ"}
                    ),
                ),
            ),
            Usage(
                Index("1/5a4"),
                UsageContent(TO_LANG, word="μονογενὴς"),
                UsageContent(
                    FROM_LANG,
                    alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
                ),
            ),
            Usage(
                Index("1/4c15"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
                UsageContent(
                    FROM_LANG,
                    alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
                ),
            ),
            Usage(
                Index("1/W168a25"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
                UsageContent(
                    FROM_LANG,
                    Source("H"),
                    alt=Alternative(
                        "\ue201д\ue205но\ue20dѧдъ", {"G": "\ue205но\ue20dѧдъ"}
                    ),
                ),
            ),
            Usage(
                Index("1/W168a28"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
            ),
            Usage(
                Index("1/W168a25"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
                UsageContent(
                    FROM_LANG,
                    alt=Alternative(
                        var_lemmas={
                            "H": "\ue201д\ue205нородъ",
                            "G": "\ue205но\ue20dѧдъ",
                        }
                    ),
                ),
            ),
            Usage(
                Index("1/5a4"),
                UsageContent(
                    TO_LANG,
                    word="μονογενὴς",
                ),
                UsageContent(
                    FROM_LANG, Source("WH"), alt=Alternative("\ue205но\ue20dѧдъ ")
                ),
            ),
            Usage(
                Index("1/4c15"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
                UsageContent(
                    FROM_LANG, Source("WH"), alt=Alternative("\ue205но\ue20dѧдъ")
                ),
            ),
        ]
    )
    assert ss2 == SortedSet(
        [
            Usage(
                Index("1/4c15"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
                UsageContent(
                    FROM_LANG,
                    alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
                ),
            ),
            Usage(
                Index("1/4c15"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
                UsageContent(
                    FROM_LANG, Source("WH"), alt=Alternative("\ue205но\ue20dѧдъ")
                ),
            ),
            Usage(
                Index("1/5a4"),
                UsageContent(
                    TO_LANG,
                    word="μονογενὴς",
                ),
                UsageContent(
                    FROM_LANG,
                    alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
                ),
            ),
            Usage(
                Index("1/5a4"),
                UsageContent(
                    TO_LANG,
                    word="μονογενὴς",
                ),
                UsageContent(
                    FROM_LANG, Source("WH"), alt=Alternative("\ue205но\ue20dѧдъ ")
                ),
            ),
            Usage(
                Index("1/W168a25"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
                UsageContent(
                    FROM_LANG,
                    alt=Alternative(
                        var_lemmas={
                            "H": "\ue201д\ue205нородъ",
                            "G": "\ue205но\ue20dѧдъ",
                        }
                    ),
                ),
            ),
            Usage(
                Index("1/W168a28"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
            ),
            Usage(
                Index("1/W168a25"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
                UsageContent(
                    FROM_LANG,
                    Source("G"),
                    alt=Alternative(
                        "\ue201д\ue205но\ue20dѧдъ", {"H": "\ue201д\ue205нородъ"}
                    ),
                ),
            ),
            Usage(
                Index("1/W168a25"),
                UsageContent(
                    TO_LANG,
                    word="μονογενοῦς",
                ),
                UsageContent(
                    FROM_LANG,
                    Source("H"),
                    alt=Alternative(
                        "\ue201д\ue205но\ue20dѧдъ", {"G": "\ue205но\ue20dѧдъ"}
                    ),
                ),
            ),
        ]
    )


def test_alternative():
    assert Alternative(
        main_lemma="невел\ue205\ue20dан\ue205\ue201",
        main_word="невел\ue205\ue20dан\ue205\ue201",
        main_cnt=1,
    ) != Alternative(
        main_lemma="невел\ue205\ue20dан\ue205\ue201",
        main_word="невел\ue205\ue20dан\ue205\ue201",
        main_cnt=2,
    )

    assert Usage(
        Index("5/21a19"),
        UsageContent(
            FROM_LANG,
            Source("WGH"),
            alt=Alternative(
                main_lemma="невел\ue205\ue20dан\ue205\ue201",
                main_word="невел\ue205\ue20dан\ue205\ue201",
                main_cnt=1,
            ),
            word="невел\ue205\ue20d\ue205\ue201 WGH",
        ),
        UsageContent(TO_LANG, cnt=2),
    ) != Usage(
        Index("5/21a19"),
        UsageContent(
            FROM_LANG,
            Source("WGH"),
            alt=Alternative(
                main_lemma="невел\ue205\ue20dан\ue205\ue201",
                main_word="невел\ue205\ue20dан\ue205\ue201",
                main_cnt=2,
            ),
            word="невел\ue205\ue20d\ue205\ue201 WGH",
        ),
        UsageContent(TO_LANG, cnt=2),
    )


def test_inside():
    assert Source("HGW").inside([Source("WGH")]) == Source("WGH")
    assert Source("M").inside(Source("M"))

    assert Source("").inside([Source("")]) == Source("")
    assert Source("").inside([Source("B")]) == None
    assert Source("Pa").inside(VAR_SOURCES["gr"]) == Source(VAR_SOURCES["gr"])
