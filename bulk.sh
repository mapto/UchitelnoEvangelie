#!/bin/bash

# Call from the directory of the xlsx files.
# This is in silent mode, but will still print warnings and errors.

# from https://stackoverflow.com/a/246128/1827854
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo $SCRIPT_DIR

OIFS="$IFS"
IFS=$'\n'

cd $1
for FILENAME in `find . -type f -name "*.xlsx" | sort`; do
    echo $FILENAME
    $SCRIPT_DIR/integrator/integrator.py -s $FILENAME
done
