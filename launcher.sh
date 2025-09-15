#!/bin/bash
# launcher.sh — your GUI launcher

# path to your virtual environment
VENV_DIR="venv"

# activate it
source "$VENV_DIR/bin/activate"

# run your GUI
venv/bin/python3 main.py
