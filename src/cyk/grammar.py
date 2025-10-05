from typing import Dict, Set, Tuple, List

# Representación: dict con conjuntos
# G = {"start": "S", "N": set(), "T": set(), "P": dict[Head, set[BodyTuple]]}
# Bodies: tuplas de símbolos (1 ó 2 en CNF) -> p.ej. ("NP","VP") o ("id",)

def load_grammar(path: str) -> Dict:
    N: Set[str] = set()
    T: Set[str] = set()
    P: Dict[str, Set[Tuple[str, ...]]] = {}
    start = None

    def add(head: str, body_syms: List[str]):
        P.setdefault(head, set()).add(tuple(body_syms))

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Formato tipo: E -> T X | F Y | id
            head, rhs = [p.strip() for p in line.split("->")]
            if start is None:
                start = head
            for alt in rhs.split("|"):
                syms = alt.strip().split()
                add(head, syms)
                # clasificar símbolos elementales (heurística simple)
                for s in syms:
                    if s.islower() or s in {"(", ")", "+", "*", "id"}:
                        T.add(s)
                    else:
                        N.add(s)
            N.add(head)
    return {"start": start, "N": N, "T": T, "P": P, "start_candidates": {start}}
