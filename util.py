from typing import List
from model import Word, Index


def link_tokens(tokens: List[Word]) -> List[Word]:
    """
    >>> link_tokens([])
    []

    >>> t = [Word(Index(0,"",0))]
    >>> t = link_tokens(t)
    >>> len(t) == 1 and t[0].prev == t[0].next == None
    True

    >>> t = [Word(Index(0,"",0)), Word(Index(0,"",0))]
    >>> t = link_tokens(t)
    >>> len(t) == 2 and t[0].prev == None and t[0].next == t[1] and t[1].prev == t[0] and t[1].next == None
    True

    >>> t = [Word(Index(0,"",0)), Word(Index(0,"",0)), Word(Index(0,"",0))]
    >>> t = link_tokens(t)
    >>> len(t) == 3 and t[0].next == t[1] and t[1].prev == t[0] and t[1].next == t[2] and t[2].prev == t[1]
    True
    
    >>> l = [Word(_index=Index(ch=1, page='4b', row=10), word='ѿ', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=10), word='\ue205', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=10), word='оана', line_context='ѿ \ue205оана⁘', variant=''), \
        Word(_index=Index(ch=1, page='4b', row=10), word='', line_context='ѿ \ue205оана⁘', variant=' на вь\ue010скрсен\ue205\ue201 ї\ue010с хⷭ҇а H'),\
        Word(_index=Index(ch=1, page='4b', row=10), word='⁘', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=11), word='\ue20cьсо', line_context='\ue20cьсо рад\ue205 \ue205н\ue205', variant='')]
    >>> l = link_tokens(l)
    >>> r = [Word(_index=Index(ch=1, page='4b', row=10), word='ѿ', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=10), word='\ue205', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=10), word='оана', line_context='ѿ \ue205оана⁘', variant=''), \
        Word(_index=Index(ch=1, page='4b', row=10), word='', line_context='ѿ \ue205оана⁘', variant=' на вь\ue010скрсен\ue205\ue201 ї\ue010с хⷭ҇а H'),\
        Word(_index=Index(ch=1, page='4b', row=10), word='⁘', line_context='ѿ \ue205оана⁘', variant=''),\
        Word(_index=Index(ch=1, page='4b', row=11), word='\ue20cьсо', line_context='\ue20cьсо рад\ue205 \ue205н\ue205', variant='')]
    >>> [v for i, v in enumerate(l) if v != r[i]]
    []

    """
    if not tokens:
        return tokens
    for i in range(len(tokens)):
        if i == len(tokens) - 1:
            break
        tokens[i].next = tokens[i + 1]
        tokens[i + 1].prev = tokens[i]
    return tokens
