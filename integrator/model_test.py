from sortedcontainers import SortedSet  # type: ignore
from model import Index, Usage


def test_order_usage():
    assert Usage(Index.unpack("1/6a8"), "sl") < Usage(Index.unpack("1/6a17"), "sl")
    assert Usage(Index.unpack("1/6a8"), "sl") < Usage(Index.unpack("1/W167c4"), "sl")
    assert not Usage(Index.unpack("2/6a8"), "sl") < Usage(
        Index.unpack("2/W167c4"), "sl"
    )


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
                trans_alt="\ue201д\ue205но\ue20dѧдъ",
                trans_alt_var={"H": "\ue201д\ue205нородъ"},
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
                trans_alt_var={"WH": "\ue201д\ue205но\ue20dѧдъ"},
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
                trans_alt_var={"WH": "\ue201д\ue205но\ue20dѧдъ"},
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
                trans_alt="\ue201д\ue205но\ue20dѧдъ",
                trans_alt_var={"G": "\ue205но\ue20dѧдъ"},
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
                trans_alt_var={
                    "H": "\ue201д\ue205нородъ",
                    "G": "\ue205но\ue20dѧдъ",
                },
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
                trans_alt="\ue205но\ue20dѧдъ ",
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
                trans_alt="\ue205но\ue20dѧдъ",
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
                trans_alt_var={"WH": "\ue201д\ue205но\ue20dѧдъ"},
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
                trans_alt="\ue205но\ue20dѧдъ",
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
                trans_alt_var={"WH": "\ue201д\ue205но\ue20dѧдъ"},
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
                trans_alt="\ue205но\ue20dѧдъ ",
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
                trans_alt_var={"H": "\ue201д\ue205нородъ", "G": "\ue205но\ue20dѧдъ"},
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
                trans_alt="\ue201д\ue205но\ue20dѧдъ",
                trans_alt_var={"H": "\ue201д\ue205нородъ"},
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
                trans_alt="\ue201д\ue205но\ue20dѧдъ",
                trans_alt_var={"G": "\ue205но\ue20dѧдъ"},
            ),
        ]
    )
