# TP6 — Montículo máximo y Top 15

## Objetivo y decisión

El sistema necesita mostrar los juegos mejor valorados sin ordenar todos los juegos
cada vez que el usuario consulta el ranking. Para esta primera versión, el equipo toma
`Videojuego.rating` como prioridad: es el puntaje disponible que mejor representa la
valoración general del juego. La popularidad y la personalización no están modeladas
todavía.

Se implementó `MonticuloMaximo` manualmente en
`estructuras/monticulo_maximo.py`, sobre un arreglo dinámico. La estructura no usa
`heapq` ni delega las operaciones de heap a una biblioteca externa. Cuando dos juegos
tienen el mismo rating, se conserva el orden de carga del catálogo.

## Integración

Al cargar o ampliar el catálogo, `Catalogo` construye un montículo máximo a partir de
los juegos usando heapify bottom-up. `Catalogo.top_n(15)` pide al heap los primeros 15
y devuelve una lista en orden de prioridad sin cambiar el heap. La terminal v4 expone
la consulta como **“Ver Top 15 por rating”**. Si el catálogo tiene menos de 15 juegos,
muestra todos; con un catálogo vacío, informa que no hay resultados.

La implementación y sus capas son:

```text
datos/videojuegos.json
        ↓ carga
Catalogo._elementos ── heapify O(n) ──> MonticuloMaximo por rating
        │                                      ↓ mayores(15)
        └──────────────────────────────> Catalogo.top_n(15)
                                               ↓
                                      Terminal v4
```

## Operaciones y complejidad

Sea `n` la cantidad de juegos y `k` la cantidad pedida (en la app, `k ≤ 15`).

| Operación | Complejidad | Motivo |
|-----------|-------------|--------|
| Construir desde los datos (`heapify`) | O(n) | Reacomoda desde los nodos internos hacia la raíz. |
| Insertar un juego | O(log n) | Sube por el árbol hasta recuperar la propiedad de heap. |
| Consultar el máximo | O(1) | El elemento prioritario está en la raíz. |
| Extraer el máximo | O(log n) | Reemplaza la raíz y baja el nuevo valor. |
| Obtener los primeros `k` | O(k log k) | Una cola auxiliar visita solo los candidatos necesarios. |
| Espacio del heap | O(n) | Conserva una entrada por videojuego. |
| Espacio auxiliar para Top-N | O(k) | Mantiene como máximo los candidatos del ranking. |

La extracción Top-N no copia ni ordena el catálogo completo, y tampoco consume el
montículo persistente. La cola auxiliar comienza en la raíz y agrega los hijos de cada
máximo seleccionado; el máximo siguiente necesariamente se encuentra entre esos
candidatos.

## Uso

```text
Opción: 5
Top 15 de videojuegos por rating:
 1. The Legend of Zelda: Breath of the Wild — ⭐ 9.7
 2. Baldur's Gate 3 — ⭐ 9.7
 3. The Witcher 3: Wild Hunt — ⭐ 9.6
...
```

Los empates se resuelven según el orden original de carga. Por eso el resultado es
determinista para el mismo archivo de datos.

## Archivos relacionados

- `estructuras/monticulo_maximo.py`: implementación del montículo binario máximo.
- `servicios/catalogo.py`: construcción del índice y operación `top_n`.
- `ui/terminal.py`: opción de menú y presentación del ranking.
- `docs/04_diagrama_datos.md`: conexión del heap con las otras estructuras.
