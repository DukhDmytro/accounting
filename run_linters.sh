#!/bin/bash
echo 'PYLINT'
pylint *.py **/*.py
echo ''
echo 'FLAKE8'
flake8
echo ''
echo 'MYPY'
mypy . --ignore-missing-imports
