# Requerimientos — Pixperience

## 1. Descripción

Pixperience es un sistema de recomendaciones de videojuegos que funciona por terminal
y organiza sus consultas con estructuras de datos. El dominio de referencia es Steam.
La versión de demostración carga 25 videojuegos desde `datos/videojuegos.json`; el
modelo contempla título, género, tags, desarrollador, rating y horas jugadas.

**Problema que resuelve.** Un jugador con una biblioteca grande de juegos comprados en
Steam muchas veces no sabe cuál elegir entre todos los que ya tiene. El sistema lo
orienta en su próxima elección.

**Usuario objetivo.** Jugador con una biblioteca grande en Steam, que prefiere juegos de
rol y que no siempre sabe cuál de los que ya tiene le conviene jugar.

## 2. Requerimientos funcionales

### Funcionalidades iniciales (definidas en TP0)

| ID | Requerimiento | Estado actual |
|----|---------------|-----------------|
| RF01 | Ayudar al usuario a elegir un videojuego mostrando juegos relacionados con el título que ingresa. | Implementado: muestra hasta 10 juegos, ordenados por similitud y rating. |
| RF02 | Buscar un juego por título y ver su ficha. | Implementado con AVL; si no hay coincidencia exacta, la terminal muestra títulos que contienen el texto ingresado. |
| RF03 | Mostrar hasta 15 juegos ordenados por rating. | Implementado mediante montículo máximo. |
| RF04 | Explorar juegos por género, tag o categoría. | Implementado con filtros y árbol de categorías. |
| RF05 | Consultar relaciones entre videojuegos. | Implementado: muestra juegos relacionados, compara dos títulos y permite recorrer conexiones con BFS y DFS. |

### Requerimientos de apoyo (surgidos en TP1)

| ID | Requerimiento | Estado actual |
|----|---------------|---------------|
| RF06 | El sistema debe cargar el catálogo de videojuegos desde un archivo JSON. | Implementado |
| RF07 | El sistema debe listar todos los videojuegos del catálogo. | Implementado |
| RF08 | Buscar por texto parcial del título. | Implementado como sugerencias en la opción de búsqueda. |
| RF09 | Filtrar por desarrollador o rating mínimo. | Implementado en `Catalogo` y disponible en la opción de filtros de la terminal. |

## 3. Requerimientos no funcionales

| ID | Requerimiento |
|----|---------------|
| RNF01 | El sistema debe ejecutarse con Python 3.10 o superior, usando solo la librería estándar. |
| RNF02 | El sistema debe operarse íntegramente por una interfaz de línea de comandos. |
| RNF03 | El código debe separarse en capas: `modelos` (datos), `estructuras` (colecciones), `servicios` (lógica), `algoritmos` (búsqueda y experimentos) y `ui` (interacción). |
| RNF04 | Las operaciones del catálogo deben tener pruebas automatizadas (`unittest`). |
| RNF05 | La búsqueda por título en producción usa el AVL integrado en TP4, que garantiza O(log n) en el peor caso para cualquier orden de carga. El BST de TP3, con costo O(h) y O(n) en el peor caso, se conserva para el experimento comparativo (`experimentos/benchmark_tp4.py`). TP2 conserva su comparación histórica entre búsqueda secuencial y árbol estático balanceado en `experimentos/benchmark_tp2.py`. |
| RNF06 | El acceso por título se evalúa con catálogos de hasta 100.000 elementos. El benchmark de TP2 compara una búsqueda secuencial (10,1 ms) con un árbol balanceado (3,2 µs) en la máquina de prueba; esos valores corresponden a la consulta y no al tiempo de carga de todas las estructuras. Los tiempos absolutos dependen del hardware; la comparación de crecimiento se explica en `docs/tp2-complejidad.md`. |
| RNF07 | El Top 15 se obtiene desde un montículo máximo construido al cargar el catálogo, sin ordenar ni copiar todos los juegos por consulta. La consulta cuesta O(k log k), con k ≤ 15. |
| RNF08 | Las relaciones entre juegos deben precalcularse, para no comparar contra todo el catálogo en cada consulta. |

## 4. Alcance

- Catálogo de videojuegos con título, género, tags, desarrollador, rating y horas jugadas.
- Búsqueda, exploración, ranking y consulta de juegos relacionados por terminal.
- Comparación experimental de estrategias de búsqueda en TP2 y TP3; la aplicación integra
  un AVL por título (TP4) y un árbol general de categorías (TP5).
- Top 15 por rating mediante montículo máximo (TP6).
- Relaciones entre videojuegos mediante un grafo, con consultas de similitud directa y
  recorridos BFS/DFS para explorar conexiones indirectas (TP7–TP8).

## 5. Fuera de alcance

- Evaluar qué juegos conviene comprar según precio o descuentos (funcionalidad tipo
  SteamDB): requiere historial de precios y lógica ajena a las estructuras de la materia.
- Interfaz gráfica.
- Autenticación o cuentas de usuario.

