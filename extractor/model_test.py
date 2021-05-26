from model import Index, Word, WordList


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

    r3 = WordList()
    w3 = ["g", "h"]
    idx = Index(ch=1, page="1a", row=3)
    for w in w3:
        r3 += Word(idx, w, w3)
    assert len(w3) == len(r3)

    r3 += r2
    assert len(w2) + 1 + len(w3) == len(r3)

    r3 += result
    assert len(w2) + 1 + len(w3) + len(result) == len(r3)
