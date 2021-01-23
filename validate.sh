#!/bin/sh -e

echo '>>> Skipping Pylint'
# pylint -E extractor
# pylint -E integrator/

echo '>>> Running Mypy'
mypy extractor
mypy integrator

echo '>>> Running Pytest'
pytest -vv --doctest-modules -s extractor # --disable-warnings
pytest -vv --doctest-modules -s integrator # --disable-warnings

echo '>>> Running Black'
black extractor
black integrator
