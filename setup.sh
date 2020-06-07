#!/bin/bash

export PIPENV_VENV_IN_PROJECT=true
pip3 install --upgrade pip pipenv
pipenv --python /usr/bin/python3
pipenv sync --dev
pipenv install bottle docopt docx openpyxl
