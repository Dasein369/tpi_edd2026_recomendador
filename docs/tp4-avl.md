# TP4 — AVL frente al BST desbalanceado

## 1. El problema: la forma del BST depende del orden de inserción

El BST de TP3 no se reorganiza: cada título nuevo cuelga de la hoja que le toca y ahí
queda. Si los títulos llegan ya ordenados, cada nuevo es mayor que todos los anteriores
y siempre baja por la derecha: el árbol se convierte en una **lista enlazada** de altura
`n`. La búsqueda pasa de `O(log n)` a `O(n)` y construir el árbol pasa de `O(n log n)` a
`O(n²)`.

No es un caso exótico. Un catálogo exportado alfabéticamente, una base ordenada por
título o un archivo que ya viene ordenado producen exactamente esta entrada.

```
Insertar A, B, C, D, E (en ese orden)

BST (TP3)                    AVL (TP4)

A                                B
 \                              / \
  B                            A   D
   \                            / \
    C                          C   E
     \
      D          altura 5               altura 3
       \
        E
```

## 2. Escenarios de desbalance generados

`experimentos/benchmark_tp4.py` arma cinco órdenes de inserción para el mismo conjunto
de títulos únicos (construidos a partir de `datos/videojuegos.json`):

- **ascendente**: Títulos ya ordenados de la A a la Z (catálogo exportado alfabéticamente).
- **descendente**: Títulos ordenados de la Z a la A.
- **zigzag**: Se alterna el menor y el mayor que quedan: A, Z, B, Y, C, X…
- **casi_ordenado**: Ordenados, con el 5 % de los títulos intercambiados con un vecino cercano.
- **aleatorio**: Orden mezclado con semilla fija (caso favorable, grupo de control).

## 3. AVL: invariante y rotaciones

Un árbol AVL es un BST que cumple, **en cada nodo**, que las alturas de sus subárboles
izquierdo y derecho difieren a lo sumo en 1. El *factor de balance*
`altura(izq) − altura(der)` solo puede valer −1, 0 o +1. La altura de cada subárbol se
guarda en el nodo (`NodoAVL.altura`), así que calcular el balance cuesta `O(1)`.

Tras insertar, se vuelve por el camino hacia la raíz actualizando alturas. El primer
nodo cuyo factor llega a ±2 se corrige con una rotación, que reordena unos pocos
enlaces en `O(1)` **sin alterar el orden inorder** (el árbol sigue siendo un BST válido).
Hay cuatro casos:

| Caso | Se detecta cuando | Corrección |
|---|---|---|
| Izquierda-izquierda | factor del nodo = +2 y de su hijo izquierdo ≥ 0 | rotación simple a la derecha |
| Derecha-derecha | factor del nodo = −2 y de su hijo derecho ≤ 0 | rotación simple a la izquierda |
| Izquierda-derecha | factor del nodo = +2 y de su hijo izquierdo < 0 | rotación izquierda del hijo, luego derecha del nodo |
| Derecha-izquierda | factor del nodo = −2 y de su hijo derecho > 0 | rotación derecha del hijo, luego izquierda del nodo |

```
Rotación simple a la derecha (LL)          Rotación doble izquierda-derecha (LR)

      y               x                      z             z               y
     / \             / \                    /             /              /   \
    x   C    -->    A   y                  x      -->    y      -->     x     z
   / \                 / \                  \            /
  A   B               B   C                  y          x
```

Una inserción provoca como máximo una corrección (simple o doble), pero se revisa el
balance en todos los nodos del camino de vuelta: `O(log n)` en total.

Implementación: `estructuras/arbol_avl.py`, con `_rotar_derecha`, `_rotar_izquierda` y
`_rebalancear`. El método `es_valido()` recalcula todo el árbol desde cero y se usa en
las pruebas para verificar el invariante tras cada inserción.

### Decisiones de diseño

- **Misma interfaz que el BST** (`insertar`, `buscar`, recorridos, `altura`, `len`),
  por lo que el catálogo cambió de estructura modificando solo la línea que la crea.
  `Catalogo.buscar()` ahora consulta el AVL.
- **Títulos repetidos.** Se desempata por orden de inserción, lo que da un orden total y
  estable que las rotaciones no alteran. `buscar` devuelve siempre el primer título
  insertado, igual que el BST de TP3. Esto mantiene válidas las pruebas de carga
  repetida de TP3.
- **Comparación idéntica** a la del BST (`casefold()` en cada paso) para que el
  experimento compare formas de árbol y no detalles de implementación.

## 4. Complejidad teórica

Sea `n` la cantidad de videojuegos y `h` la altura del árbol.

| Operación | BST (TP3) | AVL (TP4) |
|---|---:|---:|
| Altura | entre ⌈log₂(n+1)⌉ y n | siempre ≤ 1,44·log₂(n+2) |
| Buscar | O(h): O(log n) promedio, **O(n) peor caso** | **O(log n) garantizado** |
| Insertar | O(h): O(log n) promedio, **O(n) peor caso** | **O(log n) garantizado** |
| Construir con n inserciones | O(n log n) promedio, **O(n²) peor caso** | **O(n log n) garantizado** |
| Rotaciones por inserción | no tiene | O(1) amortizado, máximo 2 |
| Espacio | O(n) | O(n) (un entero extra por nodo) |

## 5. Resultados

Cada escenario se mide con `n` = 100, 1.000, 5.000, 10.000 títulos. Las
búsquedas usan una muestra fija de 500 títulos existentes elegidos al
azar; los pasos son nodos visitados (comparaciones). Los tiempos son la mediana de
5 tandas (la construcción, de 3 repeticiones hasta 1.000 elementos y 1 en
adelante) y dependen del equipo.

### 5.1 Altura

La altura mínima posible para `n` nodos es ⌈log₂(n+1)⌉. La última columna es el máximo
que la teoría permite a un AVL.

| Escenario | Elementos | Altura mínima | Altura BST | Altura AVL | Cota AVL |
|---|---:|---:|---:|---:|---:|
| ascendente | 100 | 7 | 100 | 7 | 9 |
| descendente | 100 | 7 | 100 | 7 | 9 |
| zigzag | 100 | 7 | 100 | 8 | 9 |
| casi_ordenado | 100 | 7 | 74 | 7 | 9 |
| aleatorio | 100 | 7 | 12 | 8 | 9 |
| ascendente | 1.000 | 10 | 1000 | 10 | 14 |
| descendente | 1.000 | 10 | 1000 | 10 | 14 |
| zigzag | 1.000 | 10 | 1000 | 12 | 14 |
| casi_ordenado | 1.000 | 10 | 786 | 11 | 14 |
| aleatorio | 1.000 | 10 | 25 | 12 | 14 |
| ascendente | 5.000 | 13 | 5000 | 13 | 17 |
| descendente | 5.000 | 13 | 5000 | 13 | 17 |
| zigzag | 5.000 | 13 | 5000 | 15 | 17 |
| casi_ordenado | 5.000 | 13 | 3817 | 13 | 17 |
| aleatorio | 5.000 | 13 | 30 | 15 | 17 |
| ascendente | 10.000 | 14 | 10000 | 14 | 18 |
| descendente | 10.000 | 14 | 10000 | 14 | 18 |
| zigzag | 10.000 | 14 | 10000 | 17 | 18 |
| casi_ordenado | 10.000 | 14 | 7655 | 14 | 18 |
| aleatorio | 10.000 | 14 | 31 | 16 | 18 |

### 5.2 Búsqueda

| Escenario | Elementos | Pasos prom. BST | Pasos prom. AVL | BST (ns/búsqueda) | AVL (ns/búsqueda) | BST / AVL |
|---|---:|---:|---:|---:|---:|---:|
| ascendente | 100 | 50,5 | 6,7 | 5.422,5 | 930,4 | 5,8× |
| descendente | 100 | 50,5 | 6,7 | 5.689,9 | 1.063,5 | 5,4× |
| zigzag | 100 | 50,5 | 7,0 | 5.490,6 | 991,2 | 5,5× |
| casi_ordenado | 100 | 38,9 | 6,7 | 4.323,8 | 870,6 | 5,0× |
| aleatorio | 100 | 7,5 | 6,8 | 897,5 | 916,0 | 1,0× |
| ascendente | 1.000 | 498,8 | 10,0 | 59.205,9 | 2.228,7 | 26,6× |
| descendente | 1.000 | 502,2 | 10,0 | 52.191,6 | 1.672,7 | 31,2× |
| zigzag | 1.000 | 490,8 | 10,3 | 61.800,2 | 1.389,2 | 44,5× |
| casi_ordenado | 1.000 | 389,7 | 10,1 | 60.334,9 | 1.605,2 | 37,6× |
| aleatorio | 1.000 | 12,8 | 10,2 | 1.703,2 | 1.378,1 | 1,2× |
| ascendente | 5.000 | 2.451,2 | 12,4 | 420.520,2 | 2.924,7 | 143,8× |
| descendente | 5.000 | 2.549,8 | 12,4 | 346.581,8 | 2.060,6 | 168,2× |
| zigzag | 5.000 | 2.491,1 | 12,8 | 425.872,9 | 1.717,5 | 248,0× |
| casi_ordenado | 5.000 | 1.894,1 | 12,4 | 299.931,9 | 1.946,0 | 154,1× |
| aleatorio | 5.000 | 15,5 | 12,5 | 2.229,2 | 1.840,3 | 1,2× |
| ascendente | 10.000 | 5.201,5 | 13,4 | 857.305,0 | 1.748,4 | 490,3× |
| descendente | 10.000 | 4.799,5 | 13,3 | 704.521,9 | 1.839,0 | 383,1× |
| zigzag | 10.000 | 5.049,1 | 13,8 | 985.210,9 | 1.825,1 | 539,8× |
| casi_ordenado | 10.000 | 3.973,6 | 13,5 | 665.632,9 | 2.112,3 | 315,1× |
| aleatorio | 10.000 | 16,2 | 13,6 | 2.180,8 | 2.486,1 | 0,9× |

### 5.3 Construcción

| Escenario | Elementos | Construir BST (ms) | Construir AVL (ms) | Rotaciones AVL | Rotaciones por inserción |
|---|---:|---:|---:|---:|---:|
| ascendente | 100 | 0,64 | 0,51 | 93 | 0,93 |
| descendente | 100 | 0,62 | 0,55 | 93 | 0,93 |
| zigzag | 100 | 0,64 | 0,78 | 149 | 1,49 |
| casi_ordenado | 100 | 0,42 | 0,51 | 103 | 1,03 |
| aleatorio | 100 | 0,11 | 0,45 | 59 | 0,59 |
| ascendente | 1.000 | 58,42 | 7,48 | 990 | 0,99 |
| descendente | 1.000 | 79,48 | 7,09 | 990 | 0,99 |
| zigzag | 1.000 | 63,92 | 13,50 | 1.605 | 1,60 |
| casi_ordenado | 1.000 | 88,78 | 14,38 | 1.029 | 1,03 |
| aleatorio | 1.000 | 1,74 | 7,14 | 694 | 0,69 |
| ascendente | 5.000 | 1.529,95 | 46,30 | 4.987 | 1,00 |
| descendente | 5.000 | 1.604,28 | 45,33 | 4.987 | 1,00 |
| zigzag | 5.000 | 1.568,67 | 61,14 | 8.098 | 1,62 |
| casi_ordenado | 5.000 | 1.295,36 | 40,79 | 5.242 | 1,05 |
| aleatorio | 5.000 | 15,44 | 57,42 | 3.466 | 0,69 |
| ascendente | 10.000 | 9.738,19 | 141,15 | 9.986 | 1,00 |
| descendente | 10.000 | 7.951,11 | 102,64 | 9.986 | 1,00 |
| zigzag | 10.000 | 9.585,36 | 179,42 | 16.221 | 1,62 |
| casi_ordenado | 10.000 | 5.802,09 | 99,34 | 10.528 | 1,05 |
| aleatorio | 10.000 | 25,78 | 106,26 | 6.922 | 0,69 |

### 5.4 Una escala donde el BST degenerado ya no es práctico

Con 100.000 títulos ya ordenados, el BST necesitaría
4.999.950.000 comparaciones solo para construirse (`n(n−1)/2`), por lo
que no se ejecuta. El AVL, en cambio, lo construye en
1.361 ms con altura 17 (mínima posible:
17), 99.983 rotaciones y
16,7 pasos promedio por búsqueda.

## 6. Por qué importa el balance

El costo de buscar en un árbol de búsqueda es la cantidad de niveles que hay que bajar,
o sea su altura. Cada comparación descarta un subárbol; que ese subárbol sea la mitad
de los nodos o apenas uno depende de la forma del árbol:

- **Árbol balanceado:** cada comparación descarta aproximadamente la mitad de los nodos,
  así que alcanzan `log₂ n` pasos. Con un millón de títulos son unos 20 pasos.
- **Árbol degenerado:** cada comparación descarta un solo nodo, así que hay que recorrer
  hasta `n`. Con un millón de títulos son hasta un millón de pasos, igual que una búsqueda
  secuencial. Todo lo que se ganó con el árbol se pierde.

Los resultados lo confirman. Con 10.000 títulos ordenados, el BST alcanzó altura
**10.000** y 5.201,5 pasos promedio por búsqueda, contra
**14** y 13,4 del AVL. Con entrada aleatoria el BST llegó a
altura 31 y 16,2 pasos promedio, contra altura 16 y
13,6 del AVL: con orden aleatorio el BST se defiende bien en promedio, aunque su peor
rama sigue siendo más profunda. **El BST rinde solo si el orden de entrada tiene suerte**, y
el catálogo no controla en qué orden llegan los datos. El escenario `casi_ordenado` muestra que no hace falta
una entrada perfectamente ordenada para sufrir: con solo el 5 % de títulos
desordenados, el BST llegó a altura 7.655 frente a 14 del AVL.

### Por qué el AVL garantiza `O(log n)`

Sea `N(h)` la mínima cantidad de nodos de un AVL de altura `h`. El árbol más escaso
tiene un subárbol de altura `h−1` y otro de altura `h−2`, así que
`N(h) = N(h−1) + N(h−2) + 1`. Es la recurrencia de Fibonacci: `N(h)` crece como
`φ^h` con `φ ≈ 1,618`. Despejando, `h ≤ 1,44·log₂(n+2)`. Es decir, la altura de un AVL
es `O(log n)` **para cualquier orden de inserción**, y como búsqueda e inserción cuestan
`O(h)`, ambas son `O(log n)` en el peor caso y no solo en promedio.

## 7. Costos y límites del AVL

- **Más trabajo por inserción.** Cada inserción actualiza alturas en el camino de vuelta
  y puede rotar. Con entrada aleatoria el BST ya queda razonablemente balanceado y el
  AVL no mejora de forma apreciable los pasos promedio, pero construirlo tomó
  4,1× más tiempo que el BST (106,3 ms contra
  25,8 ms con 10.000 títulos). Lo que se paga es la garantía.
- **Más memoria.** Un entero extra (la altura) por nodo.
- **Más complejidad de código.** Cuatro casos de rotación que hay que probar con cuidado.
- **Comparación con TP2.** El árbol estático de TP2 también tiene altura mínima, pero se
  construye ordenando los datos de una vez y no admite inserciones sin reconstruirse. El
  AVL logra esa altura de forma incremental, que es lo que necesita un catálogo que
  recibe cargas repetidas.

## 8. Conclusión

1. El BST de TP3 depende del orden de los datos: con entradas ordenadas, descendentes o
   en zigzag, su altura es `n` y su costo de búsqueda e inserción es `O(n)`, el mismo
   de la búsqueda secuencial.
2. El AVL mantiene la altura en `O(log n)` con rotaciones de costo constante, sin
   importar el orden de entrada: en todos los escenarios medidos su altura está dentro
   de la cota teórica y a no más de 3 niveles de la mínima posible.
3. La garantía tiene un precio pequeño (una altura por nodo y algo de trabajo extra al
   insertar), muy inferior al riesgo de que el catálogo degenere. Como la carga del
   catálogo no controla el orden de los datos, el proyecto adopta el AVL para la
   búsqueda por título.

Para repetir el experimento desde la raíz (tarda alrededor de un minuto por los casos
degenerados del BST):

```bash
python -m experimentos.benchmark_tp4
```

El comando actualiza `experimentos/resultados_tp4.csv` y este documento.
