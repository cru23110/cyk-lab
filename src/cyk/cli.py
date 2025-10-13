# cli.py
import time
import click
from .grammar import load_grammar
from .cnf import to_cnf_pipeline
from .cyk import cyk_parse
from .parse_tree import build_tree, export_tree
from .tokenize import normalize_sentence

@click.command()
@click.option("--grammar", "grammar_path", required=True, help="Ruta a la gramática (texto).")
@click.option("--sentence", "sentence", required=True, help='Frase, ej: "She eats a cake with a fork."')
@click.option("--to-cnf", is_flag=True, help="Convertir la gramática a CNF antes de CYK.")
@click.option("--tree", is_flag=True, help="Exportar árbol sintáctico (PNG si hay Graphviz; .gv si no).")
@click.option("--time", "show_time", is_flag=True, help="Mostrar tiempo de ejecución.")
@click.option("--normalize", is_flag=True, help="Normalizar frase (lowercase, quitar puntuación). Útil para inglés.")
def main(grammar_path, sentence, to_cnf, tree, show_time, normalize):
    G = load_grammar(grammar_path)
    if to_cnf:
        G = to_cnf_pipeline(G)

    tokens = normalize_sentence(sentence) if normalize else sentence.split()

    t0 = time.perf_counter()
    ok, table, back = cyk_parse(G, tokens)
    dt = (time.perf_counter() - t0)

    print("SÍ" if ok else "NO")
    if show_time:
        print(f"Tiempo: {dt*1000:.2f} ms")

    if tree and ok:
        root = build_tree(back, len(tokens), start_symbol=G["start"])
        path = export_tree(root)
        print(f"Árbol exportado a: {path}")

if __name__ == "__main__":
    main()
