from pathlib import Path
from cyk.grammar import load_grammar
from cyk.cyk import cyk_parse
from cyk.tokenize import normalize_sentence
from cyk.cnf import to_cnf_pipeline

ROOT = Path(__file__).resolve().parents[1]
ENG = ROOT / "data/grammars/english-cnf.txt"
ENG_SRC = ROOT / "data/grammars/english.txt"

def _tok(s: str):
    return normalize_sentence(s)

def test_english_accept_simple():
    G = load_grammar(str(ENG))
    ok, *_ = cyk_parse(G, _tok("She eats a cake."))
    assert ok

def test_english_accept_with_pp():
    G = load_grammar(str(ENG))
    ok, *_ = cyk_parse(G, _tok("She eats a cake with a fork."))
    assert ok

def test_english_accept_det_n_vp():
    G = load_grammar(str(ENG))
    ok, *_ = cyk_parse(G, _tok("The cat drinks the beer."))
    assert ok

def test_english_reject_bad_order():
    G = load_grammar(str(ENG))
    ok, *_ = cyk_parse(G, _tok("Eats she cake."))
    assert not ok

def test_english_reject_wrong_verb_form():
    G = load_grammar(str(ENG))
    ok, *_ = cyk_parse(G, _tok("She eat a cake."))
    assert not ok

def test_pipeline_cnf_keeps_language():
    # La conversión a CNF del mismo CFG debe seguir aceptando
    G0 = load_grammar(str(ENG_SRC))
    G = to_cnf_pipeline(G0)
    ok, *_ = cyk_parse(G, _tok("She eats a cake with a fork."))
    assert ok
