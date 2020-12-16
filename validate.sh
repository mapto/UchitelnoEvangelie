#!/bin/sh -e

echo '>>> Skipping Pylint'
# pylint -E .

echo '>>> Running Mypy'
mypy .

echo '>>> Absent Pytest'
# pytest -vv --doctest-modules -s . --disable-warnings

echo '>>> Running Black'
black .
