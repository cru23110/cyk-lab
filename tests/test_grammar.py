# tests/test_grammar.py
from src.cyk.grammar import load_grammar
def test_load():
    G = load_grammar("data/grammars/1-cnf.txt")
    assert "E" in G["N"] and "id" in G["T"]
