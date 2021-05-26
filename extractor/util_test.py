from model import Index, Word, WordList
from util import Buffer


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
