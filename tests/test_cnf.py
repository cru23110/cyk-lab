from cyk.grammar import load_grammar
from cyk.cnf import to_cnf_pipeline
def test_identity_pipeline_currently():
    G = load_grammar("data/grammars/1.txt")
    G2 = to_cnf_pipeline(G)
    assert isinstance(G2, dict)
