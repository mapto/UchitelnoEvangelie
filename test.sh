#!/bin/bash

echo "Testing extractor..."
cd extractor/test
PARTS="docProps/app.xml xl/theme/theme1.xml xl/worksheets/sheet1.xml _rels/.rels xl/workbook.xml xl/_rels/workbook.xml.rels [Content_Types].xml"
#PARTS="docProps/app.xml xl/theme/theme1.xml xl/worksheets/sheet1.xml xl/styles.xml _rels/.rels xl/workbook.xml xl/_rels/workbook.xml.rels [Content_Types].xml"
# SKIPPED: docProps/core.xml, as it contains no relevant information, but timestamps
for FILENAME in *.docx; do
    ../extractor.py -p $FILENAME
    STRIPPED="${FILENAME%.docx}"
    unzip -q "$STRIPPED.expected.xlsx" -d expected
    unzip -q "$STRIPPED.xlsx" -d out
    for NEXT in $PARTS; do 
        if [ -n "$(diff expected/$NEXT out/$NEXT)" ]; then
            diff expected/$NEXT out/$NEXT
            echo "DIFFERENCES FOUND in $NEXT!"
            exit 0
        else
            echo "No differences in $NEXT"            
        fi
    done
    rm -rf expected
    rm -rf out
    rm "$STRIPPED.xlsx"
done
cd ../..

echo "Testing integrator..."
cd integrator/test
VARIANTS="list-gre list-sla"
PARTS="[Content_Types].xml _rels/.rels docProps/core.xml docProps/app.xml word/document.xml word/_rels/document.xml.rels word/styles.xml word/stylesWithEffects.xml word/settings.xml word/webSettings.xml word/fontTable.xml word/theme/theme1.xml customXml/item1.xml customXml/_rels/item1.xml.rels customXml/itemProps1.xml word/numbering.xml docProps/thumbnail.jpeg"
# SKIPPED: docProps/core.xml, as it contains no relevant information, but timestamps
for FILENAME in *.xlsx; do
    ../integrator.py -p $FILENAME
    for VAR in $VARIANTS; do
        STRIPPED="${FILENAME%.xlsx}"
        STRIPPED="$STRIPPED-$VAR"
        echo "Testing $STRIPPED"
        unzip -q "$STRIPPED.expected.docx" -d expected
        unzip -q "$STRIPPED.docx" -d out
        for NEXT in $PARTS; do
            if [ -n "$(diff expected/$NEXT out/$NEXT)" ]; then
                diff expected/$NEXT out/$NEXT
                echo "DIFFERENCES FOUND in $NEXT!"
                exit 0
            else
                echo "No differences in $NEXT"
            fi
        done
        rm -rf expected
        rm -rf out
        rm "$STRIPPED.docx"
    done
done
cd ../..

echo "Testing indexgenerator..."
cd integrator/test
VARIANTS="index-gre index-sla"
PARTS="[Content_Types].xml _rels/.rels docProps/core.xml docProps/app.xml word/document.xml word/_rels/document.xml.rels word/styles.xml word/stylesWithEffects.xml word/settings.xml word/webSettings.xml word/fontTable.xml word/theme/theme1.xml customXml/item1.xml customXml/_rels/item1.xml.rels customXml/itemProps1.xml word/numbering.xml docProps/thumbnail.jpeg"
# SKIPPED: docProps/core.xml, as it contains no relevant information, but timestamps
for FILENAME in *.xlsx; do
    ../indexgenerator.py -p $FILENAME
    for VAR in $VARIANTS; do
        STRIPPED="${FILENAME%.xlsx}"
        STRIPPED="$STRIPPED-$VAR"
        echo "Testing $STRIPPED"
        unzip -q "$STRIPPED.expected.docx" -d expected
        unzip -q "$STRIPPED.docx" -d out
        for NEXT in $PARTS; do 
            if [ -n "$(diff expected/$NEXT out/$NEXT)" ]; then
                diff expected/$NEXT out/$NEXT
                echo "DIFFERENCES FOUND in $NEXT!"
                exit 0
            else
                echo "No differences in $NEXT"
            fi
        done
        rm -rf expected
        rm -rf out
        rm "$STRIPPED.docx"
    done
done
cd ../..
