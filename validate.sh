#!/bin/sh -e

echo '>>> Skipping Pylint'
# pylint -E extractor

echo '>>> Running Mypy'
mypy extractor

echo '>>> Running Pytest'
pytest -vv --doctest-modules -s extractor # --disable-warnings

echo '>>> Running Black'
black extractor
