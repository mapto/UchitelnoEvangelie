sl = "а б в г д е ж ꙃ(ꙅ,ѕ) ꙁ (і,и) к л м н о п р с т оу(ѹ,ꙋ) ф х ш ц  щ ъ ꙑ(ы) ь ѣ ю ꙗ  ѧ ѫ ѩ ѭ ѯ ѱ ѳ у(ѵ)".split()
sl2 = "а б в г д е ж ꙃ ꙁ  к л м н о п р с т ѹ ф х ш ц  щ ъ ꙑ ь ѣ ю ꙗ  ѧ ѫ ѩ ѭ ѯ ѱ ѳ у".split()
gr = "α β γ δ ε ζ η θ(ϑ) ι κ(ϰ) λ μ ν ξ ο π ρ σ τ υ ϕ(φ) χ ψ ω".split()


def _ord(a: str) -> float:
    """
    >>> _ord("а")
    1072
    >>> _ord("ж")
    1078
    >>> _ord("к")
    1082

    >>> _ord("ꙃ")
    1078.5
    
    >>> _ord("ꙅ")
    1078.5
    
    >>> _ord("ѕ")
    1078.5
    
    >>> _ord("ꙁ")
    1079
    >>> _ord("и")
    1080
    >>> _ord("і")
    1080
    >>> _ord("")
    1080
    >>> _ord("т")
    1090
    >>> _ord("ѹ")
    1090.5
    >>> _ord("ꙋ")
    1090.5
    >>> _ord("ш")
    1093.5
    >>> _ord("ц")
    1094
    >>> _ord("")
    1094.5
    >>> _ord("ъ")
    1098
    >>> _ord("ꙑ")
    1099
    >>> _ord("ы")
    1099
    >>> _ord("ь")
    1100
    >>> _ord("ѣ")
    1100.5
    >>> _ord("ю")
    1102
    >>> _ord("ꙗ")
    1102.5
    >>> _ord("")
    1102.7
    >>> _ord("ѧ")
    1127
    >>> _ord("ѫ")
    1131
    >>> _ord("ѩ")
    1131.5
    >>> _ord("ѭ")
    1133
    >>> _ord("ѯ")
    1135
    >>> _ord("ѱ")
    1137
    >>> _ord("ѳ")
    1139
    >>> _ord("у")
    1141
    >>> _ord("ѵ")
    1141
    """
    assert len(a) == 1

    if a == "ꙃ" or a == "ꙅ" or a == "ѕ":
        return ord("ж") + 0.5
    if a == "ꙁ":
        return ord("ж") + 1
    if a == "" or a == "і":
        return ord("и")
    if a == "ꙋ" or a == "ѹ":
        return ord("т") + 0.5
    if a == "ш":
        return ord("х") + 0.5
    if a == "":
        return ord("ц") + 0.5
    if a == "ꙑ":
        return ord("ы")
    if a == "ѣ":
        return ord("ь") + 0.5
    if a == "ꙗ":
        return ord("ю") + 0.5
    if a == "":
        return ord("ю") + 0.7
    if a == "ѩ":
        return ord("ѫ") + 0.5
    if a == "у":
        return ord("ѵ")

    if a == "ϕ":
        return ord("υ") + 0.5
    if a == "ϑ":
        return ord("η") + 0.5
    if a == "ϰ":
        return ord("ι") + 0.5

    return ord(a)


def cmp(a: str, b: str) -> float:
    """
    >>> cmp("а", "б")
    -1

    >>> cmp("", "к")
    -1

    >>> cmp("ꙁ", "")
    -1

    >>> sl = "а б в г д е ж ꙃ ꙁ  к л м н о п р с т ѹ ф х ш ц  щ ъ ꙑ ь ѣ ю ꙗ  ѧ ѫ ѩ ѭ ѯ ѱ ѳ у"
    >>> sl2 = sl.split()
    >>> sl2.sort(key=_ord)
    >>> sl == " ".join(sl2)
    True

    >>> sl = "а б в г д е ж ꙅ ꙁ і к л м н о п р с т ꙋ ф х ш ц  щ ъ ы ь ѣ ю ꙗ  ѧ ѫ ѩ ѭ ѯ ѱ ѳ ѵ"
    >>> sl2 = sl.split()
    >>> sl2.sort(key=_ord)
    >>> sl == " ".join(sl2)
    True

    >>> sl = "а б в г д е ж ѕ ꙁ и к л м н о п р с т ѹ ф х ш ц  щ ъ ꙑ ь ѣ ю ꙗ  ѧ ѫ ѩ ѭ ѯ ѱ ѳ ѵ"
    >>> sl2 = sl.split()
    >>> sl2.sort(key=_ord)
    >>> sl == " ".join(sl2)
    True

    >>> sl = "α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ ϕ χ ψ ω"
    >>> sl2 = sl.split()
    >>> sl2.sort(key=_ord)
    >>> sl == " ".join(sl2)
    True

    >>> sl = "α β γ δ ε ζ η ϑ ι ϰ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω"
    >>> sl2 = sl.split()
    >>> sl2.sort(key=_ord)
    >>> sl == " ".join(sl2)
    True
    """
    assert len(a) == len(b) == 1

    return 0 if _ord(a) - _ord(b) == 0 else 1 if _ord(a) - _ord(b) > 0 else -1
    # return _ord(a) - _ord(b)
