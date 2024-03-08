from sortedcontainers import SortedDict, SortedSet  # type: ignore

from config import FROM_LANG, TO_LANG
from const import STYLE_COL

from semantics import MainLangSemantics, VarLangSemantics
from aggregator import present, _expand_and_aggregate
from aggregator import reorganise_orig_special, reorganise_trans_special

# semantics change from September 2021
# with repetitions added (as if after merge)
sl_sem = MainLangSemantics(
    FROM_LANG,
    5,
    [7, 8, 9, 10],
    VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
    cnt_col=STYLE_COL + 1,
)
gr_sem = MainLangSemantics(
    TO_LANG,
    11,
    [12, 13, 14, 15],
    VarLangSemantics(TO_LANG, 16, [17, 18, 19, 20], cnt_col=STYLE_COL + 4),
    cnt_col=STYLE_COL + 3,
)


def test_present():
    sem = VarLangSemantics(lang=FROM_LANG, word=0, lemmas=[1, 2, 20, 21])
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "",
            "1/7b19",
            "вѣроують",
            "вьс\ue205 вѣроують",
            "вѣроват\ue205",
        ]
        + ([""] * 3)
        + ["πιστεύσωσι", "πιστεύω"]
        + ([""] * 13)
        + ["hl00"]
    )
    assert present(row, sem)
    row = (
        ["\ue205моуть GH", "ѩт\ue205"]
        + ([""] * 2)
        + ["1/7b19"]
        + ([""] * 20)
        + ["hl00"]
    )
    assert present(row, sem)
    row = ["\ue205моуть GH"] + ([""] * 3) + ["1/7b19"] + ([""] * 20) + ["hl00"]
    assert not present(row, sem)

    sem = VarLangSemantics(lang=TO_LANG, word=16, lemmas=[17, 18, 19])
    row = (
        [
            "вѣроу GH",
            "вѣра",
            "вѣрѫ ѩт\ue205",
            "",
            "1/7b19",
            "вѣроують",
            "вьс\ue205 вѣроують",
            "вѣроват\ue205",
        ]
        + ([""] * 3)
        + [
            "πιστεύσωσι",
            "πιστεύω",
        ]
        + ([""] * 13)
        + ["hl00"]
    )
    assert not present(row, sem)
    row = (
        ["\ue205моуть GH", "ѩт\ue205"]
        + ([""] * 2)
        + ["1/7b19"]
        + ([""] * 20)
        + ["hl00"]
    )
    assert not present(row, sem)

    row = (
        ([""] * 4)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με C", "ἐγώ"]
        + ([""] * 9)
    )
    sl_sem = MainLangSemantics(
        FROM_LANG, 5, [7, 8, 9, 10], VarLangSemantics(FROM_LANG, 0, [1, 2, 3])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 11, [12, 13, 14], VarLangSemantics(TO_LANG, 16, [17, 18, 19])
    )
    assert not present(row, sl_sem.var)
    assert present(row, sl_sem)
    assert not present(row, gr_sem)
    assert present(row, gr_sem.var)


def test_expand_and_aggregate():
    row = [""] * STYLE_COL
    dummy_sem = VarLangSemantics(lang="sl_var", word=0, lemmas=[1, 2, 19, 20])
    d = SortedDict()

    d = _expand_and_aggregate(row, None, dummy_sem, d)
    assert len(d) == 0

    d = _expand_and_aggregate(row, dummy_sem, None, d)
    assert len(d) == 0


def test_reorganise_special():
    row = (
        [""] * 4
        + ["05/17b12", "грѣхъм\ue205", "оубо ꙗко грѣ-", "грѣхъ", "#"]
        + [""] * 2
        + ["υἱός"] * 2
        + [""] * 14
        + ["1"] * 4
    )
    row = reorganise_orig_special(row, sl_sem, gr_sem)
    assert row == (
        [""] * 4
        + ["05/17b12", "грѣхъм\ue205", "оубо ꙗко грѣ-", "грѣхъ"]
        + [""] * 3
        + ["υἱός", "# υἱός"]
        + [""] * 14
        + ["1"] * 4
    )


def test_reorganise_special_var():
    row = (
        [
            "проꙁрѣвшоѡмоу G  проꙁрѣвшоумоу H",
            "проꙁьрѣт\ue205",
            "#",
            "",
            "06/38b11",
            "\ue205сцѣленоумоу",
            "сповѣдат\ue205• нъ \ue205-",
            "\ue205цѣл\ue205т\ue205",
        ]
        + [""] * 3
        + ["τεθαραπευμένον", "θεραπεύω"]
        + [""] * 14
    )
    row = reorganise_orig_special(row, sl_sem.var, gr_sem)
    assert (
        row
        == ["проꙁрѣвшоѡмоу G  проꙁрѣвшоумоу H", "проꙁьрѣт\ue205"]
        + [""] * 2
        + [
            "06/38b11",
            "\ue205сцѣленоумоу",
            "сповѣдат\ue205• нъ \ue205-",
            "\ue205цѣл\ue205т\ue205",
        ]
        + [""] * 3
        + ["τεθαραπευμένον", "# θεραπεύω"]
        + [""] * 14
    )


def test_reorganise_special_var_vyara():
    row = (
        [
            "вѣрою хвальна G",
            "вѣра хвальнъ G",
            "вѣра хвальна G",
            "# G",
            "34/156c21-d01",
            "вѣра … вельꙗ",
            "твор\ue205• \ue205 вѣ-",
            "вѣра",
            "вѣра вел\ue205ꙗ",
            "#",
            "",
            "ἐγκώμιον μέγα",
            "ἐγκώμιον & μέγας",
            "ἐγκώμιον μέγα",
        ]
        + [""] * 12
        + ["hl05:FFFCE4D6|hl11:FFFCE4D6"]
        + ["1"] * 4
    )
    row = reorganise_orig_special(row, sl_sem.var, gr_sem)
    assert (
        row
        == [
            "вѣрою хвальна G",
            "вѣра хвальнъ G",
            "вѣра хвальна G",
            "",
            "34/156c21-d01",
            "вѣра … вельꙗ",
            "твор\ue205• \ue205 вѣ-",
            "вѣра",
            "вѣра вел\ue205ꙗ",
            "#",
            "",
            "ἐγκώμιον μέγα",
            "ἐγκώμιον & μέγας",
            "# ἐγκώμιον μέγα",
        ]
        + [""] * 12
        + ["hl05:FFFCE4D6|hl11:FFFCE4D6"]
        + ["1"] * 4
    )


def test_reorganise_special_var_vyara_trans():
    row = (
        [
            "вѣрою хвальна G",
            "вѣра & хвальнъ G",
            "вѣра хвальна G",
            "# G",
            "34/156c21-d01",
            "вѣра … вельꙗ",
            "твор\ue205• \ue205 вѣ-",
            "вѣра & вел\ue205\ue205",
            "вѣра вел\ue205ꙗ",
            "#",
            "",
            "ἐγκώμιον μέγα",
            "ἐγκώμιον",
            "ἐγκώμιον μέγα",
        ]
        + [""] * 12
        + ["hl05:FFFCE4D6|hl11:FFFCE4D6"]
        + ["1"] * 4
    )

    row = reorganise_trans_special(row, sl_sem)
    assert (
        row
        == [
            "вѣрою хвальна G",
            "вѣра & хвальнъ G",
            "вѣра хвальна G",
            "# G",
            "34/156c21-d01",
            "вѣра … вельꙗ",
            "твор\ue205• \ue205 вѣ-",
            "вѣра & вел\ue205\ue205",
            "# вѣра вел\ue205ꙗ",
            "",
            "",
            "ἐγκώμιον μέγα",
            "ἐγκώμιον",
            "ἐγκώμιον μέγα",
        ]
        + [""] * 12
        + ["hl05:FFFCE4D6|hl11:FFFCE4D6"]
        + ["1"] * 4
    )


def test_reorganise_special_var_vyara_trans_var():
    row = (
        [
            "вѣрою хвальна G",
            "вѣра & хвальнъ G",
            "вѣра хвальна G",
            "# G",
            "34/156c21-d01",
            "вѣра … вельꙗ",
            "твор\ue205• \ue205 вѣ-",
            "вѣра & вел\ue205\ue205",
            "вѣра вел\ue205ꙗ",
            "#",
            "",
            "ἐγκώμιον μέγα",
            "ἐγκώμιον",
            "ἐγκώμιον μέγα",
        ]
        + [""] * 12
        + ["hl05:FFFCE4D6|hl11:FFFCE4D6"]
        + ["1"] * 4
    )

    row = reorganise_trans_special(row, sl_sem.var)
    assert (
        row
        == [
            "вѣрою хвальна G",
            "вѣра & хвальнъ G",
            "# вѣра хвальна G",
            "",
            "34/156c21-d01",
            "вѣра … вельꙗ",
            "твор\ue205• \ue205 вѣ-",
            "вѣра & вел\ue205\ue205",
            "вѣра вел\ue205ꙗ",
            "#",
            "",
            "ἐγκώμιον μέγα",
            "ἐγκώμιον",
            "ἐγκώμιον μέγα",
        ]
        + [""] * 12
        + ["hl05:FFFCE4D6|hl11:FFFCE4D6"]
        + ["1"] * 4
    )


def test_reorganise_var_special_prichatnik():
    row = (
        [
            "боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 G пр\ue205\ue20dестн\ue205ц\ue205 H",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "≈ GH",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "≈",
            "",
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05:FFFCD5B4|hl00:FFFCD5B4|hl11:FFFCD5B4"]
        + ["1"] * 4
    )
    result = reorganise_trans_special(row, sl_sem.var)
    assert (
        result
        == [
            "боудемь W пр\ue205\ue20dестьн\ue205ц\ue205 G пр\ue205\ue20dестн\ue205ц\ue205 H",
            "пр\ue205\ue20dѧстьн\ue205къ GH",
            "≈ пр\ue205\ue20dѧстьн\ue205къ бꙑт\ue205 GH",
            "",
            "05/028c21-d01",
            "пр\ue205\ue20dьтьн\ue205ц\ue205 боудоуть",
            "да пр\ue205\ue20dьтьн\ue205ц\ue205",
            "пр\ue205\ue20dьтьн\ue205къ",
            "пр\ue205\ue20dьтьн\ue205къ бꙑт\ue205",
            "≈",
            "",
            "ποιῆσαι κοινωνοὺς",
            "ποιέω & κοινωνός",
            "ποιέω κοινωνόν",
        ]
        + [""] * 12
        + ["hl05:FFFCD5B4|hl00:FFFCD5B4|hl11:FFFCD5B4"]
        + ["1"] * 4
    )


# TODO: Test for sl_sem.var
