from __future__ import annotations
from typing import Dict, Set, Tuple, List, Iterable
from copy import deepcopy
import re

Grammar = Dict[str, object]  # {"start":str, "N":set[str], "T":set[str], "P":dict[str,set[tuple[str,...]]], "start_candidates":set[str]}

_EPS_NAMES = {"e", "ε", "EPS", "eps", "epsilon"}

def _is_epsilon(body: Tuple[str, ...]) -> bool:
    return len(body) == 0 or (len(body) == 1 and body[0] in _EPS_NAMES)

def _add(P, A, body):
    P.setdefault(A, set()).add(tuple(body))

def _sanitize_terminal(t: str) -> str:
    # Mapear algunos símbolos comunes a nombres legibles
    special = {"(": "LPAREN", ")": "RPAREN", "+": "PLUS", "*": "STAR"}
    if t in special:
        return f"T_{special[t]}"
    # alfanumérico -> mayúsculas y guiones bajos
    name = re.sub(r"[^A-Za-z0-9]+", "_", t).upper()
    if not name:
        name = "TERM"
    return f"T_{name}"

def _clone(G: Grammar) -> Grammar:
    return {
        "start": G["start"],
        "N": set(G["N"]),
        "T": set(G["T"]),
        "P": {A: set(bodies) for A, bodies in G["P"].items()},
        "start_candidates": set(G.get("start_candidates", {G["start"]})),
    }

def remove_epsilon(G: Grammar) -> Grammar:
    G = _clone(G)
    P = G["P"]
    start = G["start"]

    # 1) Encontrar anulables
    nullable: Set[str] = set()
    changed = True
    while changed:
        changed = False
        for A, bodies in P.items():
            if A in nullable:
                continue
            for body in bodies:
                if _is_epsilon(body) or all((X in nullable) for X in body if X in G["N"]):
                    nullable.add(A)
                    changed = True
                    break

    # 2) Agregar nuevas producciones omitiendo anulables
    newP = {A: set() for A in P}
    for A, bodies in P.items():
        for body in bodies:
            if _is_epsilon(body):
                # eliminar ε aquí; solo se reinsertará si A es el start
                continue
            # construir subconjuntos donde se omiten no terminales anulables
            positions = [i for i, X in enumerate(body) if X in nullable]
            # generar combinaciones
            n = len(positions)
            # siempre incluir la versión original
            _add(newP, A, body)
            for mask in range(1, 1 << n):
                b = list(body)
                for bit in range(n - 1, -1, -1):
                    if (mask >> bit) & 1:
                        del b[positions[bit]]
                if len(b) == 0:
                    # A -> ε solo permitido para el símbolo inicial
                    if A == start:
                        _add(newP, A, ())
                else:
                    _add(newP, A, tuple(b))
    G["P"] = newP
    return G

def remove_unit(G: Grammar) -> Grammar:
    G = _clone(G)
    P = G["P"]
    N = G["N"]

    # Cierre de unit-productions
    unit_pairs: Set[Tuple[str, str]] = set()
    for A in N:
        unit_pairs.add((A, A))

    changed = True
    while changed:
        changed = False
        for A in N:
            for body in P.get(A, []):
                if len(body) == 1 and body[0] in N:
                    B = body[0]
                    if (A, B) not in unit_pairs:
                        unit_pairs.add((A, B))
                        changed = True

            # propagar transitivo
            for (_, B) in list(filter(lambda p: p[0] == A, unit_pairs)):
                for C in N:
                    if (B, C) in unit_pairs and (A, C) not in unit_pairs:
                        unit_pairs.add((A, C))
                        changed = True

    # Construir nuevas producciones sin unit
    newP = {A: set() for A in N}
    for A in N:
        for (_, B) in filter(lambda p: p[0] == A, unit_pairs):
            for body in P.get(B, []):
                # saltar unit directas; agregamos solo no-unit o terminales
                if len(body) == 1 and body[0] in N:
                    continue
                _add(newP, A, body)
    G["P"] = newP
    return G

def remove_useless(G: Grammar) -> Grammar:
    G = _clone(G)
    P = G["P"]
    N = G["N"]
    T = G["T"]
    start = G["start"]

    # 1) Generating
    generating: Set[str] = set()
    changed = True
    while changed:
        changed = False
        for A in N:
            if A in generating:
                continue
            for body in P.get(A, []):
                if all((s in T) or (s in generating) for s in body):
                    generating.add(A)
                    changed = True
                    break

    # 2) Filtrar por generating
    P = {A: {b for b in bodies if all((s in T) or (s in generating) for s in b)}
         for A, bodies in P.items() if A in generating}
    N = {A for A in N if A in generating}

    # 3) Reachable
    reachable: Set[str] = {start}
    changed = True
    while changed:
        changed = False
        for A in list(reachable):
            for body in P.get(A, []):
                for s in body:
                    if s in N and s not in reachable:
                        reachable.add(s)
                        changed = True

    P = {A: bodies for A, bodies in P.items() if A in reachable}
    N = {A for A in N if A in reachable}

    G["P"], G["N"] = P, N
    return G

def terminals_to_unaries(G: Grammar) -> Grammar:
    """
    Reemplaza terminales en producciones de longitud>=2 por no terminales nuevos T_x -> x.
    CNF requiere que si la longitud es 2, ambos símbolos sean no terminales.
    """
    G = _clone(G)
    P = G["P"]
    N = G["N"]
    T = G["T"]

    termmap = {}  # terminal -> NT (p.ej. '+' -> T_PLUS)
    def nt_for(t: str) -> str:
        if t not in termmap:
            name = _sanitize_terminal(t)
            # evitar colisiones
            base = name
            k = 0
            while name in N:
                k += 1
                name = f"{base}_{k}"
            termmap[t] = name
            N.add(name)
            _add(P, name, (t,))
        return termmap[t]

    newP = {A: set() for A in N}
    for A, bodies in P.items():
        for body in bodies:
            if len(body) >= 2:
                b2 = []
                for s in body:
                    if s in T:
                        b2.append(nt_for(s))
                    else:
                        b2.append(s)
                _add(newP, A, tuple(b2))
            else:
                _add(newP, A, body)
    G["P"], G["N"] = newP, N
    return G

def binarize(G: Grammar) -> Grammar:
    """
    Convierte producciones de longitud > 2 en cadena binaria A -> X1 N1, N1 -> X2 N2, ..., Nk-2 -> X_{k-1} X_k.
    """
    G = _clone(G)
    P = G["P"]
    N = G["N"]

    counter = 0
    newP = {A: set() for A in N}

    def fresh(A: str) -> str:
        nonlocal counter
        counter += 1
        name = f"{A}_BIN_{counter}"
        while name in N:
            counter += 1
            name = f"{A}_BIN_{counter}"
        N.add(name)
        return name

    for A, bodies in P.items():
        for body in bodies:
            if len(body) <= 2:
                _add(newP, A, body)
            else:
                Xs = list(body)
                head = A
                # encadenar
                while len(Xs) > 2:
                    nxt = fresh(A)
                    _add(newP, head, (Xs[0], nxt))
                    Xs = Xs[1:]
                    head = nxt
                _add(newP, head, tuple(Xs))
    G["P"], G["N"] = newP, N
    return G

def to_cnf_pipeline(G: Grammar) -> Grammar:
    """
    Pipeline: ε-removal -> unit-removal -> useless-removal -> terminals->unaries -> binarize.
    Mantiene S->ε solo si el start era anulable.
    """
    G1 = remove_epsilon(G)
    G2 = remove_unit(G1)
    G3 = remove_useless(G2)
    G4 = terminals_to_unaries(G3)
    G5 = binarize(G4)
    # recalcular T por si aparecieron terminales nuevos en P (no deberían)
    return G5
