from model import Index, Word
from util import Buffer, link_tokens, WordList


def test_link_tokens():
    assert 0 == len(link_tokens([]))

    t = [Word(Index(0, "", 0))]
    t = link_tokens(t)
    assert len(t) == 1 and t[0].prev == t[0].next == None

    t = [Word(Index(0, "", 0)), Word(Index(0, "", 0))]
    t = link_tokens(t)
    assert (
        len(t) == 2
        and t[0].prev == None
        and t[0].next == t[1]
        and t[1].prev == t[0]
        and t[1].next == None
    )

    t = [Word(Index(0, "", 0)), Word(Index(0, "", 0)), Word(Index(0, "", 0))]
    t = link_tokens(t)
    assert (
        len(t) == 3
        and t[0].next == t[1]
        and t[1].prev == t[0]
        and t[1].next == t[2]
        and t[2].prev == t[1]
    )

    l = [
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="ѿ",
            line_context="ѿ \ue205оана⁘",
            variant="",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="\ue205",
            line_context="ѿ \ue205оана⁘",
            variant="",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="оана",
            line_context="ѿ \ue205оана⁘",
            variant="",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="",
            line_context="ѿ \ue205оана⁘",
            variant=" на вь\ue010скрсен\ue205\ue201 ї\ue010с хⷭ҇а H",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="⁘",
            line_context="ѿ \ue205оана⁘",
            variant="",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=11),
            word="\ue20cьсо",
            line_context="\ue20cьсо рад\ue205 \ue205н\ue205",
            variant="",
        ),
    ]
    l = link_tokens(l)
    r = [
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="ѿ",
            line_context="ѿ \ue205оана⁘",
            variant="",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="\ue205",
            line_context="ѿ \ue205оана⁘",
            variant="",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="оана",
            line_context="ѿ \ue205оана⁘",
            variant="",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="",
            line_context="ѿ \ue205оана⁘",
            variant=" на вь\ue010скрсен\ue205\ue201 ї\ue010с хⷭ҇а H",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="⁘",
            line_context="ѿ \ue205оана⁘",
            variant="",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=11),
            word="\ue20cьсо",
            line_context="\ue20cьсо рад\ue205 \ue205н\ue205",
            variant="",
        ),
    ]
    assert 0 == len([v for i, v in enumerate(l) if v != r[i]])


def test_WordList():
    result = WordList()
    words = ["a", "b", "c"]
    idx = Index(ch=1, page="1a", row=1)
    for w in words:
        result += Word(idx, w, words)
    assert len(words) == len(result)

    r2 = WordList()
    r2 += Word(idx, "f", "context")
    w2 = ["d", "e"]
    idx = Index(ch=1, page="1a", row=2)
    for w in w2:
        r2 += Word(idx, w, w2)
    assert len(w2) + 1 == len(r2)

    r2 = WordList()
    w2 = ["g", "h"]
    idx = Index(ch=1, page="1a", row=3)
    for w in w2:
        r2 += Word(idx, w, w2)
    assert len(w2) == len(r2)


def test_compile_words():
    idx = Index(ch=43, page="197a", row=7)
    b = Buffer("СДОⷬ҇• ПЛⷭ҇")
    r = b.compile_words(idx, "")

    expected = [
        Word(
            _index=Index(ch=43, page="197a", row=7),
            word="\ue204С\ue204ДОⷬ҇•",
            line_context="\ue204С\ue204ДОⷬ҇• П\ue204Л\ue216ⷭ҇",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=7),
            word="П\ue204Л\ue216ⷭ҇",
            line_context="\ue204С\ue204ДОⷬ҇• П\ue204Л\ue216ⷭ҇",
        ),
    ]

    assert len(r) == len(expected)
    assert 0 == len([n for i, n in enumerate(r) if n != expected[i]])

    idx = Index(ch=43, page="197a", row=8)
    b = Buffer("съкаꙁан •ді• е-ваньⷢ҇ле• ѿ лоуⷦ҇⁖")
    r = b.compile_words(idx, "")

    expected = [
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="съкаꙁан\ue205\ue201",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="•д\ue010і•",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="е-ваньⷢ҇л\ue205е•",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="ѿ",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="лоуⷦ҇⁖",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="",
        ),
    ]

    assert len(r) == len(expected)
    assert 0 == len([n for i, n in enumerate(r) if n != expected[i]])


def test_compile_buffer():
    idx = Index(ch=43, page="197a", row=8)
    b = Buffer("съкаꙁан •ді• е-ваньⷢ҇ле• ѿ лоуⷦ҇⁖")
    r = b.compile_buffer(idx, {})

    expected = [
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="съкаꙁан\ue205\ue201",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="•д\ue010і•",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="е-ваньⷢ҇л\ue205е•",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="ѿ",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="лоуⷦ҇⁖",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="",
        ),
    ]

    assert len(r) == len(expected)
    assert 0 == len([n for i, n in enumerate(r) if n != expected[i]])
