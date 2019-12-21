#!/usr/bin/env bash
cd python_src
export PYTHONPATH="/Users/davidscroggins/scripts/python_src"
$(pwd)/.env/bin/python setup_logs.py && $(pwd)/.env/bin/python routines/clean_screenshots.py
