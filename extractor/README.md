# Extractor

The vocabulary extractor takes an annotated document and extracts an aligned (between variants) vocabulary spreadsheet. It also adds some spreadsheet formulas to improve usability (i.e. autofill on repetitions).

## Examples

![An animation showing an example of what the extractor does](../docs/extractor-demo.gif) [src](https://docs.google.com/presentation/d/139kNBtE6D1VM_1ScXHugP0nJWT8lVl61_zyEFkcxvU0)

See futher examples in [test](test/).

## Spreadsheet Formulas

The extractor reads an annotated document and generates a spreadsheet with one word from the document text per line.

The generated spreadsheet utilises the following formulas:

* https://support.microsoft.com/en-us/office/vlookup-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1
* https://support.microsoft.com/en-us/office/ifna-function-6626c961-a569-42fc-a49d-79b4951fd461
* https://support.microsoft.com/en-us/office/isformula-function-e4d1355f-7121-4ef2-801e-3839bfd6b1e5
* https://support.microsoft.com/en-us/office/if-function-69aed7c9-4e8a-4755-a9bc-aa8bbff73be2

