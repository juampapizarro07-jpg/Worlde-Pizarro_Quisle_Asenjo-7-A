# Worlde-Pizarro_Quisle_Asenjo-7°A
Juego de Wordle para la terminal, con tres dificultades:

| Dificultad | Letras |
|------------|--------|
| Fácil      | 4      |
| Normal     | 5      |
| Difícil    | 6      |

Cada nivel es una palabra distinta. Tenés 6 intentos para adivinarla.

## Cómo jugar

Necesitás tener Python 3.8 o superior instalado.

### 1. Descargar y preparar el proyecto

1. En GitHub, tocá **Code → Download ZIP** para descargar los archivos del código.
2. Descomprimí el ZIP en una carpeta.
3. Dentro de esa misma carpeta tiene que existir una carpeta llamada `palabras` (si no viene en el ZIP, creala) con los archivos `.txt` de las palabras: `palabras_4.txt`, `palabras_5.txt` y `palabras_6.txt`.
4. Abrí la carpeta general del proyecto desde la plataforma que uses (por ejemplo, VS Code) y ejecutá `wordle.py`. El juego se juega desde la terminal:

```
python wordle.py
```

### 2. Elegir la dificultad

Primero te muestra las dificultades, que se eligen escribiendo el número:

```
1) Fácil (4 letras)
2) Normal (5 letras)
3) Difícil (6 letras)
0) Salir
```

### 3. Elegir el nivel

Después te pregunta qué nivel querés probar. Podés escribir el número que quieras, dentro del rango que te indique, o presionar Enter para que sea al azar.

### 4. Jugar

Comienza el juego. En pantalla se muestran las 6 líneas de intento y un teclado para ver el estado de las letras:

| Color | Significado |
|-------|-------------|
| Verde | La letra es correcta y está en su lugar |
| Amarillo | La letra está en la palabra, pero en otra posición |
| Gris oscuro | La letra no está en la palabra |
| Gris claro | Letra sin usar |

Se puede escribir con o sin tildes (`cancion` = `canción`). La ñ cuenta como una letra más.

### Mensajes del juego

- Si repetís una palabra que ya usaste: `Ya probaste esa palabra.`
- Si la palabra no tiene la cantidad de letras correcta (el número depende de la dificultad): `La palabra debe tener 4 letras (solo letras).`
- Si adivinás la palabra: `¡Ganaste en N intento(s)! La palabra era MODA.`
- Si no la adivinás: `Perdiste. La palabra era MODA.`

Al final de cada partida, ganes o pierdas, te pregunta `¿Jugar otra vez? (s/n):`.

## Estructura

```
wordle.py              juego principal
generarpalabras.py     script auxiliar para armar listas de palabras
palabras/
  palabras_4.txt       respuestas posibles (nivel 1 = primera línea)
  palabras_5.txt
  palabras_6.txt
