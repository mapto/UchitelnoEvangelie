from setup import sl_sem, gr_sem
from merger import merge, _close

raw = [
    [""] * 4
    + ["38/178c06"]
    + ["ₓ", ""] * 2
    + [""] * 2
    + ["τῶν", "ὁ"]
    + [""] * 13
    + ["hl11:FFFCD5B4|hl14:FFB8CCE4"],
    [""] * 4
    + ["38/178c06", "словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
    + [""] * 3
    + ["εἰρημένων", "λέγω", "τὸ εἰρημένον"]
    + [""] * 12
    + ["hl11:FFFCD5B4"],
]


def test_merge_sloves_inverse():
    rows = [r.copy() for r in raw]
    result = merge(rows, gr_sem, sl_sem)

    assert result == [
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "", "ₓ"]
        + [""] * 3
        + ["τῶν εἰρημένων", "ὁ"]
        + [""] * 13
        + ["hl11:FFFCD5B4|hl14:FFB8CCE4"]
        + ["1"] * 4,
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
        + [""] * 3
        + ["τῶν εἰρημένων", "λέγω", "τὸ εἰρημένον"]
        + [""] * 12
        + ["hl11:FFFCD5B4"]
        + ["1"] * 4,
    ]


def test_close_sloves_inverse():
    rows = [r.copy() for r in raw]
    result = _close(rows, gr_sem, sl_sem)

    assert result == [
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "", "ₓ"]
        + [""] * 3
        + ["τῶν εἰρημένων", "ὁ"]
        + [""] * 13
        + ["hl11:FFFCD5B4|hl14:FFB8CCE4"],
        [""] * 4
        + ["38/178c06", "ₓ словесъ", "\ue205хъ словесъ въспⷪ҇-", "слово"]
        + [""] * 3
        + ["τῶν εἰρημένων", "λέγω", "τὸ εἰρημένον"]
        + [""] * 12
        + ["hl11:FFFCD5B4"],
    ]


def test_merge_avramov_chad():
    rows = [
        [""] * 4
        + ["05/24b21"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τοὺς", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + [
            "05/24b21",
            "авраамовоу",
            "н\ue205ша сѧ• авраа-",
            "авраамовъ",
            # "авраамова \ue20dѧдь",
        ]
        + [""] * 3
        + ["περὶ", "περί", "περί + Acc.", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl13:FF92D050"],
        [""] * 4
        + ["", "ₓ"] * 2
        + [""] * 3
        + ["τὸν", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + [
            "05/24c01",
            "\ue20dадь",
            "мовоу \ue20dадь г\ue010лю-",
            "\ue20dѧдь",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["Ἀβραὰμ", "Ἀβραάμ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4"],
    ]

    result = merge(rows, sl_sem, gr_sem)

    assert result == [
        [""] * 4
        + ["05/24b21", "ₓ авраамовоу ₓ \ue20dадь", "", "ₓ"]
        + [""] * 3
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"]
        + ["1"] * 4,
        [""] * 4
        + [
            "05/024b21-c01",
            "ₓ авраамовоу ₓ \ue20dадь",
            "н\ue205ша сѧ• авраа-",
            "авраамовъ",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "περί & Ἀβραάμ", "", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl13:FF92D050"]
        + ["1"] * 4,
        [""] * 4
        + ["05/24b21", "ₓ авраамовоу ₓ \ue20dадь", "", "ₓ"]
        + [""] * 3
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7", "2"]
        + ["1"] * 3,
        [""] * 4
        + [
            "05/024b21-c01",
            "ₓ авраамовоу ₓ \ue20dадь",
            "мовоу \ue20dадь г\ue010лю-",
            "\ue20dѧдь",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "περί & Ἀβραάμ", "", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4"]
        + ["1"] * 4,
    ]


def test_merge_avramov_chad_inverse():
    rows = [
        [""] * 4
        + ["05/24b21"]
        + ["ₓ", ""] * 2
        + [""] * 2
        + ["τοὺς", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + ["05/24b21", "авраамовоу", "н\ue205ша сѧ• авраа-", "авраамовъ"]
        + [""] * 3
        + ["περὶ", "περί", "περί + Acc.", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl13:FF92D050"],
        [""] * 4
        + ["", "ₓ"] * 2
        + [""] * 3
        + ["τὸν", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"],
        [""] * 4
        + [
            "05/24c01",
            "\ue20dадь",
            "мовоу \ue20dадь г\ue010лю-",
            "\ue20dѧдь",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["Ἀβραὰμ", "Ἀβραάμ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4"],
    ]

    result = merge(rows, gr_sem, sl_sem)

    assert result == [
        [""] * 4
        + ["05/24b21", "ₓ авраамовоу ₓ \ue20dадь", "", "ₓ"]
        + [""] * 3
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7"]
        + ["1"] * 4,
        [""] * 4
        + [
            "05/024b21-c01",
            "ₓ авраамовоу ₓ \ue20dадь",
            "н\ue205ша сѧ• авраа-",
            "авраамовъ & \ue20dѧдь",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "περί", "περί + Acc.", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 11
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl13:FF92D050"]
        + ["1"] * 4,
        [""] * 4
        + ["05/24b21", "ₓ авраамовоу ₓ \ue20dадь", "", "ₓ"]
        + [""] * 3
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "ὁ"]
        + [""] * 13
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4|hl14:FFB4C7E7", "2"]
        + ["1"] * 3,
        [""] * 4
        + [
            "05/024b21-c01",
            "ₓ авраамовоу ₓ \ue20dадь",
            "мовоу \ue20dадь г\ue010лю-",
            "авраамовъ & \ue20dѧдь",
            "авраамова \ue20dѧдь",
        ]
        + [""] * 2
        + ["τοὺς περὶ τὸν Ἀβραὰμ", "Ἀβραάμ", "ὁ περὶ τὸν Ἀβραάμ"]
        + [""] * 12
        + ["hl05:FFC5E0B4|hl11:FFC5E0B4"]
        + ["1"] * 4,
    ]


def test_merge_iakov_brata():
    rows = [
        [""] * 4
        + ["38/181a19"]
        + ["ₓ", ""] * 2
        + [""] * 7
        + ["οἱ", "ὁ"]
        + [""] * 8
        + ["hl05:FFFCD5B4|hl16:FFFCD5B4|hl19:FFB4C7E7"],
        [""] * 4
        + [
            "38/181a19",
            "\ue205ꙗковъ",
            "\ue20dоуть сꙗ \ue205ꙗко-",
            "\ue205ꙗковъ",
            "\ue205аковъ \ue205 брат\ue205ꙗ \ue201го",
        ]
        + [""] * 2
        + ["om."] * 2
        + [""] * 3
        + ["περὶ", "περί", "περί + Acc.", "οἱ περὶ Ἰάκωβον"]
        + [""] * 6
        + ["hl05:FFFCD5B4|hl16:FFFCD5B4|hl18:FFA9D18E"],
        [""] * 4
        + ["38/181a20", "\ue205", "въ \ue205 брат\ue205ꙗ его•", "\ue205 conj."]
        + [""] * 8
        + ["Ἰάκωβον", "Ἰάκωβος"]
        + [""] * 8
        + ["hl05:FFFCD5B4|hl16:FFFCD5B4"],
        [""] * 4
        + ["38/181a20", "брат\ue205ꙗ", "въ \ue205 брат\ue205ꙗ его•", "брат\ue205ꙗ"]
        + [""] * 18
        + ["hl05:FFFCD5B4"],
        [""] * 4
        + ["38/181a20", "его•", "въ \ue205 брат\ue205ꙗ его•", "\ue205 pron."]
        + [""] * 18
        + ["hl05:FFFCD5B4"],
    ]

    result = merge(rows, sl_sem, gr_sem)

    assert result == [
        [""] * 4
        + ["38/181a19", "ₓ \ue205ꙗковъ \ue205 брат\ue205ꙗ его•", "", "ₓ"]
        + [""] * 3
        + ["om."]
        + [""] * 4
        + ["οἱ περὶ Ἰάκωβον Cs", "ὁ"]
        + [""] * 8
        + ["hl05:FFFCD5B4|hl16:FFFCD5B4|hl19:FFB4C7E7"]
        + ["1"] * 4,
        [""] * 4
        + [
            "38/181a19-20",
            "ₓ \ue205ꙗковъ \ue205 брат\ue205ꙗ его•",
            "\ue20dоуть сꙗ \ue205ꙗко-",
            "\ue205ꙗковъ",
            "\ue205аковъ \ue205 брат\ue205ꙗ \ue201го",
        ]
        + [""] * 2
        + ["om."] * 2
        + [""] * 3
        + [
            "οἱ περὶ Ἰάκωβον Cs",
            "περί & Ἰάκωβος Cs",
            "",
            "οἱ περὶ Ἰάκωβον Cs",
        ]
        + [""] * 6
        + ["hl05:FFFCD5B4|hl16:FFFCD5B4|hl18:FFA9D18E"]
        + ["1"] * 4,
        [""] * 4
        + [
            "38/181a19-20",
            "ₓ \ue205ꙗковъ \ue205 брат\ue205ꙗ его•",
            "въ \ue205 брат\ue205ꙗ его•",
            "\ue205 conj.",
            "\ue205аковъ \ue205 брат\ue205ꙗ \ue201го",
        ]
        + [""] * 2
        + ["om."] * 2
        + [""] * 3
        + ["οἱ περὶ Ἰάκωβον Cs", "περί & Ἰάκωβος Cs", "", "οἱ περὶ Ἰάκωβον Cs"]
        + [""] * 6
        + ["hl05:FFFCD5B4|hl16:FFFCD5B4"]
        + ["1"] * 4,
        [""] * 4
        + [
            "38/181a19-20",
            "ₓ \ue205ꙗковъ \ue205 брат\ue205ꙗ его•",
            "въ \ue205 брат\ue205ꙗ его•",
            "брат\ue205ꙗ",
            "\ue205аковъ \ue205 брат\ue205ꙗ \ue201го",
        ]
        + [""] * 2
        + ["om."] * 2
        + [""] * 3
        + ["οἱ περὶ Ἰάκωβον Cs", "περί & Ἰάκωβος Cs", "", "οἱ περὶ Ἰάκωβον Cs"]
        + [""] * 6
        + ["hl05:FFFCD5B4"]
        + ["1"] * 4,
        [""] * 4
        + [
            "38/181a19-20",
            "ₓ \ue205ꙗковъ \ue205 брат\ue205ꙗ его•",
            "въ \ue205 брат\ue205ꙗ его•",
            "\ue205 pron.",
            "\ue205аковъ \ue205 брат\ue205ꙗ \ue201го",
        ]
        + [""] * 2
        + ["om."] * 2
        + [""] * 3
        + ["οἱ περὶ Ἰάκωβον Cs", "περί & Ἰάκωβος Cs", "", "οἱ περὶ Ἰάκωβον Cs"]
        + [""] * 6
        + ["hl05:FFFCD5B4"]
        + ["1"] * 4,
    ]


def test_gen_lemma2():
    rows = [
        [""] * 4
        + ["14/71c11", "въ\ue205ноу", "ща въ\ue205ноу• по-", "въ\ue205нѫ"]
        + [""] * 3
        + ["διηνεκῶς"] * 2
        + [""] * 3
        + ["διὰ MVPa", "διά", "διά + Gen", "διὰ παντός"]
        + [""] * 6
        + ["hl16:FFFCD5B5|hl18:FF92D050"],
        [""] * 16 + ["παντός MVPa", "πᾶς"] + [""] * 8 + ["hl16:FFFCD5B5"],
    ]

    result = merge(rows, gr_sem.var, sl_sem)

    assert result == [
        [""] * 4
        + ["14/071c11", "въ\ue205ноу", "ща въ\ue205ноу• по-", "въ\ue205нѫ"]
        + [""] * 3
        + ["διηνεκῶς"] * 2
        + [""] * 3
        + ["διὰ παντός MVPa", "διά MVPa", "διά + Gen", "διὰ παντός MVPa"]
        + [""] * 6
        + ["hl16:FFFCD5B5|hl18:FF92D050"]
        + ["1"] * 4,
        [""] * 4
        + ["14/071c11", "въ\ue205ноу", "", "въ\ue205нѫ"]
        + [""] * 3
        + ["διηνεκῶς"] * 2
        + [""] * 3
        + ["διὰ παντός MVPa", "πᾶς MVPa", "διὰ παντός MVPa"]
        + [""] * 7
        + ["hl16:FFFCD5B5"]
        + ["1"] * 4,
    ]


def test_gen_lemma3():
    rows = [
        [""] * 4
        + [
            "35/162d12",
            "\ue205сцѣл\ue205",
            "ны \ue205сцѣл\ue205 отъ",
            "\ue205цѣл\ue205т\ue205",
            "\ue205цѣл\ue205т\ue205 отъ стрѹпъ",
            "",
            "",
            "πρὸς",
            "πρός",
            "πρός + Acc.",
        ]
        + [""] * 12
        + ["hl05:FFFCD5B4|hl11:FFFCD5B4|hl13:FF92D050"],
        [""] * 4
        + ["35/162d12"]
        + [""] * 6
        + ["τελείαν", "τέλειος", "", "πρὸς τέλειαν θεραπείαν ἀρκέω"]
        + [""] * 11
        + ["hl05:FFFCD5B4|hl11:FFFCD5B4"],
        [""] * 4
        + ["35/162d12", "отъ", "ны \ue205сцѣл\ue205 отъ", "отъ"]
        + [""] * 3
        + ["θεραπείαν", "θεραπεία"]
        + [""] * 13
        + [
            "hl05:FFFCD5B4|hl11:FFFCD5B4",
        ],
        [""] * 4
        + ["35/162d13", "строупъ•", "строупъ• н\ue205 ле-", "стрѹпъ"]
        + [""] * 3
        + ["ἤρκεσεν", "ἀρκέω"]
        + [""] * 13
        + [
            "hl05:FFFCD5B4|hl11:FFFCD5B4",
        ],
    ]

    result = merge(rows, gr_sem, sl_sem)

    assert result == [
        [""] * 4
        + [
            "35/162d12-13",
            "\ue205сцѣл\ue205 отъ строупъ•",
            "ны \ue205сцѣл\ue205 отъ",
            "\ue205цѣл\ue205т\ue205 & отъ & стрѹпъ",
            "\ue205цѣл\ue205т\ue205 отъ стрѹпъ",
            "",
            "",
            "πρὸς τελείαν θεραπείαν ἤρκεσεν",
            "πρός",
            "πρός + Acc.",
            "πρὸς τέλειαν θεραπείαν ἀρκέω",
        ]
        + [""] * 11
        + ["hl05:FFFCD5B4|hl11:FFFCD5B4|hl13:FF92D050"]
        + ["1"] * 4,
        [""] * 4
        + [
            "35/162d12-13",
            "\ue205сцѣл\ue205 отъ строупъ•",
            "",
            "\ue205цѣл\ue205т\ue205 & отъ & стрѹпъ",
            "\ue205цѣл\ue205т\ue205 отъ стрѹпъ",
            "",
            "",
            "πρὸς τελείαν θεραπείαν ἤρκεσεν",
            "τέλειος",
            "πρὸς τέλειαν θεραπείαν ἀρκέω",
        ]
        + [""] * 12
        + ["hl05:FFFCD5B4|hl11:FFFCD5B4"]
        + ["1"] * 4,
        [""] * 4
        + [
            "35/162d12-13",
            "\ue205сцѣл\ue205 отъ строупъ•",
            "ны \ue205сцѣл\ue205 отъ",
            "\ue205цѣл\ue205т\ue205 & отъ & стрѹпъ",
            "\ue205цѣл\ue205т\ue205 отъ стрѹпъ",
            "",
            "",
            "πρὸς τελείαν θεραπείαν ἤρκεσεν",
            "θεραπεία",
            "πρὸς τέλειαν θεραπείαν ἀρκέω",
        ]
        + [""] * 12
        + ["hl05:FFFCD5B4|hl11:FFFCD5B4"]
        + ["1"] * 4,
        [""] * 4
        + [
            "35/162d12-13",
            "\ue205сцѣл\ue205 отъ строупъ•",
            "строупъ• н\ue205 ле-",
            "\ue205цѣл\ue205т\ue205 & отъ & стрѹпъ",
            "\ue205цѣл\ue205т\ue205 отъ стрѹпъ",
            "",
            "",
            "πρὸς τελείαν θεραπείαν ἤρκεσεν",
            "ἀρκέω",
            "πρὸς τέλειαν θεραπείαν ἀρκέω",
        ]
        + [""] * 12
        + ["hl05:FFFCD5B4|hl11:FFFCD5B4"]
        + ["1"] * 4,
    ]


def test_raspati():
    rows = [
        ["распетоу WG", "распѧт\ue205"]
        + [""] * 2
        + ["18/89c21", "пропѧтоу", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"],
        ["быт\ue205 WG", "бꙑт\ue205"]
        + [""] * 2
        + ["18/89d01", "бꙑт\ue205•", "же пропѧтоу бꙑ-", "бꙑт\ue205", "", "gramm."]
        + [""] * 2
        + ["pass."]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl09:FFB8CCE4"],
    ]

    result = merge(rows, sl_sem, gr_sem)

    assert result == [
        ["распетоу быт\ue205 WG", "распѧт\ue205 WG"]
        + [""] * 2
        + ["18/089c21-d01", "пропѧтоу бꙑт\ue205•", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"]
        + ["1"] * 4,
        ["распетоу быт\ue205 WG", "бꙑт\ue205"]
        + [""] * 2
        + [
            "18/89d01",
            "пропѧтоу бꙑт\ue205•",
            "же пропѧтоу бꙑ-",
            "бꙑт\ue205",
            "",
            "gramm.",
            "",
            "σταυρωθῆναι",
            "pass.",
        ]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl09:FFB8CCE4"]
        + ["1"] * 4,
    ]


def test_raspati_var():
    rows = [
        ["распетоу WG", "распѧт\ue205"]
        + [""] * 2
        + ["18/89c21", "пропѧтоу", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"],
        ["быт\ue205 WG", "бꙑт\ue205"]
        + [""] * 2
        + ["18/89d01", "бꙑт\ue205•", "же пропѧтоу бꙑ-", "бꙑт\ue205", "", "gramm."]
        + [""] * 2
        + ["pass."]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl09:FFB8CCE4"],
    ]

    result = merge(rows, sl_sem.var, gr_sem)

    assert result == [
        ["распетоу быт\ue205 WG", "распѧт\ue205 WG"]
        + [""] * 2
        + ["18/089c21-d01", "пропѧтоу бꙑт\ue205•", "же пропѧтоу бꙑ-", "пропѧт\ue205"]
        + [""] * 3
        + ["σταυρωθῆναι", "σταυρόω"]
        + [""] * 13
        + ["hl05:FFFCD5B4"]
        + ["1"] * 4,
        ["распетоу быт\ue205 WG", "бꙑт\ue205 WG"]
        + [""] * 2
        + [
            "18/89d01",
            "пропѧтоу бꙑт\ue205•",
            "же пропѧтоу бꙑ-",
            "бꙑт\ue205",
            "",
            "gramm.",
            "",
            "σταυρωθῆναι",
            "pass.",
        ]
        + [""] * 13
        + ["hl05:FFFCD5B4|hl09:FFB8CCE4"]
        + ["1"] * 4,
    ]
