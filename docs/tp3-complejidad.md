# TP3 — Búsqueda secuencial frente al BST

## Decisión de diseño

El árbol binario de búsqueda ordena por `titulo.casefold()`, por lo que una consulta
no distingue mayúsculas. Se construye insertando los videojuegos de a uno, en el orden
en que se cargan; no ordena ni balancea la entrada. Los títulos equivalentes sin
distinción de mayúsculas se insertan a la derecha y se conservan; `buscar` devuelve
la primera coincidencia encontrada desde la raíz.

El BST se conserva para comparar con la búsqueda secuencial en el experimento de TP3.
La aplicación usa el AVL integrado en TP4 para buscar títulos; la lista del catálogo se
mantiene para listar, filtrar y conservar el orden original de carga. Este BST es una
estructura distinta de `ArbolBusquedaBalanceada`, exclusiva del experimento TP2.

## Complejidad teórica

Sea `h` la altura del BST y `n` la cantidad de videojuegos:

| Operación | BST | Búsqueda secuencial |
|---|---:|---:|
| Buscar, mejor caso | Ω(1) | Ω(1) |
| Buscar, promedio | Θ(log n) si la forma es razonablemente equilibrada; en general O(h) | Θ(n) |
| Buscar, peor caso | O(n), si las inserciones producen una cadena | O(n) |
| Insertar un elemento | O(h); O(log n) promedio bajo esa misma condición, O(n) peor caso | No aplica |
| Construir con n inserciones | O(n log n) promedio bajo esa misma condición, O(n²) peor caso | No aplica |
| Espacio de la estructura | O(n) | O(1) adicional |

La búsqueda del árbol se expresa como O(h), no como O(log n) garantizado. El orden de
inserción determina la forma del BST. Insertar títulos ya ordenados puede hacerlo
degenerar en una cadena; esa limitación motivó la integración del AVL en TP4.

## Comparación experimental

El script `experimentos/benchmark_tp3.py` compara la búsqueda secuencial de TP2 con el
BST de TP3. Genera entradas de 100, 1.000, 10.000 y 100.000 títulos, fija una semilla
para mezclar el orden de inserción, busca el último elemento de la lista (peor caso de
la secuencial) y toma la mediana de siete tandas. El tiempo de construcción del árbol
queda fuera de la medición de consultas, pero se analiza por separado en la tabla
teórica. La altura se informa para hacer visible la forma obtenida en cada tamaño.

Los tiempos están expresados en nanosegundos por consulta y dependen del equipo. La
medición de una ejecución sirve como observación, no como garantía de crecimiento:
esa garantía depende de la forma del árbol.

| Elementos | Secuencial (ns) | BST (ns) | Altura BST | Relación secuencial / BST |
|---:|---:|---:|---:|---:|
| 100 | 13.551,7 | 2.773,3 | 13 | 4,89× |
| 1.000 | 147.089,8 | 4.124,0 | 22 | 35,67× |
| 10.000 | 1.398.428,0 | 4.708,0 | 30 | 297,03× |
| 100.000 | 13.903.700,0 | 6.380,0 | 39 | 2.179,26× |

## Conclusión

En esta muestra, el BST tuvo menor tiempo de búsqueda que el recorrido lineal porque las
inserciones produjeron una altura baja. A diferencia del árbol balanceado experimental
de TP2, puede desbalancearse según el orden de inserción: búsqueda e inserción llegan a
O(n) en el peor caso. La aplicación usa el AVL integrado en TP4 para garantizar
búsquedas O(log n).

Para repetir el experimento desde la raíz:

```bash
python -m experimentos.benchmark_tp3
```

El comando actualiza `experimentos/resultados_tp3.csv` y esta tabla.
