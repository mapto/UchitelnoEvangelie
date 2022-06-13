# languages
FROM_LANG = "sl"
TO_LANG = "gr"

# first letter is main variant
MAIN_SL = "S"  # for Synodal
ALT_SL = "W"  # for Wiener
VAR_SL = "WGH"
DEFAULT_SL = VAR_SL
MAIN_GR = ""  # "C" for Cramer
# VAR_GR = "BCMAsChP" + "".join(f"P{chr(ord('a')+c)}" for c in range(26))  # for Paris x
DEFAULT_GR = "C"  # for Cramer
VAR_GR = DEFAULT_GR + (
    "A"  # 	Athina, EBE, 56, f. 47r ff
    "Sp"  # 	ASP Città del Vaticano, BAV, Archivio di S. Pietro B 59, f. 132r ff
    "Ca"  # 	Кирил Александрийски
    "Ch"  # 	Chrysostomos….
    "Fa"  # 	F6/5 Firenze, BML, Plut.6.5
    "Fb"  # 	F8/29 Firenze, BML, Plut.8.29
    "L"  # 	Oxford, Bodl., Laud 33, f. 29v ff
    "M"  # 	München, Universitätsbibliothek, 2° 30 (Cim. 16)
    "Ma"  # 	M208 München, BSB, Gr. 208, f. 60v ff
    "B"  # 	Oxford, Bodleian Library, Auct. T.1.4
    "Pa"  # 	P188 Paris, BnF, Grec 188, f. 43r ff
    "Pb"  # 	P191 Paris, BnF, Grec 191
    "Pc"  # 	P199 Paris, BnF, Grec 199
    "Pd"  # 	P200 Paris, BnF, Grec 200
    "Pe"  # 	P201 Paris, BnF, Grec 201
    "Pf"  # 	P203 Paris, BnF, Grec 203, f. 196r ff
    "Pg"  # 	P231 Paris, BnF, Grec 231
    "Ph"  # 	P701 Paris, BnF, Grec 701
    "Pi"  # 	P702 Paris, BnF, Grec 702
    "Pk"  # 	P704 Paris, BnF, Grec 704
    "Pl"  # 	PC71 Paris, BnF, Coislin 71
    "Pm"  # 	PC23 Paris, BnF, Coislin 23
    "Pn"  # 	PC195 Paris, BnF, Coislin 195
    "Po"  # 	PC206 Paris, BnF, Coislin 206, f. 85r ff
    "R"  # 	Roma, Biblioteca Angelica, Gr. 67, f. 14r ff
    "Tb"  # 	Тит Востронски
    "V"  # 	VC444 Città del Vaticano, BAV, Barb. gr. 444, f. 95r ff
    "Z"  # 	Venezia, BNM, Z.544, f. 54v ff
    "Nt"  # 	NA
)

other_lang = {TO_LANG: FROM_LANG, FROM_LANG: TO_LANG}
