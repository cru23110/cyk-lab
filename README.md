### Proyecto: Implementación del Algoritmo CYK y Simplificación de Gramáticas

## Descripción General

Este proyecto implementa el algoritmo CYK (Cocke–Younger–Kasami) para análisis
sintáctico de cadenas en un lenguaje formal, junto con los algoritmos de 
simplificación de gramáticas que permiten convertir una gramática libre de contexto
(CFG) en su Forma Normal de Chomsky (CNF).

El sistema admite:

    - Carga de gramáticas desde archivos de texto.

    - Conversión automática a CNF mediante un pipeline de simplificación.

    - Análisis de frases o expresiones para determinar si pertenecen al lenguaje.

    - Construcción y exportación del árbol sintáctico.

    - Ejecución de pruebas automáticas y benchmarks de rendimiento

### Video del funcionamiento

    https://youtu.be/oaSg_GQlzBY

### Instalación y Ejecución

## Crear y activar entorno virtual

    py -m venv .venv
    source .venv/bin/activate        ( Linux / Mac)
    .venv\Scripts\activate           ( Windows)
    pip install -r requirements.txt

## Ejecución
    
    Ejecutar el módulo cli.py desde la raíz del proyecto:

    python -m src.cyk.cli --grammar data/grammars/english-cnf.txt --sentence "She eats a cake with a fork." --normalize --tree --time

    # Estructura de la entrada

    python -m src.cli --grammar data/grammars/1-cnf.txt --sentence "id + id * id" --tree --time

    | Parámetro    | Descripción                                                               |
    |--------------|---------------------------------------------------------------------------|
    | `--grammar`  | Ruta al archivo de gramática                                              |
    | `--sentence` | Frase o expresión a analizar                                              |
    | `--to-cnf`   | Convierte la gramática a CNF antes de ejecutar                           |
    | `--tree`     | Genera el árbol sintáctico                                               |
    | `--time`     | Muestra el tiempo de ejecución                                           |
    | `--normalize`| Normaliza la frase (útil para inglés)                                    |

# También se puede ejecutar
    
    bash scripts/run.sh

    - Activa el entorno virtual automáticamente.
    - Analiza una expresión aritmética y una oración en inglés.
    - Muestra los tiempos de ejecución y genera los árboles sintácticos.

# Para evaluar el rendimiento ejecutar

    python scripts/benchmark.py

    o también -> python -m scripts.benchmark   

    - Imprimirá los tiempos promedio de análisis para cada oración de prueba.

## Ejecución de pruebas

    pip install pytest

    # Para ejecutar todas las pruebas
    python -m pytest -q


## Estructura del proyecto

cyk-lab/
├── data/
│   ├── grammars/
│   ├── 1-cnf.txt
│   ├── 1.txt
│   ├── english-cnf.txt
│   ├── english.txt
│   └── examples/
│       └── sentences.txt
├── scripts/
│   ├── benchmark.py
│   └── run.sh
├── src/
├── cyk/
│   ├── __init__.py
│   ├── cli.py
│   ├── cnf.py
│   ├── cyk.py
│   ├── grammar.py
│   ├── parse_tree.py
│   └── tokenize.py
├── tests/
│   ├── test_cnf.py
│   ├── test_cyk.py
│   ├── test_english.py
│   └── test_grammar.py
└── requirements.txt


### Descripción de la estructura:

- data/: Contiene gramáticas y ejemplos para el algoritmo CYK

    - grammars/: Directorio para archivos de gramáticas

        - Archivos de gramáticas (1-cnf.txt, 1.txt, english-cnf.txt, english.txt)

    - examples/: Ejemplos de oraciones para probar

        -sentences.txt: Archivo con oraciones de ejemplo

- scripts/: Scripts utilitarios

    - benchmark.py: Para medir el rendimiento del algoritmo

    - run.sh: Script de ejecución

- src/: Código fuente principal del proyecto

    - Módulos para el algoritmo CYK, gramáticas, árboles de análisis, etc.

- tests/: Pruebas unitarias para los diferentes módulos

- requirements.txt: Dependencias del proyecto


