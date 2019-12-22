#!/usr/bin/env bash
source scripts.env
cd python_src
date
if $(pwd)/.env/bin/python setup_logs.py && $(pwd)/.env/bin/python routines/clean_downloads.py ; then
    echo "SUCCESS"
fi
