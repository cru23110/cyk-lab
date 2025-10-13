# cyk.py
from typing import Dict, List, Tuple, Set, DefaultDict
from collections import defaultdict

def invert_rules(P) -> Tuple[DefaultDict[Tuple[str,...], Set[str]], DefaultDict[str, Set[str]]]:
    bin_map = defaultdict(set)  # (A,B) -> {Head}
    uni_map = defaultdict(set)  # (a)  -> {Head}
    for head, bodies in P.items():
        for body in bodies:
            if len(body) == 2:
                bin_map[tuple(body)].add(head)
            elif len(body) == 1:
                uni_map[body[0]].add(head)
    return bin_map, uni_map

def cyk_parse(G: Dict, words: List[str]) -> Tuple[bool, List[List[Set[str]]], Dict]:
    n = len(words)
    P = G["P"]
    bin_map, uni_map = invert_rules(P)

    # tabla[i][j] = conjunto de variables que generan el span (i, j] (longitud j-i)
    table: List[List[Set[str]]] = [[set() for _ in range(n)] for _ in range(n)]
    back: Dict = {}  # (i,j,Head) -> ("term", w) | ("split", k, B, C)

    # Inicialización (longitud 1)
    for i, w in enumerate(words):
        for A in uni_map.get(w, []):
            table[i][i].add(A)
            back[(i, i+1, A)] = ("term", w)

    # Relleno (longitud >= 2)
    for span in range(2, n+1):
        for i in range(0, n-span+1):
            j = i + span
            cell = table[i][j-1]
            for k in range(i+1, j):
                left = table[i][k-1]
                right = table[k][j-1]
                for B in left:
                    for C in right:
                        for A in bin_map.get((B, C), []):
                            cell.add(A)
                            back[(i, j, A)] = ("split", k, B, C)

    start = G["start"]
    ok = start in table[0][n-1] if n>0 else False
    return ok, table, back
