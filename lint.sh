#!/usr/bin/env bash
docformatter --recursive --in-place typenv/ tests/ &&
isort -rc . &&
black . &&
flake8 . &&
mypy . &&
echo "Success!"
