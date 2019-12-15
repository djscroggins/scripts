#!/usr/bin/env bash
deactivate && python -m venv .env && source $_/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
