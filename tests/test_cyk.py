from cyk.grammar import load_grammar
from cyk.cyk import cyk_parse
def test_cyk_accepts():
    G = load_grammar("data/grammars/1-cnf.txt")
    ok, *_ = cyk_parse(G, "id + id * id".split())
    assert ok
def test_cyk_rejects():
    G = load_grammar("data/grammars/1-cnf.txt")
    ok, *_ = cyk_parse(G, "+ id id".split())
    assert not ok
