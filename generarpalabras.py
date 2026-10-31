#!/usr/bin/env python3
"""Genera las listas de palabras del Wordle a partir de una lista de frecuencias.

Uso:
    python generar_palabras.py es_50k.txt

El archivo de entrada puede tener el formato "palabra frecuencia" (una por línea,
de la más común a la menos común) o solo una palabra por línea ya ordenada.

Crea en la carpeta "palabras/":
  - palabras_N.txt : las 2000 palabras más comunes de N letras (niveles 1-2000).
  - validas_N.txt  : todas las palabras de N letras encontradas (para aceptar intentos).

Opcional: si existe "palabras/excluir.txt" (una palabra por línea), esas palabras
se descartan. Sirve para sacar nombres propios, groserías, palabras raras, etc.
"""

import re
import sys
from pathlib import Path

from wordle import normalizar

LARGOS = (4, 5, 6)
CANTIDAD = 2000
CARPETA = Path(__file__).resolve().parent / "palabras"
SOLO_LETRAS = re.compile(r"^[a-záéíóúüñ]+$")


def leer_excluidas():
    ruta = CARPETA / "excluir.txt"
    if not ruta.exists():
        return set()
    with open(ruta, encoding="utf-8") as f:
        return {normalizar(l) for l in f if l.strip()}


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    excluidas = leer_excluidas()
    por_largo = {n: [] for n in LARGOS}
    vistas = {n: set() for n in LARGOS}

    with open(sys.argv[1], encoding="utf-8") as f:
        for linea in f:
            partes = linea.split()
            if not partes:
                continue
            palabra = partes[0].lower()
            if not SOLO_LETRAS.match(palabra):
                continue
            norm = normalizar(palabra)
            n = len(norm)
            if n not in por_largo or norm in vistas[n] or norm in excluidas:
                continue
            vistas[n].add(norm)
            por_largo[n].append(palabra)

    CARPETA.mkdir(exist_ok=True)
    for n in LARGOS:
        palabras = por_largo[n]
        respuestas = palabras[:CANTIDAD]
        (CARPETA / f"palabras_{n}.txt").write_text("\n".join(respuestas) + "\n", encoding="utf-8")
        (CARPETA / f"validas_{n}.txt").write_text("\n".join(palabras) + "\n", encoding="utf-8")
        aviso = "" if len(respuestas) == CANTIDAD else f"  <- faltan {CANTIDAD - len(respuestas)}, usá una lista más grande"
        print(f"{n} letras: {len(respuestas)} respuestas, {len(palabras)} válidas{aviso}")


if __name__ == "__main__":
    main()