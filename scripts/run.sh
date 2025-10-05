#!/usr/bin/env bash
set -e
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate

echo "[Arithmetic CNF] id + id * id"
python -m cyk.cli --grammar data/grammars/1-cnf.txt --sentence "id + id * id" --tree --time

echo
echo "[English CNF] She eats a cake with a fork."
python -m cyk.cli --grammar data/grammars/english-cnf.txt --sentence "She eats a cake with a fork." --normalize --tree --time || true
