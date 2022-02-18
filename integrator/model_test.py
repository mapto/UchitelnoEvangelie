from sortedcontainers import SortedSet  # type: ignore
from address import Index
from model import Alternative, Source, Usage


def test_order_usage():
    assert Usage(Index.unpack("1/6a8"), "sl") < Usage(Index.unpack("1/6a17"), "sl")
    assert Usage(Index.unpack("1/6a8"), "sl") < Usage(Index.unpack("1/W167c4"), "sl")
    assert not Usage(Index.unpack("2/6a8"), "sl") < Usage(
        Index.unpack("2/W167c4"), "sl"
    )

    assert Usage(Index.unpack("1/8b5-6"), "sl") > Usage(Index.unpack("1/5a5"), "sl")
    assert Usage(Index.unpack("1/5a5"), "sl") < Usage(Index.unpack("3/11b2-3"), "sl")
    assert Usage(Index.unpack("3/11b2-3"), "sl") > Usage(
        Index.unpack("1/W168a14-15"), "sl"
    )

    assert Usage(Index.unpack("1/8a13"), "sl") > Usage(Index.unpack("1/5d9(2)"), "sl")


def test_sort_usage():
    ss1 = SortedSet(
        [
            Usage(Index.unpack("2/6a8"), "sl"),
            Usage(Index.unpack("2/W167c4"), "sl"),
            Usage(Index.unpack("1/W167c4"), "sl"),
            Usage(Index.unpack("1/6a8"), "sl"),
        ]
    )
    assert ss1 == SortedSet(
        [
            Usage(Index.unpack("1/6a8"), "sl"),
            Usage(Index.unpack("1/W167c4"), "sl"),
            Usage(Index.unpack("2/W167c4"), "sl"),
            Usage(Index.unpack("2/6a8"), "sl"),
        ]
    )

    ss2 = SortedSet(
        [
            Usage(
                idx=Index(
                    ch=1,
                    alt=True,
                    page=168,
                    col="a",
                    row=25,
                    word="μονογενοῦς",
                ),
                lang="gr",
                var="G",
                trans_alt=Alternative(
                    "\ue201д\ue205но\ue20dѧдъ", {"H": "\ue201д\ue205нородъ"}
                ),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=False,
                    page=5,
                    col="a",
                    row=4,
                    word="μονογενὴς",
                ),
                lang="gr",
                trans_alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=False,
                    page=4,
                    col="c",
                    row=15,
                    word="μονογενοῦς",
                ),
                lang="gr",
                trans_alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=True,
                    page=168,
                    col="a",
                    row=25,
                    word="μονογενοῦς",
                ),
                lang="gr",
                var="H",
                trans_alt=Alternative(
                    "\ue201д\ue205но\ue20dѧдъ", {"G": "\ue205но\ue20dѧдъ"}
                ),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=True,
                    page=168,
                    col="a",
                    row=28,
                    word="μονογενοῦς",
                ),
                lang="gr",
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=True,
                    page=168,
                    col="a",
                    row=25,
                    word="μονογενοῦς",
                ),
                lang="gr",
                trans_alt=Alternative(
                    var_lemmas={
                        "H": "\ue201д\ue205нородъ",
                        "G": "\ue205но\ue20dѧдъ",
                    }
                ),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=False,
                    page=5,
                    col="a",
                    row=4,
                    word="μονογενὴς",
                ),
                lang="gr",
                var="WH",
                trans_alt=Alternative("\ue205но\ue20dѧдъ "),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=False,
                    page=4,
                    col="c",
                    row=15,
                    word="μονογενοῦς",
                ),
                lang="gr",
                var="WH",
                trans_alt=Alternative("\ue205но\ue20dѧдъ"),
            ),
        ]
    )
    assert ss2 == SortedSet(
        [
            Usage(
                idx=Index(
                    ch=1,
                    alt=False,
                    page=4,
                    col="c",
                    row=15,
                    word="μονογενοῦς",
                ),
                lang="gr",
                trans_alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=False,
                    page=4,
                    col="c",
                    row=15,
                    word="μονογενοῦς",
                ),
                lang="gr",
                var="WH",
                trans_alt=Alternative("\ue205но\ue20dѧдъ"),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=False,
                    page=5,
                    col="a",
                    row=4,
                    word="μονογενὴς",
                ),
                lang="gr",
                trans_alt=Alternative(var_lemmas={"WH": "\ue201д\ue205но\ue20dѧдъ"}),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=False,
                    page=5,
                    col="a",
                    row=4,
                    word="μονογενὴς",
                ),
                lang="gr",
                var="WH",
                trans_alt=Alternative("\ue205но\ue20dѧдъ "),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=True,
                    page=168,
                    col="a",
                    row=25,
                    word="μονογενοῦς",
                ),
                lang="gr",
                trans_alt=Alternative(
                    var_lemmas={"H": "\ue201д\ue205нородъ", "G": "\ue205но\ue20dѧдъ"}
                ),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=True,
                    page=168,
                    col="a",
                    row=28,
                    word="μονογενοῦς",
                ),
                lang="gr",
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=True,
                    page=168,
                    col="a",
                    row=25,
                    word="μονογενοῦς",
                ),
                lang="gr",
                var="G",
                trans_alt=Alternative(
                    "\ue201д\ue205но\ue20dѧдъ", {"H": "\ue201д\ue205нородъ"}
                ),
            ),
            Usage(
                idx=Index(
                    ch=1,
                    alt=True,
                    page=168,
                    col="a",
                    row=25,
                    word="μονογενοῦς",
                ),
                lang="gr",
                var="H",
                trans_alt=Alternative(
                    "\ue201д\ue205но\ue20dѧдъ", {"G": "\ue205но\ue20dѧдъ"}
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
        idx=Index(
            ch=5,
            alt=False,
            page=21,
            col="a",
            row=19,
            tcnt=2,
            word="невел\ue205\ue20d\ue205\ue201 WGH",
        ),
        lang="sl",
        var=Source("WGH"),
        orig_alt=Alternative(
            main_lemma="невел\ue205\ue20dан\ue205\ue201",
            main_word="невел\ue205\ue20dан\ue205\ue201",
            main_cnt=1,
        ),
    ) != Usage(
        idx=Index(
            ch=5,
            alt=False,
            page=21,
            col="a",
            row=19,
            tcnt=2,
            word="невел\ue205\ue20d\ue205\ue201 WGH",
        ),
        lang="sl",
        var=Source("WGH"),
        orig_alt=Alternative(
            main_lemma="невел\ue205\ue20dан\ue205\ue201",
            main_word="невел\ue205\ue20dан\ue205\ue201",
            main_cnt=2,
        ),
    )
