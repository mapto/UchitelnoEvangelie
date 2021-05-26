#!/bin/bash

cd extractor/test
PARTS="docProps/app.xml xl/theme/theme1.xml xl/worksheets/sheet1.xml xl/styles.xml _rels/.rels xl/workbook.xml xl/_rels/workbook.xml.rels [Content_Types].xml"
# SKIPPED: docProps/core.xml, as it contains no relevant information, but timestamps
for FILENAME in *.docx; do
    ../extractor.py -p $FILENAME
    stripped="${FILENAME%.docx}"
    unzip "$stripped.expected.xlsx" -d expected
    unzip "$stripped.xlsx" -d out
    for NEXT in $PARTS; do 
        if [ -z "$(diff expected/$NEXT out/$NEXT)" ]; then
            echo "No differences in $NEXT"
        else
            echo "DIFFERENCES FOUND in $NEXT!"
            exit 0
        fi
    done
    rm -rf expected
    rm -rf out
    rm "$stripped.xlsx"
done
cd ../..