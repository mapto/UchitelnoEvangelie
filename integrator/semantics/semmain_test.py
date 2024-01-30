from .semmain import collect_lemma


def test_repeated_om():
    # based on 19/95d18
    group = [["om."], ["om."], [""], [""]]
    result = collect_lemma(None, group, 0)
    assert result == "om."
