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

echo '>>> Running Autoflake'
autoflake --remove-all-unused-imports --remove-unused-variables -i -r extractor
autoflake --remove-all-unused-imports --remove-unused-variables -i -r integrator

echo '>>> Running Pylint'
# pylint -E extractor/*.py
pylint -E -v integrator/*.py
pylint -E -v integrator/model
pylint -E -v integrator/semantics

echo '>>> Running Mypy'
mypy extractor # --install-types --ignore-missing-imports
mypy integrator # --install-types --ignore-missing-imports
mypy integrator/semantics # --install-types --ignore-missing-imports
mypy integrator/model # --install-types --ignore-missing-imports

echo '>>> Running Pytest'
# processes also subdirectories
pytest --doctest-modules -s extractor  #  -vv -o log_cli=true
pytest --doctest-modules -s integrator #  -vv -o log_cli=true

echo '>>> Running Black'
# processes also subdirectories
black extractor
black integrator
