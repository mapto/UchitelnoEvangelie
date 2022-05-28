#!/bin/sh -e

echo '>>> Cleaning cache'
rm -rf .mypy_cache
rm -rf .pytest_cache
rm -rf extractor/__pycache__
rm -rf integrator/__pycache__
rm -rf integrator/.ipynb_checkpoints
rm -rf integrator/.pytest_cache
rm -rf integrator/semantics/__pycache__
rm -rf integrator/model/__pycache__

echo '>>> Running Pylint'
# pylint -E extractor/*.py
pylint -E -v integrator/*.py
pylint -E -v integrator/model
pylint -E -v integrator/semantics

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
# processes also subdirectories
black extractor
black integrator
