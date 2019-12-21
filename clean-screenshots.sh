#!/usr/bin/env bash
source scripts.env
cd python_src
$(pwd)/.env/bin/python setup_logs.py && $(pwd)/.env/bin/python routines/clean_screenshots.py
