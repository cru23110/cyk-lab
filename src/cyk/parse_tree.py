#parse_tree.py
from typing import Dict, Any
from pathlib import Path
from graphviz import Digraph
import time

class Node:
    def __init__(self, sym, left=None, right=None, word=None):
        self.sym = sym; self.left = left; self.right = right; self.word = word

def _build(back: Dict, i: int, j: int, A: str):
    step = back.get((i,j,A))
    if step is None:
        return None
    kind = step[0]
    if kind == "term":
        return Node(A, word=step[1])
    elif kind == "split":
        _, k, B, C = step
        return Node(A, _build(back, i, k, B), _build(back, k, j, C))
    return None

def build_tree(back: Dict, n: int, start_symbol: str):
    return _build(back, 0, n, start_symbol)

def export_tree(root: Node) -> str:
    ts = int(time.time())
    out_dir = Path("outputs/trees"); out_dir.mkdir(parents=True, exist_ok=True)
    gv = Digraph(comment="Parse Tree")
    idx = 0
    def walk(node):
        nonlocal idx
        if node is None: return
        my = f"n{idx}"; idx += 1
        label = node.sym if node.word is None else f"{node.sym}\\n\"{node.word}\""
        gv.node(my, label=label)
        if node.left:
            ch = walk(node.left); gv.edge(my, ch)
        if node.right:
            ch = walk(node.right); gv.edge(my, ch)
        return my
    walk(root)
    path = out_dir / f"tree_{ts}"
    gv.render(str(path), format="png", cleanup=True)
    return str(path.with_suffix(".png"))
