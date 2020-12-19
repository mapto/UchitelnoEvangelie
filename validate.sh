#!/bin/sh -e

echo '>>> Skipping Pylint'
# pylint -E .

echo '>>> Running Mypy'
mypy .

echo '>>> Running Pytest'
pytest -vv --doctest-modules -s . # --disable-warnings

echo '>>> Running Black'
black .
