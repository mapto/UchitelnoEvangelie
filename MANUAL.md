# Extractor

The extractor reads an annotated document and generates a spreadsheet with one word from the document text per line.

The generated spreadsheet utilises the following formulas:

* https://support.microsoft.com/en-us/office/vlookup-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1
* https://support.microsoft.com/en-us/office/ifna-function-6626c961-a569-42fc-a49d-79b4951fd461
* https://support.microsoft.com/en-us/office/isformula-function-e4d1355f-7121-4ef2-801e-3839bfd6b1e5
* https://support.microsoft.com/en-us/office/if-function-69aed7c9-4e8a-4755-a9bc-aa8bbff73be2


# Integrator and Index Generator

For to be indicated as part of a biblical citation, a word needs to be marked as bold and italic. In general bold and italic are being preserved into the integrator list and generated index.

Highlighting (actually background colouring):
* When several words need to be considered as a phrase, this grouping needs to be indicated in the spreadsheet by changing the background colour of one of the word columns for all the rows in the phrase.
* When a lemma has to be included in the group for its langauge, but not in the translation, this can be encoded as highlighting of the second lemma
* When a word has some special function (e.g. grammatical, conditional, passive, etc), a third or later lemmas needs to be indicated by changing its background colour.

TODO: explain multivariants