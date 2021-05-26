#!/bin/bash

cd extractor/test
for filename in *.docx; do
    ../extractor.py -p $filename
    stripped="${filename%.docx}"
    unzip "$stripped.expected.xlsx" -d expected
    unzip "$stripped.xlsx" -d out
    if [ -z "$(diff expected/xl/worksheets/sheet1.xml out/xl/worksheets/sheet1.xml)" ]; then
        echo "No differences"
    else
        echo "DIFFERENCES FOUND!"
    fi
    rm -rf expected
    rm -rf out
    rm "$stripped.xlsx"
done
cd ../..