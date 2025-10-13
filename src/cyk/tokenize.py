# tokenize.py
import re
from typing import List

_PUNCT = re.compile(r"[.,!?;:]")

def normalize_sentence(s: str) -> List[str]:
    """
    Normaliza frases en inglés simples:
    - lowercase
    - elimina .,!?;:
    - separa por espacios
    """
    s = s.strip().lower()
    s = _PUNCT.sub(" ", s)
    tokens = [t for t in s.split() if t]
    return tokens
