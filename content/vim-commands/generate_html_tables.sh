#!/usr/bin/env bash
set -x
python generate_html_tables.py motions.txt          > motions.html
python generate_html_tables.py operators.txt        > operators.html
python generate_html_tables.py visual-operators.txt > visual-operators.html
python generate_html_tables.py text-objects.txt     > text-objects.html
python generate_html_tables.py modifiers.txt        > modifiers.html
python random_commands.py                           > random-commands.html
