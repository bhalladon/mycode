#!/bin/sh
export PYTHONPATH=/ui_project/
export webbrowser=firefox
export headless=false
cd /ui_project/testscripts
pip install selenium
python -m unittest test1
