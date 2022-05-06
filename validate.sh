#!/bin/sh -e

echo '>>> Cleaning cache'
rm -rf .mypy_cache
rm -rf .pytest_cache
rm -rf extractor/__pycache__
rm -rf integrator/__pycache__
rm -rf integrator/.ipynb_checkpoints
rm -rf integrator/.pytest_cache
rm -rf semantics/__pycache__
rm -rf model/__pycache__

echo '>>> Skipping Pylint'
# pylint -E extractor
# pylint -E integrator/

echo '>>> Running Mypy'
mypy extractor
mypy integrator
mypy integrator/semantics
mypy integrator/model

echo '>>> Running Pytest'
pytest -vv --doctest-modules -s extractor # --disable-warnings
pytest -vv --doctest-modules -s integrator # --disable-warnings
pytest -vv --doctest-modules -s integrator/semantics # --disable-warnings
pytest -vv --doctest-modules -s integrator/model # --disable-warnings

echo '>>> Running Black'
black extractor
black integrator
black integrator/semantics
black integrator/model