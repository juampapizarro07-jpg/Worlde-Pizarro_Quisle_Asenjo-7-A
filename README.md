# Worlde-Pizarro_Quisle_Asenjo-7-A
# Wordle en español

Juego de Wordle para la terminal, con tres dificultades:

| Dificultad | Letras |
|------------|--------|
| Fácil      | 4      |
| Normal     | 5      |
| Difícil    | 6      |

Cada dificultad tiene hasta 2000 niveles. El nivel 1 es la palabra más común y el 2000 la menos común.
Tenés 6 intentos. Verde = letra en su lugar, amarillo = está en otro lugar, gris = no está.

## Cómo jugar

Necesitás Python 3.8 o superior. Desde la carpeta del proyecto:

```
python wordle.py
```

Se puede escribir con o sin tildes (`cancion` = `canción`). La ñ cuenta como una letra más.

## Estructura

```
wordle.py              juego principal
generar_palabras.py    arma las listas de 2000 palabras por dificultad
palabras/
  palabras_4.txt       respuestas posibles (nivel 1 = primera línea)
  palabras_5.txt
  palabras_6.txt
  validas_N.txt        (opcional) palabras aceptadas como intento
  excluir.txt          (opcional) palabras a descartar al generar
```

## Generar las 2000 palabras por dificultad

El repositorio trae una lista corta de ejemplo. Para tener 2000 palabras por dificultad:

1. Descargá `es_50k.txt` de [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords) (carpeta `content/2018/es/`).
2. Ejecutá:

   ```
   python generar_palabras.py es_50k.txt
   ```

Esa lista sale de subtítulos, así que conviene revisar las palabras y agregar al archivo `palabras/excluir.txt` las que no sirvan (nombres propios, groserías, palabras raras) y volver a ejecutar el script.

## Créditos

Lista de frecuencias: [FrequencyWords](https://github.com/hermitdave/FrequencyWords) de Hermit Dave (licencia MIT), basada en OpenSubtitles.
 
