from model import Source
from semantics import MainLangSemantics, VarLangSemantics

from const import STYLE_COL
from config import FROM_LANG, TO_LANG
from setup import sl_sem, gr_sem


def test_basic_1():
    # old semantics
    sl_sem = MainLangSemantics(
        FROM_LANG, 4, [6, 7, 8, 9], VarLangSemantics(FROM_LANG, 0, [1, 2])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 10, [11, 12, 13], VarLangSemantics(TO_LANG, 15, [16, 17])
    )

    row = (
        ["ю G", "\ue205 pron.", "", "1/W168b6", "om.", "", "om."]
        + [""] * 3
        + ["ταύτην", "οὗτος"]
        + [""] * 12
    )
    result = sl_sem.var.multilemma(row)
    assert result == {"G": "\ue205 pron."}


def test_basic_2():
    # old semantics
    sl_sem = MainLangSemantics(
        FROM_LANG, 4, [6, 7, 8, 9], VarLangSemantics(FROM_LANG, 0, [1, 2])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 10, [11, 12, 13], VarLangSemantics(TO_LANG, 15, [16, 17])
    )

    row = (
        ["вь WGH", "въ", "въ + Loc.", "1/7d1", "оу", "оу насъ", "ѹ"]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["παρ’ Cs", "παρά ", "παρά + Acc."]
        + [""] * 6
    )
    result = sl_sem.var.multilemma(row)
    assert result == {Source("WGH"): "въ"}
    result = gr_sem.var.multilemma(row)
    assert result == {"Cs": "παρά"}


def test_basic_3():
    # old semantics
    sl_sem = MainLangSemantics(
        FROM_LANG, 4, [6, 7, 8, 9], VarLangSemantics(FROM_LANG, 0, [1, 2])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 10, [11, 12, 13], VarLangSemantics(TO_LANG, 15, [16, 17])
    )

    row = (
        ([""] * 3)
        + ["1/W168c7", "мене", "мене соуща послѣд\ue205 створ\ue205", "аꙁъ"]
        + ([""] * 3)
        + ["μὲν"]
        + ([""] * 4)
        + ["με Cs", "ἐγώ"]
        + ([""] * 7)
    )
    result = sl_sem.multilemma(row)
    assert result == {"": "аꙁъ"}
    result = gr_sem.var.multilemma(row)
    assert result == {"Cs": "ἐγώ"}

    dummy_sem = MainLangSemantics(
        FROM_LANG, 2, [3], VarLangSemantics(FROM_LANG, 0, [1])
    )

    result = dummy_sem.var.multilemma(
        ["ноедаго G  днородоу H", "днородъ H & ноѧдъ G", "", ""]
    )
    assert len(result) == 2
    assert result["H"] == "\ue201д\ue205нородъ"
    assert result["G"] == "\ue205но\ue20dѧдъ"

    result = dummy_sem.var.multilemma(["", "", "", ""])
    assert len(result) == 0

    result = dummy_sem.var.multilemma(
        [
            "дноеды WH Ø G",
            "дноѧдъ",
            "\ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ",
        ]
    )
    assert result == {Source("WH"): "дноѧдъ"}

    dummy_sem2 = VarLangSemantics(TO_LANG, 0, [1])
    result = dummy_sem2.multilemma(["με Cs", "ἐγώ"])
    assert result == {"Cs": "ἐγώ"}


def test_std_sem():
    row = (
        ["\ue201д\ue205но\ue20dеды WH Ø G", "\ue201д\ue205но\ue20dѧдъ"]
        + [""] * 2
        + [
            "1/5a4",
            "\ue205но\ue20dадꙑ\ue205",
            "нъ ꙗко б\ue010ъ• а \ue205но\ue20dадꙑ\ue205",
            "\ue205но\ue20dѧдъ",
        ]
        + [""] * 3
        + ["μονογενὴς", "μονογενής"]
        + [""] * 14
    )
    result = sl_sem.var.multilemma(row)
    assert result == {Source("WH"): "\ue201д\ue205но\ue20dѧдъ"}

    row = (
        [
            "\ue201д\ue205нородоу H",
            "\ue201д\ue205нородъ",
        ]
        + [""] * 2
        + [
            "1/W168a34",
            "\ue201д\ue205но\ue20dедоу",
            "бѣ \ue205мѣт\ue205 \ue201д\ue205но\ue20dедоу",
            "\ue201д\ue205но\ue20dѧдъ ",
        ]
        + [""] * 3
        + ["μονογενῆ", "μονογενής"]
        + [""] * 14
    )
    result = sl_sem.multilemma(row)
    assert result == {"": "\ue201д\ue205но\ue20dѧдъ"}
    result = sl_sem.var.multilemma(row)
    assert result == {"H": "\ue201д\ue205нородъ"}


def test_sub():
    # old semantics
    sl_sem = MainLangSemantics(
        FROM_LANG, 4, [6, 7, 8, 9], VarLangSemantics(FROM_LANG, 0, [1, 2])
    )
    gr_sem = MainLangSemantics(
        TO_LANG, 10, [11, 12, 13], VarLangSemantics(TO_LANG, 15, [16, 17])
    )
    row = (
        ["вь WGH", "въ", "въ + Loc.", "1/7d1", "оу", "оу насъ", "ѹ"]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["παρ’ Cs", "παρά ", "παρά + Acc."]
        + [""] * 6
    )
    result = gr_sem.var.multilemma(row, 1)
    assert result == {"Cs": "παρά + Acc."}

    result = sl_sem.var.multilemma(row, 1)
    assert result == {Source("WGH"): "въ + Loc."}


def test_sub_std_sem():
    row = (
        [
            "хⷪ҇домь спѣюще WG ход\ue205т\ue205 с пѣн\ue205\ue201мь H",
            "ходъ WG",
            "ходомь спѣт\ue205 WG",
            "",
            "14/072d18-19",
            "",
            "себе• по поут\ue205 хо-",
            "ход\ue205т\ue205 спѣт\ue205",
            "ход\ue205т\ue205 спѣѭще ≠",
        ]
        + [""] * 2
        + ["προβαίνοντες", "προβαίνω"]
        + [""] * 13
        + ["hl05|hl00"]
    )
    result = sl_sem.var.multilemma(row, 1)
    assert result == {Source("WG"): "ходомь спѣт\ue205"}
    result = sl_sem.var.multilemma(row)
    assert result == {Source("WG"): "ходъ"}


def test_paris():
    """Greek opies held in Paris library are indicated by P?"""
    # old semantics, so that variants are in word, not lemma
    gr_sem = MainLangSemantics(
        TO_LANG, 10, [11, 12, 13], VarLangSemantics(TO_LANG, 15, [16, 17])
    )

    row = (
        [""] * 4
        + ["12/67d19", "\ue20dьтеть•", "\ue20dьтеть• въꙁлѣга-", "\ue20d\ue205ст\ue205"]
        + [""] * 3
        + ["τιμὰς"]
        + [""] * 4
        + ["τιμᾷ MPaPb", "τιμάω"]
        + [""] * 9
    )
    result = gr_sem.var.multilemma(row)
    assert result == {Source("MPaPb"): "τιμᾷ"}

    row = (
        [""] * 4
        + [
            "12/67d19",
            "въꙁлѣган\ue205е",
            "\ue20dьтеть• въꙁлѣга-",
            "въꙁлѣган\ue205\ue201",
        ]
        + [""] * 3
        + ["ἀνάκλισιν", "ἀνάκλισις"]
        + [""] * 3
        + ["ἀνάκλησιν CsMPcPa"]
        + [""] * 10
    )
    result = gr_sem.var.multilemma(row)
    assert result == {Source("CsMPcPa"): "ἀνάκλησιν"}


def test_bozhii():
    row = (
        ["б\ue010ж\ue205 W б\ue010ж\ue205\ue205 G б\ue010жї\ue205 H", "бож\ue205\ue205"]
        + [""] * 2
        + ["1/7a4", "боꙁѣ", "о боꙁѣ словес\ue205•", "богъ", "Dat."]
        + [""] * 2
        + ["Θεοῦ", "θεός", "Gen."]
        + [""] * 13
    )
    result = sl_sem.var.multilemma(row)
    assert result == {Source("GHW"): "бож\ue205\ue205"}


def test_puteshestive():
    rows = [
        [
            "шьст\ue205ꙗ G шьств\ue205ꙗ H пꙋт\ue205 GH",
            "шьст\ue205\ue201 G / шьств\ue205\ue201 H",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/028d18",
            "поутошьств\ue205ꙗ",
            "поутошьств\ue205-",
            "пѫтошьств\ue205\ue201",
        ]
        + [""] * 3
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00"]
        + ["1"] * 4,
        [
            "шьст\ue205ꙗ G шьств\ue205ꙗ H пꙋт\ue205 GH",
            "пѫть",
            "шьст\ue205\ue201 пѫт\ue205 G / шьств\ue205\ue201 пѫт\ue205 H",
            "",
            "05/028d18",
            "поутошьств\ue205ꙗ",
            "",
            "пѫтошьств\ue205\ue201",
        ]
        + [""] * 3
        + ["ὁδοιπορίας", "ὁδοιπορία"]
        + [""] * 13
        + ["hl00"]
        + ["1"] * 4,
    ]

    result = sl_sem.var.multilemma(rows[0])
    assert result == {Source("G"): "шьст\ue205\ue201", Source("H"): "шьств\ue205\ue201"}

    result = sl_sem.var.multilemma(rows[0], 1)
    assert result == {
        Source("G"): "шьст\ue205\ue201 пѫт\ue205",
        Source("H"): "шьств\ue205\ue201 пѫт\ue205",
    }

    result = sl_sem.var.multilemma(rows[1])
    assert result == {Source("GH"): "пѫть"}

    result = sl_sem.var.multilemma(rows[1], 1)
    assert result == {
        Source("G"): "шьст\ue205\ue201 пѫт\ue205",
        Source("H"): "шьств\ue205\ue201 пѫт\ue205",
    }


def test_velichanie():
    rows = [
        ["вел\ue205\ue20dан\ue205е WGH", "вел\ue205\ue20dан\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["1"] * 4,
        ["невел\ue205\ue20d\ue205\ue201 WGH", "невел\ue205\ue20d\ue205\ue201"]
        + [""] * 2
        + [
            "05/21a19",
            "невел\ue205\ue20dан\ue205\ue201",
            "тъкмо• нъ \ue205 не-",
            "невел\ue205\ue20dан\ue205\ue201",
        ]
        + [""] * 3
        + ["ἄτυφον", "ἄτυφος"]
        + [""] * 14
        + ["2", "1"] * 2,
    ]

    result = sl_sem.var.multilemma(rows[0])
    assert result == {Source("GHW"): "вел\ue205\ue20dан\ue205\ue201"}

    result = sl_sem.var.multilemma(rows[1])
    assert result == {Source("WHG"): "невел\ue205\ue20d\ue205\ue201"}


def test_gr_variant():
    row = (
        [""] * 4
        + ["16/80a08", "хлѣбꙑ•", "ре\ue20dе хлѣбꙑ• не", "хлѣбъ"]
        + [""] * 3
        + ["om."] * 2
        + [""] * 3
        + ["ἄρτους Ch", "ἄρτος"]
        + [""] * 9
        + ["1"] * 4
    )
    result = gr_sem.var.multilemma(row)
    assert result == {Source("Ch"): "ἄρτος"}


def test_est_in_var_no_main():
    sl_sem = MainLangSemantics(
        FROM_LANG,
        5,
        [7, 8, 9, 10],
        VarLangSemantics(FROM_LANG, 0, [1, 2, 3], cnt_col=STYLE_COL + 2),
        cnt_col=STYLE_COL + 1,
    )

    row = (
        [
            "\ue201сть GH",
            "бꙑт\ue205",
            "",
            "gramm.",
            "07/47a06",
            "om.",
            "сътвор\ue205лъ",
            "om.",
        ]
        + [""] * 3
        + ["Ø"] * 2
        + [""] * 13
        + ["hl03"]
        + ["1"] * 4
    )
    # result = sl_sem.var.multilemma(row)
    # assert result == {Source("GH"): "бꙑт\ue205"}

    # result = sl_sem.var.multilemma(row, 1)
    # assert result == {}

    result = sl_sem.var.multilemma(row, 2)
    assert result == {Source("GH"): "gramm."}


def test_pros_eis():
    row = (
        [""] * 4
        + ["35/162a10", "въ", "въ \ue205ер\ue205хѫ• съвы-", "въ", "въ + Acc."]
        + [""] * 2
        + ["om."] * 2
        + [""] * 3
        + ["εἰς MPePgPkR πρὸς PhPi", "εἰς MPePgPkR / πρός PhPi", "πρός + Acc. PhPi"]
        + [""] * 7
        + ["bold|italic"]
    )
    assert gr_sem.var.multilemma(row) == {
        Source("PhPi"): "πρός",
        Source("MPePgPkR"): "εἰς",
    }
    assert gr_sem.var.multilemma(row, 1) == {Source("PhPi"): "πρός + Acc."}


def test_greh_reorganised():
    row = (
        [""] * 4
        + ["05/17b12", "грѣхъм\ue205", "оубо ꙗко грѣ-", "грѣхъ"]
        + [""] * 3
        + ["υἱός", "# υἱός"]
        + [""] * 14
        + ["1"] * 4
    )
    assert gr_sem.multilemma(row) == {Source(""): "# υἱός"}


def test_gen_lemma2():
    row = (
        [""] * 4
        + ["14/71c11", "въ\ue205ноу", "ща въ\ue205ноу• по-", "въ\ue205нѫ"]
        + [""] * 3
        + ["διηνεκῶς"] * 2
        + [""] * 3
        + ["διὰ MVPa", "διά", "διά + Gen.", "διὰ παντός"]
        + [""] * 6
        + ["hl16:FFFCD5B5|hl18:FF92D050"]
    )

    assert gr_sem.var.multilemma(row, 1) == {Source("MVPa"): "διά + Gen."}


def test_mutliple_gen_lemma2():
    row = (
        [""] * 4
        + ["38/176a15", "по", "слоужꙗщоу по", "по", "по + Loc."]
        + [""] * 2
        + ["om."]
        + [""] * 4
        + ["μετὰ Cs κατὰ Fb", "μετά Cs / κατά Fb", "μετά + Acc. Cs / κατά + Gen. Fb"]
        + [""] * 8
    )

    assert gr_sem.var.multilemma(row, 1) == {
        Source("Fb"): "κατά + Gen.",
        Source("Cs"): "μετά + Acc.",
    }


if __name__ == "__main__":
    test_basic_1()
