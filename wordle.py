#!/usr/bin/env python3
"""Wordle en español con tres dificultades (4, 5 y 6 letras).

Las palabras se leen de la carpeta "palabras/":
  - palabras_N.txt : posibles respuestas, de la más común (nivel 1) a la menos común.
  - validas_N.txt  : (opcional) palabras aceptadas como intento. Si no existe,
                     se acepta cualquier combinación de letras del largo correcto.
"""

import os
import random
import sys
import unicodedata
from collections import Counter
from pathlib import Path

CARPETA = Path(__file__).resolve().parent / "palabras"
INTENTOS = 6
DIFICULTADES = {"1": ("Fácil", 4), "2": ("Normal", 5), "3": ("Difícil", 6)}
FILAS_TECLADO = ["qwertyuiop", "asdfghjklñ", "zxcvbnm"]

# Colores ANSI (fondo + texto)
ESTILOS = {
    "verde": "\033[1;30;42m",
    "amarillo": "\033[1;30;43m",
    "gris": "\033[1;97;100m",
    None: "\033[30;47m",  # letra sin usar
}
RESET = "\033[0m"
PRIORIDAD = {None: 0, "gris": 1, "amarillo": 2, "verde": 3}


# ---------------------------------------------------------------- utilidades
def normalizar(texto):
    """Pasa a minúsculas y quita tildes, pero conserva la ñ."""
    texto = unicodedata.normalize("NFC", texto.strip().lower())
    texto = texto.replace("ñ", "\0")
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.replace("\0", "ñ")


def limpiar():
    print("\033[2J\033[H", end="")


def leer_lineas(ruta):
    with open(ruta, encoding="utf-8") as f:
        return [linea.strip() for linea in f if linea.strip()]


def cargar_respuestas(largo):
    """Devuelve la lista de respuestas (con tildes) ordenada por nivel."""
    ruta = CARPETA / f"palabras_{largo}.txt"
    if not ruta.exists():
        return []
    vistas, resultado = set(), []
    for palabra in leer_lineas(ruta):
        n = normalizar(palabra)
        if len(n) == largo and n.isalpha() and n not in vistas:
            vistas.add(n)
            resultado.append(palabra.lower())
    return resultado


def cargar_validas(largo, respuestas):
    """Conjunto de intentos válidos, o None si no hay lista (se acepta todo)."""
    ruta = CARPETA / f"validas_{largo}.txt"
    if not ruta.exists():
        return None
    validas = {normalizar(p) for p in leer_lineas(ruta)}
    validas.update(normalizar(p) for p in respuestas)
    return validas


# -------------------------------------------------------------------- lógica
def evaluar(secreta, intento):
    """Devuelve una lista con 'verde', 'amarillo' o 'gris' por cada letra.

    Se hace en dos pasadas para tratar bien las letras repetidas:
    primero los verdes, y luego los amarillos solo mientras queden
    letras sin emparejar en la palabra secreta.
    """
    colores = ["gris"] * len(secreta)
    restantes = Counter()
    for i, (s, g) in enumerate(zip(secreta, intento)):
        if s == g:
            colores[i] = "verde"
        else:
            restantes[s] += 1
    for i, g in enumerate(intento):
        if colores[i] != "verde" and restantes[g] > 0:
            colores[i] = "amarillo"
            restantes[g] -= 1
    return colores


def actualizar_teclado(teclado, intento, colores):
    for letra, color in zip(intento, colores):
        if PRIORIDAD[color] > PRIORIDAD[teclado.get(letra)]:
            teclado[letra] = color


# ------------------------------------------------------------------- pantalla
def casilla(letra, color):
    return f"{ESTILOS[color]} {letra.upper()} {RESET}"


def dibujar(intentos, largo, teclado, titulo, mensaje):
    limpiar()
    print(f"  W O R D L E   -   {titulo}\n")
    for fila in range(INTENTOS):
        if fila < len(intentos):
            palabra, colores = intentos[fila]
            celdas = [casilla(l, c) for l, c in zip(palabra, colores)]
        else:
            celdas = [" · "] * largo
        print("   " + " ".join(celdas) + "\n")
    for i, fila in enumerate(FILAS_TECLADO):
        sangria = " " * (3 + i * 2)
        print(sangria + "".join(casilla(l, teclado.get(l)) for l in fila))
    print()
    if mensaje:
        print(f"  {mensaje}\n")


# --------------------------------------------------------------------- menús
def pedir(texto):
    try:
        return input(texto).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n¡Hasta la próxima!")
        sys.exit(0)


def elegir_dificultad():
    limpiar()
    print("  W O R D L E   en español\n")
    for clave, (nombre, largo) in DIFICULTADES.items():
        print(f"   {clave}) {nombre} ({largo} letras)")
    print("   0) Salir\n")
    while True:
        opcion = pedir("  Elegí la dificultad: ")
        if opcion == "0":
            print("¡Hasta la próxima!")
            sys.exit(0)
        if opcion in DIFICULTADES:
            return DIFICULTADES[opcion]
        print("  Opción no válida.")


def elegir_nivel(total):
    while True:
        texto = pedir(f"  Nivel (1-{total}) o Enter para uno al azar: ")
        if texto == "":
            return random.randrange(total)
        if texto.isdigit() and 1 <= int(texto) <= total:
            return int(texto) - 1
        print(f"  Escribí un número entre 1 y {total}.")


# --------------------------------------------------------------------- juego
def jugar_ronda(nombre, largo, respuestas, validas):
    indice = elegir_nivel(len(respuestas))
    original = respuestas[indice]
    secreta = normalizar(original)
    titulo = f"{nombre} - nivel {indice + 1}"

    intentos, teclado, mensaje = [], {}, ""
    while len(intentos) < INTENTOS:
        dibujar(intentos, largo, teclado, titulo, mensaje)
        mensaje = ""
        intento = normalizar(pedir(f"  Intento {len(intentos) + 1}/{INTENTOS}: "))

        if len(intento) != largo or not intento.isalpha():
            mensaje = f"La palabra debe tener {largo} letras (solo letras)."
            continue
        if validas is not None and intento not in validas:
            mensaje = "Esa palabra no está en el diccionario."
            continue
        if any(intento == p for p, _ in intentos):
            mensaje = "Ya probaste esa palabra."
            continue

        colores = evaluar(secreta, intento)
        intentos.append((intento, colores))
        actualizar_teclado(teclado, intento, colores)

        if intento == secreta:
            fin = f"¡Ganaste en {len(intentos)} intento(s)! La palabra era {original.upper()}."
            dibujar(intentos, largo, teclado, titulo, fin)
            return

    dibujar(intentos, largo, teclado, titulo,
            f"Perdiste. La palabra era {original.upper()}.")


def main():
    os.system("")  # activa los colores ANSI en la consola de Windows
    while True:
        nombre, largo = elegir_dificultad()
        respuestas = cargar_respuestas(largo)
        if not respuestas:
            print(f"\n  No encontré palabras de {largo} letras en: {CARPETA}")
            print("  Revisá que exista el archivo palabras_%d.txt." % largo)
            pedir("\n  Enter para volver al menú...")
            continue
        validas = cargar_validas(largo, respuestas)
        jugar_ronda(nombre, largo, respuestas, validas)
        if pedir("  ¿Jugar otra vez? (s/n): ").lower() not in ("s", "si", "sí"):
            print("¡Hasta la próxima!")
            break


if __name__ == "__main__":
    main()