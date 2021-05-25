import util

from model import Index, Word
from processor import dehyphenate, integrate_words


def test_dehyphenate():
    words = [
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
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="съкаꙁан\ue205\ue201",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="слово H ",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="•",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="+ неⷣ H",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="д\ue010і",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="↓",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="•м\ue010г• H",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="+ ѡ слепц\ue205 W неⷣ •л\ue010е• G",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="•",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="+ ѡ слепц\ue205 W неⷣ •л\ue010е• G",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="е-",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="ваньⷢ҇л\ue205е•",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="ѿ",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="лоуⷦ҇",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="⁖",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="+ неⷣ •л\ue010д• еуⷢ҇а ѿ мⷬ҇ка• \ue205мѣе пооу\ue20dен\ue205\ue201 наꙁаⷣ створено ꙁлⷮоустомь• вь неⷣ •в\ue010і• ѿ маⷴ по всѣхь с\ue010тыⷯ⁘",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=10),
            word="Брат\ue205\ue201",
            line_context="Брат\ue205\ue201 д\ue010\ue010хвь-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=10),
            word="д\ue010\ue010хвь-",
            line_context="Брат\ue205\ue201 д\ue010\ue010хвь-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=11),
            word="наꙗ•",
            line_context="наꙗ• \ue201д\ue205на-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=11),
            word="\ue201д\ue205на-",
            line_context="наꙗ• \ue201д\ue205на-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=12),
            word="ко",
            line_context="ко не облѣ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=12),
            word="не",
            line_context="ко не облѣ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=12),
            word="облѣ-",
            line_context="ко не облѣ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=13),
            word="н\ue205мъ",
            line_context="н\ue205мъ сѧ•",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=13),
            word="сѧ•",
            line_context="н\ue205мъ сѧ•",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=14),
            word="н\ue205",
            line_context="н\ue205 оунꙑ\ue205мъ•",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=14),
            word="оунꙑ\ue205мъ•",
            line_context="н\ue205 оунꙑ\ue205мъ•",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=15),
            word="молѧще",
            line_context="молѧще сѧ х\ue010оу",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=15),
            word="сѧ",
            line_context="молѧще сѧ х\ue010оу",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=15),
            word="х\ue010оу",
            line_context="молѧще сѧ х\ue010оу",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=16),
            word="б\ue010оу",
            line_context="б\ue010оу нашемоу• пр҇ⷪ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=16),
            word="",
            line_context="б\ue010оу нашемоу• пр҇ⷪ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=16),
            word="нашемоу",
            line_context="б\ue010оу нашемоу• пр҇ⷪ-",
            variant="\ue201д\ue205номоу WG",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=16),
            word="•",
            line_context="б\ue010оу нашемоу• пр҇ⷪ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=16),
            word="пр҇ⷪ-",
            line_context="б\ue010оу нашемоу• пр҇ⷪ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=17),
            word="свѣщаѭщюоу-",
            line_context="свѣщаѭщюоу-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=18),
            word="моу",
            line_context="моу омра\ue20dен\ue205ѧ•",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=18),
            word="омра\ue20dен\ue205ѧ•",
            line_context="моу омра\ue20dен\ue205ѧ•",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=19),
            word="пр\ue205шьдъшюоу-",
            line_context="пр\ue205шьдъшюоу-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=20),
            word="моу",
            line_context="моу не правьдь-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=20),
            word="не",
            line_context="моу не правьдь-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=20),
            word="",
            line_context="моу не правьдь-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=20),
            word="правьдь-",
            line_context="моу не правьдь-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=21),
            word="н\ue205кꙑ",
            line_context="н\ue205кꙑ ꙁъват\ue205",
            variant="праведньныхь G",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=21),
            word="",
            line_context="н\ue205кꙑ ꙁъват\ue205",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=21),
            word="",
            line_context="н\ue205кꙑ ꙁъват\ue205",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=21),
            word="ꙁъват\ue205",
            line_context="н\ue205кꙑ ꙁъват\ue205",
            variant="вьꙁва W вьꙁват\ue205 G ",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=21),
            word="",
            line_context="н\ue205кꙑ ꙁъват\ue205",
        ),
    ]

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
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="съкаꙁан\ue205\ue201",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="слово H ",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="•",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="+ неⷣ H",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="д\ue010і",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="↓",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="•м\ue010г• H",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="+ ѡ слепц\ue205 W неⷣ •л\ue010е• G",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="•",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
            variant="+ ѡ слепц\ue205 W неⷣ •л\ue010е• G",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=8),
            word="еваньⷢ҇л\ue205е•",
            line_context="съкаꙁан\ue205\ue201 •д\ue010і• е-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="ѿ",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="лоуⷦ҇",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="⁖",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
            variant="+ неⷣ •л\ue010д• еуⷢ҇а ѿ мⷬ҇ка• \ue205мѣе пооу\ue20dен\ue205\ue201 наꙁаⷣ створено ꙁлⷮоустомь• вь неⷣ •в\ue010і• ѿ маⷴ по всѣхь с\ue010тыⷯ⁘",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=9),
            word="",
            line_context="ваньⷢ҇л\ue205е• ѿ лоуⷦ҇⁖",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=10),
            word="Брат\ue205\ue201",
            line_context="Брат\ue205\ue201 д\ue010\ue010хвь-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=10),
            word="д\ue010\ue010хвьнаꙗ•",
            line_context="Брат\ue205\ue201 д\ue010\ue010хвь-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=11),
            word="\ue201д\ue205нако",
            line_context="наꙗ• \ue201д\ue205на-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=12),
            word="не",
            line_context="ко не облѣ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=12),
            word="облѣн\ue205мъ",
            line_context="ко не облѣ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=13),
            word="сѧ•",
            line_context="н\ue205мъ сѧ•",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=14),
            word="н\ue205",
            line_context="н\ue205 оунꙑ\ue205мъ•",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=14),
            word="оунꙑ\ue205мъ•",
            line_context="н\ue205 оунꙑ\ue205мъ•",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=15),
            word="молѧще",
            line_context="молѧще сѧ х\ue010оу",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=15),
            word="сѧ",
            line_context="молѧще сѧ х\ue010оу",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=15),
            word="х\ue010оу",
            line_context="молѧще сѧ х\ue010оу",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=16),
            word="б\ue010оу",
            line_context="б\ue010оу нашемоу• пр҇ⷪ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=16),
            word="",
            line_context="б\ue010оу нашемоу• пр҇ⷪ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=16),
            word="нашемоу",
            line_context="б\ue010оу нашемоу• пр҇ⷪ-",
            variant="\ue201д\ue205номоу WG",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=16),
            word="•",
            line_context="б\ue010оу нашемоу• пр҇ⷪ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=16),
            word="пр҇ⷪсвѣщаѭщюоумоу",
            line_context="б\ue010оу нашемоу• пр҇ⷪ-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=18),
            word="омра\ue20dен\ue205ѧ•",
            line_context="моу омра\ue20dен\ue205ѧ•",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=19),
            word="пр\ue205шьдъшюоумоу",
            line_context="пр\ue205шьдъшюоу-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=20),
            word="не",
            line_context="моу не правьдь-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=20),
            word="",
            line_context="моу не правьдь-",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=20),
            word="правьдьн\ue205кꙑ",
            line_context="моу не правьдь-",
            variant="праведньныхь G",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=21),
            word="",
            line_context="н\ue205кꙑ ꙁъват\ue205",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=21),
            word="",
            line_context="н\ue205кꙑ ꙁъват\ue205",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=21),
            word="ꙁъват\ue205",
            line_context="н\ue205кꙑ ꙁъват\ue205",
            variant="вьꙁва W вьꙁват\ue205 G ",
        ),
        Word(
            _index=Index(ch=43, page="197a", row=21),
            word="",
            line_context="н\ue205кꙑ ꙁъват\ue205",
        ),
    ]

    for i, w in enumerate(words):
        if i < len(words) - 1:
            w.next = words[i + 1]

    r = dehyphenate(words)

    assert len(expected) == len(r)
    assert 0 == len([v for i, v in enumerate(expected) if v != r[i]])


def test_integrate_words():
    l = [
        Word(_index=Index(ch=1, page="4b", row=10), word="ѿ", line_context="ѿ xоана⁘"),
        Word(_index=Index(ch=1, page="4b", row=10), word="x", line_context="ѿ xоана⁘"),
        Word(
            _index=Index(ch=1, page="4b", row=10), word="оана", line_context="ѿ xоана⁘"
        ),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="",
            line_context="ѿ xоана⁘",
            variant=" на вь\ue010скрсенxy1 ї\ue010с хⷭ҇а H",
        ),
        Word(_index=Index(ch=1, page="4b", row=10), word="⁘", line_context="ѿ xоана⁘"),
        Word(
            _index=Index(ch=1, page="4b", row=11),
            word="ycьсо",
            line_context="ycьсо радx xнx",
        ),
    ]
    l = util.link_tokens(l)
    l = integrate_words(l)
    r = [
        Word(_index=Index(ch=1, page="4b", row=10), word="ѿ", line_context="ѿ xоана⁘"),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="xоана⁘",
            line_context="ѿ xоана⁘",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=10),
            word="",
            line_context="ѿ xоана⁘",
            variant=" на вь\ue010скрсенxy1 ї\ue010с хⷭ҇а H",
        ),
        Word(
            _index=Index(ch=1, page="4b", row=11),
            word="ycьсо",
            line_context="ycьсо радx xнx",
        ),
    ]

    assert len(r) == len(l)
    assert 0 == len([v for i, v in enumerate(l) if v != r[i]])
