# benchmark.py
import time
from pathlib import Path
from src.cyk.grammar import load_grammar
from src.cyk.cyk import cyk_parse
from src.cyk.tokenize import normalize_sentence

def bench(grammar_path: str, sentences):
    G = load_grammar(grammar_path)
    print(f"Grammar: {grammar_path}")
    for s in sentences:
        tokens = normalize_sentence(s)
        t0 = time.perf_counter()
        ok, *_ = cyk_parse(G, tokens)
        dt = (time.perf_counter() - t0) * 1000
        print(f"[{ 'OK' if ok else 'NO' :>2}] {dt:7.3f} ms  | {s}")

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    eng = root / "data/grammars/english-cnf.txt"
    sentences = [
        "She eats a cake.",
        "He eats the cake with a fork.",
        "He drinks the beer.",
        "She eats the soup with a spoon.",
        "He cuts the meat with a knife.",
        "Eats she cake.",
        "She eat a cake.",
        "The drinks cat beer.",
        "Cake eats she.",
        "The eats. she cake"
    ]
    bench(str(eng), sentences)
