# TP8 — Recorridos BFS y DFS

## Objetivo

El grafo de TP7 permite consultar relaciones directas. TP8 permite responder dos
preguntas nuevas sobre relaciones indirectas, integradas en la terminal v6.

## Caso 1: cadena de relaciones entre dos juegos (BFS)

**Pregunta:** ¿cuál es la cadena con menos relaciones que conecta *Elden Ring* con
*Portal 2*? No comparten una arista directa, pero sí existe una cadena:

```text
Opción: 8
Juego de origen: Elden Ring
Juego de destino: Portal 2
Cadena más corta (2 relaciones):
Elden Ring → Minecraft → Portal 2
```

BFS visita primero los juegos a una arista del origen, luego los que están a dos,
y así sucesivamente. Usa una cola (`deque`) y guarda el predecesor de cada juego
descubierto para reconstruir el camino cuando encuentra el destino. Por eso devuelve
un camino con la **menor cantidad de aristas**. Si hay varios caminos igual de cortos,
elige el primero según el orden de inserción de las aristas.

El peso del grafo representa similitud. BFS no minimiza ni maximiza la suma de esos
pesos: aquí cada arista cuenta como un paso. Si no existe conexión devuelve `None`;
si origen y destino coinciden devuelve una lista con ese único juego.

## Caso 2: explorar todos los juegos alcanzables (DFS)

**Pregunta:** ¿qué juegos aparecen si se explora en profundidad la red desde
*Elden Ring*? La opción 9 muestra los alcanzables en orden DFS:

```text
Opción: 9
Juego de origen: Elden Ring
Juegos alcanzables desde 'Elden Ring' (DFS):
 1. Elden Ring
 2. The Legend of Zelda: Breath of the Wild
 3. Hollow Knight
 4. Stardew Valley
 ...
```

DFS toma un vecino, sigue explorando su rama y después vuelve a los demás vecinos.
La implementación usa una pila para evitar el límite de recursión de Python y un
conjunto de visitados para que cada juego aparezca una sola vez. Solo visita la
componente conectada que contiene al juego inicial. En el dataset actual, esa
componente contiene los 25 juegos.

## Cuándo conviene cada recorrido

| Necesidad | Algoritmo | Motivo |
|-----------|-----------|--------|
| Hallar una cadena con menos relaciones | BFS | Explora por distancia en número de aristas. |
| Recorrer todos los juegos alcanzables en profundidad | DFS | Sigue cada rama antes de volver; sirve para explorar la componente. |

Ambos recorren el grafo sin repetir juegos. DFS no garantiza el camino con menos
aristas; BFS sí. Ninguno usa los pesos para optimizar un recorrido.

## Complejidad

Sean `V` los vértices y `E` las aristas de la componente alcanzable.

| Operación | Tiempo | Espacio adicional |
|-----------|--------|-------------------|
| `Grafo.camino_bfs(origen, destino)` | O(V + E) | O(V) para cola y predecesores |
| `Grafo.recorrido_dfs(origen)` | O(V + E) | O(V + E) para pila, visitados y resultado |

En BFS cada vértice entra a la cola una vez y se revisa cada arista de los vértices
alcanzados. En DFS pueden quedar entradas repetidas en la pila cuando varias aristas
apuntan al mismo vértice; cada arista genera como máximo una entrada y cada vértice
se procesa una vez. Por eso ambos tiempos son O(V + E). La lista de adyacencia de
TP7 permite recorrer únicamente los vecinos existentes.

`Catalogo` expone los recorridos mediante `camino_de_relaciones` y `explorar_red`.
La terminal primero busca los títulos en el AVL y luego llama a esos métodos. Si
un título no existe, informa el problema sin iniciar el recorrido.

## Verificación

`tests/test_tp8.py` comprueba que BFS elige menos aristas aunque una arista pese más,
los casos sin camino y con vértices aislados, la visita única de DFS, un camino
indirecto real del catálogo y ambas opciones de la terminal v6.
