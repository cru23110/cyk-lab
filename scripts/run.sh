#!/usr/bin/env bash
set -e
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate
python -m cyk.cli --grammar data/grammars/1-cnf.txt --sentence "id + id * id" --tree --time
