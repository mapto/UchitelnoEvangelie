#!/usr/bin/env python3

from typing import List, Tuple, Dict

import re

from model import Comment


def transform_clean(
    lines_index: Dict[str, Tuple[str, List[str]]]
) -> List[Tuple[str, str, List[str]]]:
    """Transforms Dict to List and merges hyphened words into their first line.
    Returns line_num, line, comment_indices"""
    transformed = []
    prevline = ""
    pli = ""
    for nli in lines_index.keys():
        nextline = lines_index[nli][0]
        if prevline:
            if prevline[-1] == "-":
                prevwords = re.split(r"\s", prevline)
                nextwords = re.split(r"\s", nextline)
                assert len(nextwords) > 0
                assert len(prevwords) > 0
                prevwords[-1] = prevwords[-1][:-1] + nextwords[0]
                prevline = " ".join(prevwords)
                nextline = " ".join(nextwords[1:])
                lines_index[pli] = (prevline, lines_index[pli][1])
                lines_index[nli] = (nextline, lines_index[nli][1])
            transformed.append((pli, prevline, lines_index[pli][1]))
        prevline = nextline
        pli = nli

    transformed.append((pli, prevline, lines_index[pli][1]))

    return transformed


def split_rows(
    book_index: List[Tuple[str, str, List[str]]], comments: Dict[int, Comment]
) -> List[Tuple[str, str, str, str]]:
    """Returns line_num, word, line, comment

    >>> split_rows([], {})
    []

    01-slovo1-4b
    >> comments = {0: Comment(0, 'оана', addition=' на вь\ue010скрсен\ue205\ue201 ї\ue010с хⷭ҇а H'), \
        1: Comment(1, 'семоу', annotation='семь WGH'), 2: Comment(2, 'рекъ• \ue205', annotation='рекы WGH')}
    >> transformed = [('1/4b6', 'С\ue010ТГО \ue204ОАНА', []), ('1/4b7', 'Ꙁлатооустааго•', []), ('1/4b8', 'съкаꙁан\ue205\ue201 с\ue010тааго', []), ('1/4b9', 'евангел\ue205ꙗ⁘', []), ('1/4b10', 'ѿ \ue205оана⁘', ["0-0"]), ('1/4b11', '\ue20cьсо рад\ue205 \ue205н\ue205', []), ('1/4b12', 'евангел\ue205ст\ue205•', []), ('1/4b13', 'отъ съмотрен\ue205ꙗ', []), ('1/4b14', 'на\ue20dаша• \ue205', []), ('1/4b15', 'се въ малѣ• по', []), ('1/4b16', 'семоу на\ue20dатъ', ["1-0"]), ('1/4b17', 'рекъ• \ue205 слово плъть', ["2-0"]), ('1/4b18', 'бꙑсть• а дроугое', []), ('1/4b19', 'вьсе м\ue205моте\ue20dе•', []), ('1/4b20', 'ꙁа\ue20dѧт\ue205\ue201•', []), ('1/4b21', 'рожьство въсп\ue205тѣн\ue205е', []), ('1/4b22', 'въꙁдращен\ue205е⁘', []), ('1/4b23', '', [])]
    >> split_rows(transformed, comments)
    [('1/4b6', 'С\ue010ТГО', 'С\ue010ТГО \ue204ОАНА', ''), ('1/4b6', '\ue204ОАНА', 'С\ue010ТГО \ue204ОАНА', ''), ('1/4b7', 'Ꙁлатооустааго•', 'Ꙁлатооустааго•', ''), ('1/4b8', 'съкаꙁан\ue205\ue201', 'съкаꙁан\ue205\ue201 с\ue010тааго', ''), ('1/4b8', 'с\ue010тааго', 'съкаꙁан\ue205\ue201 с\ue010тааго', ''), ('1/4b9', 'евангел\ue205ꙗ⁘', 'евангел\ue205ꙗ⁘', ''), ('1/4b10', 'ѿ', 'ѿ \ue205оана⁘', ''), ('1/4b10', '\ue205оана⁘', 'ѿ \ue205оана⁘', ''), ('1/4b10', '', 'ѿ \ue205оана⁘', ' на вь\ue010скрсен\ue205\ue201 ї\ue010с хⷭ҇а H'), ('1/4b11', '\ue20cьсо', '\ue20cьсо рад\ue205 \ue205н\ue205', ''), ('1/4b11', 'рад\ue205', '\ue20cьсо рад\ue205 \ue205н\ue205', ''), ('1/4b11', '\ue205н\ue205', '\ue20cьсо рад\ue205 \ue205н\ue205', ''), ('1/4b12', 'евангел\ue205ст\ue205•', 'евангел\ue205ст\ue205•', ''), ('1/4b13', 'отъ', 'отъ съмотрен\ue205ꙗ', ''), ('1/4b13', 'съмотрен\ue205ꙗ', 'отъ съмотрен\ue205ꙗ', ''), ('1/4b14', 'на\ue20dаша•', 'на\ue20dаша• \ue205', ''), ('1/4b14', '\ue205', 'на\ue20dаша• \ue205', ''), ('1/4b15', 'се', 'се въ малѣ• по', ''), ('1/4b15', 'въ', 'се въ малѣ• по', ''), ('1/4b15', 'малѣ•', 'се въ малѣ• по', ''), ('1/4b15', 'по', 'се въ малѣ• по', ''), ('1/4b16', 'семоу', 'семоу на\ue20dатъ', 'семь WGH'), ('1/4b16', 'на\ue20dатъ', 'семоу на\ue20dатъ', ''), ('1/4b17', 'рекъ•', 'рекъ• \ue205 слово плъть', ''), ('1/4b17', '\ue205', 'рекъ• \ue205 слово плъть', 'рекы WGH'), ('1/4b17', 'слово', 'рекъ• \ue205 слово плъть', ''), ('1/4b17', 'плъть', 'рекъ• \ue205 слово плъть', ''), ('1/4b18', 'бꙑсть•', 'бꙑсть• а дроугое', ''), ('1/4b18', 'а', 'бꙑсть• а дроугое', ''), ('1/4b18', 'дроугое', 'бꙑсть• а дроугое', ''), ('1/4b19', 'вьсе', 'вьсе м\ue205моте\ue20dе•', ''), ('1/4b19', 'м\ue205моте\ue20dе•', 'вьсе м\ue205моте\ue20dе•', ''), ('1/4b20', 'ꙁа\ue20dѧт\ue205\ue201•', 'ꙁа\ue20dѧт\ue205\ue201•', ''), ('1/4b21', 'рожьство', 'рожьство въсп\ue205тѣн\ue205е', ''), ('1/4b21', 'въсп\ue205тѣн\ue205е', 'рожьство въсп\ue205тѣн\ue205е', ''), ('1/4b22', 'въꙁдращен\ue205е⁘', 'въꙁдращен\ue205е⁘', ''), ('1/4b23', '', '', '')]

    01-slovo1-5c
    >> comments = {0: ('ван\ue205ꙗ', 'жестован\ue205ꙗ WGH'), 1: ('тѣ', 'то WG')}
    >> transformed = [('1/5c1', 'мъ с\ue205мь се бѣ', []), ('1/5c2', '\ue205спрьва оу б\ue010а•', []), ('1/5c3', 'с\ue205рѣ\ue20dь не мьн\ue205', []), ('1/5c4', 'ре\ue20dе \ue201стьствован\ue205ꙗ', []), ('1/5c5', 'о\ue20d\ue010а старѣ\ue205ша', [0]), ('1/5c6', 'соуща не', []), ('1/5c7', 'бѣ бо н\ue205кол\ue205же', []), ('1/5c8', 'о\ue010ць бе-с\ue010на аще л\ue205', []), ('1/5c9', 'кто г\ue010лть• тѣ', [1]), ('1/5c10', 'како \ue201сть с\ue010нъ', []), ('1/5c11', 'не съ̏ юнѣ\ue205 о\ue010ца', []), ('1/5c12', '\ue201же бо отъ кого', []), ('1/5c13', '\ue201сть ноужда', []), ('1/5c14', '\ue201сть послѣжде', []), ('1/5c15', 'бꙑт\ue205 отъ н\ue201гоже', []), ('1/5c16', 'боудеть•', []), ('1/5c17', 'се ре\ue20dемъ оубо с\ue205ꙗн\ue205\ue201', []), ('1/5c18', 'слънь\ue20dьно•', []), ('1/5c19', 'ѿ самого естьства', []), ('1/5c20', 'сл\ue010нь\ue20dьнаго', []), ('1/5c21', '\ue205сходѧ• еда послѣ-', [])]
    >> split_rows(transformed, comments)
    [('1/5c5', 'о\ue20d\ue010а', 'о\ue20d\ue010а старѣ\ue205ша', ''), ('1/5c5', 'старѣ\ue205ша', 'о\ue20d\ue010а старѣ\ue205ша', ''), ('1/5c5', '', 'о\ue20d\ue010а старѣ\ue205ша', 'жестован\ue205ꙗ WGH'), ('1/5c9', 'кто', 'кто г\ue010лть• тѣ', ''), ('1/5c9', 'г\ue010лть•', 'кто г\ue010лть• тѣ', ''), ('1/5c9', 'тѣ', 'кто г\ue010лть• тѣ', 'то WG')]
    """
    # TODO: allow for multiple comments for a word
    word_index = []
    # list in order to handle multiple comments in line
    for line in book_index:
        (row_num, row_text, row_comments) = line
        to_find = list(row_comments)
        for word in re.split(r"\s", row_text):
            if row_comments:
                for cref in row_comments:
                    parts = cref.split("-")
                    assert len(parts) == 2
                    crid = int(parts[0])
                    crline = int(parts[1])
                    comment = comments[crid]
                    # only last word of last row of selection is relevant
                    # TODO: handle multiline comment selections
                    marked = re.split(r"\s", comments[crid].ref[crline])[-1]
                    # print(marked)
                    # print(word)
                    # print(marked in word)
                    if marked in word:
                        if cref not in to_find:
                            print(f"Found reference to already used comment: {cref}")
                            continue
                        to_find.remove(cref)
                        word_index.append((row_num, word, row_text, comment.annotation))
                        if comment.addition:
                            word_index.append((row_num, "", row_text, comment.addition))
                    else:
                        word_index.append((row_num, word, row_text, ""))
                        if len(marked) == 1 and marked in [".", "!"]:
                            to_find.remove(cref)
                            if comment.annotation:
                                print(
                                    f"Annotation present for punctuation comment {comment}"
                                )
                                word_index.append(
                                    (row_num, "", row_text, comment.annotation)
                                )
                            if comment.addition:
                                print(
                                    f"Addition present for punctuation comment {comment}"
                                )
                                word_index.append(
                                    (row_num, "", row_text, comment.addition)
                                )
            else:
                word_index.append((row_num, word, row_text, ""))

        # if no row_comments, to_find is empty
        for rc in to_find:
            r = int(rc.split("-")[0])
            print(f"Unallocated comment {comments[r]}")
            if comments[r].annotation:
                print(f"Annotation present for punctuation comment {comments[r]}")
                word_index.append((row_num, "", row_text, comments[r].annotation))
            if comments[r].addition:
                print(f"Addition present for punctuation comment {comments[r]}")
                word_index.append((row_num, "", row_text, comments[r].addition))

    return word_index
