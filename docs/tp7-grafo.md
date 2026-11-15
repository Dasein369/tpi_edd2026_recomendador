# TP7 — Grafo de relaciones entre videojuegos

## Objetivo

Hasta TP6 cada juego se consultaba de forma aislada: por título (AVL), por categoría
(árbol general) o por rating (heap). Ninguna estructura responde "¿qué juegos se parecen
a este?". TP7 convierte las relaciones del dominio en una red para consultar juegos similares (RF01, RF05).

## Modelo del grafo

| Decisión | Elección | Justificación |
|----------|----------|---------------|
| **Vértice** | Un vértice = un `Videojuego` | Es la entidad central del dominio; el objeto ya tiene identidad y todos los datos necesarios. Usar el objeto (y no su `id`) evita una tabla auxiliar `id → juego`. |
| **Arista** | Dos juegos están conectados si comparten **género**, **familia de géneros**, **desarrollador** o **tags** | Reutiliza la jerarquía de TP5 y permite relacionar juegos de distintas familias mediante tags comunes. |
| **Dirección** | **No dirigido** | "A se parece a B" implica "B se parece a A": la relación es simétrica. Un grafo dirigido duplicaría la información sin aportar nada. |
| **Peso** | **Pesado**, con la similitud como peso | Dos juegos pueden compartir mucho o poco; sin peso no se podría ordenar las recomendaciones. |
| **Representación** | **Lista de adyacencia** (`dict` de `dict`) | Ver la justificación más abajo. |

### Cómo se calcula el peso

El peso es la suma de los criterios que cumple el par:

| Criterio | Puntos | Motivo |
|----------|--------|--------|
| Mismo género | 3 | La afinidad más fuerte: es lo que un jugador busca al pedir "algo parecido". |
| Mismo desarrollador | 2 | Estilo y calidad suelen repetirse dentro de un mismo estudio. |
| Misma familia, distinto género | 1 | Afinidad débil: pertenecen a la misma rama de la jerarquía de TP5. |
| Cada tag compartido | 1 | Afinidad adicional, incluso entre juegos de familias distintas. |

El mismo género y la misma familia no se suman: el género ya implica la familia. Los
tags sí se suman a los demás criterios. Por ejemplo, *Elden Ring* y *Dark Souls III*
pesan 7 (3 por género, 2 por estudio y 2 por tags). Un par sin nada en común no tiene arista.

Los pesos son una decisión de diseño del equipo, no una medida objetiva; viven como
constantes en `servicios/relaciones.py` y se pueden ajustar sin tocar el grafo. Los
tags del catálogo de prueba son una selección manual para los 25 juegos.

### Por qué se incluye la familia

Se midió el grafo sobre `datos/videojuegos.json` (25 juegos) con y sin ese criterio:

| Criterio | Aristas | Densidad | Juegos aislados |
|----------|---------|----------|-----------------|
| Género, desarrollador y tags | 82 | 0,27 | 0 |
| Género, desarrollador, tags y familia | 132 | 0,44 | 0 |

Los tags conectan juegos de familias distintas y evitan vértices aislados en este
catálogo. La familia aporta 50 aristas más entre géneros hermanos.

### Representación: lista de adyacencia

La densidad medida es 0,44: de cada 100 pares posibles, 44 están conectados. Con 25
juegos la matriz ocuparía 625 celdas para guardar 264 entradas útiles (2 por arista). Se
eligió lista de adyacencia por estos motivos:

- **Espacio:** O(V + E) frente a O(V²) de la matriz.
- **Vecinos:** listar los vecinos de un juego cuesta O(grado) y no O(V). Es la consulta
  que más se usa (relacionados, y BFS/DFS en TP8, que recorren O(V + E) en vez de O(V²)).
- **Vértices como objetos:** el diccionario admite `Videojuego` como clave directa; la
  matriz exigiría asignar un índice entero a cada juego y mantener esa correspondencia.
- **Catálogo dinámico:** agregar un vértice no obliga a redimensionar nada.

En el catálogo de demostración la densidad es 0,44. La familia y los tags aumentan la
conectividad, por lo que la cantidad de aristas puede crecer cuadráticamente según los
datos. La lista de adyacencia conserva acceso O(1) a una arista y permite recorrer vecinos
en proporción al grado; su costo espacial es O(V + E). Para ampliar el catálogo, la
construcción puede optimizarse agrupando juegos por atributos compartidos y evaluando solo
los pares candidatos.

## Operaciones y complejidad

Sea `V` la cantidad de juegos, `E` la de aristas, `d` el grado de un vértice y `t`
la cantidad total de tags de los dos juegos comparados.

| Operación | Complejidad | Motivo |
|-----------|-------------|--------|
| Agregar vértice o arista | O(1) | Inserción en diccionarios. |
| `tiene_arista`, `peso`, `grado` | O(1) | Búsqueda por clave. |
| `vecinos(v)` | O(d) | Copia el diccionario del vértice. |
| Recorrer todas las aristas | O(V + E) | Cada arista se emite una sola vez. |
| Construir el grafo desde el catálogo | O(V² (1 + t log(t+1))) | Compara cada par una vez y ordena los tags compartidos; se paga al cargar. |
| `Catalogo.relacion_entre(a, b)` | O(1 + t log(t+1)) | Consulta la arista y recalcula los motivos de un par. |
| `Catalogo.juegos_relacionados(v)` | O(d log(d+1) + d t log(t+1)) | Ordena los vecinos y recalcula sus motivos, sin recorrer el catálogo. |
| Espacio del grafo | O(V + E) | Una entrada por vértice y dos por arista. |

La construcción es aceptable para este catálogo. Para catálogos mucho mayores
convendría agrupar los juegos por género, desarrollador y tag, y comparar solo pares
que compartan alguna de esas claves o la misma familia.

## Consultas de ejemplo

Salidas reales de la terminal v5 con el dataset del repositorio:

```text
Opción: 6
Título del videojuego: elden ring
Juegos relacionados con 'Elden Ring':
- Dark Souls III — similitud 7 (mismo género (RPG), mismo desarrollador (FromSoftware), tags compartidos (difícil, fantasía oscura))
- The Witcher 3: Wild Hunt — similitud 4 (mismo género (RPG), tags compartidos (mundo abierto))
- Baldur's Gate 3 — similitud 3 (mismo género (RPG))
- Undertale — similitud 3 (mismo género (RPG))
- The Legend of Zelda: Breath of the Wild — similitud 1 (tags compartidos (mundo abierto))
- Red Dead Redemption 2 — similitud 1 (tags compartidos (mundo abierto))
- Hollow Knight — similitud 1 (tags compartidos (difícil))
- Celeste — similitud 1 (tags compartidos (difícil))
- Minecraft — similitud 1 (tags compartidos (mundo abierto))
- Civilization VI — similitud 1 (misma familia (Rol y estrategia))
```

```text
Opción: 7
Primer título: elden ring
Segundo título: dark souls iii
'Elden Ring' y 'Dark Souls III' están relacionados (similitud 7):
- mismo género (RPG)
- mismo desarrollador (FromSoftware)
- tags compartidos (difícil, fantasía oscura)
```

```text
Opción: 7
Primer título: elden ring
Segundo título: portal 2
'Elden Ring' y 'Portal 2' no tienen relación directa.
```

Para repetir la medición de la red:

```python
from servicios.catalogo import Catalogo

catalogo = Catalogo()
catalogo.cargar_desde_json("datos/videojuegos.json")
print(catalogo.resumen_red())  # {'vertices': 25, 'aristas': 132, 'densidad': 0.44}
```

## Integración

```text
datos/videojuegos.json
        ↓ carga
Catalogo._elementos ── construir_grafo, O(V² (1 + t log(t+1))) ──> Grafo[Videojuego]
        │                                              ↓ vecinos / peso
        └─────────────────────────────> Catalogo.juegos_relacionados / relacion_entre
                                                       ↓
                                              Terminal v5 (opciones 6 y 7)
```

`Catalogo` construye el grafo al cargar los datos, junto con el AVL, el árbol general y el
heap. Como en las demás estructuras, el grafo nuevo se arma completo antes de reemplazar
el anterior: si un registro es inválido, el catálogo no queda a medias.

La regla de negocio (qué significa "relacionados") está en `servicios/relaciones.py` y
la estructura (`estructuras/grafo.py`) no conoce nada del dominio, así que se puede
probar y reutilizar por separado.

## Alcance de esta etapa y continuidad

- **Relaciones directas e indirectas.** TP7 permite consultar vecinos y comparar dos
  juegos. TP8 amplía esas consultas con BFS para hallar una cadena con menos aristas y
  DFS para explorar todos los juegos alcanzables.
- **Datos de demostración.** El catálogo actual contiene 25 juegos con tags seleccionados
  para ilustrar los criterios de relación. Una fuente ampliada debe conservar el modelo
  de datos y normalizar los atributos antes de construir el grafo.
- **Criterio de similitud.** Los pesos reflejan la regla de negocio acordada por el equipo
  y están centralizados en `servicios/relaciones.py` para facilitar su ajuste.
- **Recomendación (RF01).** `juegos_relacionados` muestra candidatos para el título ingresado, ordenados por similitud y rating.

## Archivos relacionados

- `estructuras/grafo.py`: grafo no dirigido y pesado con lista de adyacencia.
- `servicios/relaciones.py`: criterio de similitud, `Relacion` y construcción del grafo.
- `servicios/catalogo.py`: integración (`juegos_relacionados`, `relacion_entre`, `resumen_red`).
- `ui/terminal.py`: opciones 6 y 7 de la terminal v5.
- `tests/test_tp7.py`: pruebas del grafo, las relaciones y la terminal.

