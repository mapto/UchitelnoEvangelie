from sortedcontainers import SortedSet  # type: ignore
from model import Index, Usage, Alternative


def test_index_unpack():
    assert Index.unpack("1/W167c4").longstr() == "01/W167c04"
    assert str(Index.unpack("1/6c4")) == "1/6c4"
    assert str(Index.unpack("1/6c4\u2082")) == "1/6c4₂"

    """
    >> str(Index.unpack("1/6c4var"))
    '1/6c4var'
    >> str(Index.unpack("1/6c4-8var"))
    '1/6c4-8var'
    >> str(Index.unpack("1/6c4var-2/6d4var"))
    '1/6c4var-2/6d4var'
    """

    assert str(Index.unpack("1/6c4-8")) == "1/6c4-8"
    assert str(Index.unpack("1/6c4-d4")) == "1/6c4-d4"
    assert str(Index.unpack("1/6c4-6d4")) == "1/6c4-d4"
    assert str(Index.unpack("1/6c4-7d4")) == "1/6c4-7d4"
    assert str(Index.unpack("1/6c4-2/6d4")) == "1/6c4-2/6d4"


def test_index_order():
    assert Index.unpack("1/6a8") < Index.unpack("1/6a17")
    assert Index.unpack("1/6a8") < Index.unpack("1/W167c4")
    assert not Index.unpack("2/6a8") < Index.unpack("2/W167c4")

    assert Index.unpack("1/8b5-6") > Index.unpack("1/5a5")
    assert Index.unpack("1/5a5") < Index.unpack("3/11b2-3")
    assert Index.unpack("3/11b2-3") > Index.unpack("1/W168a14-15")

    assert Index.unpack("1/8a13") > Index.unpack("1/5d9(2)")


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
