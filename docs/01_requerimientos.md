# Requerimientos — Pixperience

## 1. Descripción

Pixperience es un sistema de recomendaciones de videojuegos que funciona por terminal
y organiza sus consultas con estructuras de datos. El dominio de referencia es Steam.
La versión de demostración carga 25 videojuegos desde `datos/videojuegos.json`; el
modelo contempla título, género, tags, desarrollador, rating y horas jugadas.

**Problema que resuelve.** Un jugador no sabe qué jugar y quiere descubrir títulos
relacionados a partir de un juego que elige.

**Usuario objetivo.** Jugador que busca opciones relacionadas con un título de interés.

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
| RNF03 | El código se organiza en `modelos` (datos), `estructuras` (colecciones), `servicios` (lógica), `algoritmos` (búsquedas), `experimentos` (benchmarks) y `ui` (interacción). |
| RNF04 | Las operaciones del catálogo deben tener pruebas automatizadas (`unittest`). |
| RNF05 | La búsqueda por título usa el AVL integrado en TP4, con O(log n) garantizado. El BST de TP3 se conserva para los benchmarks de TP3 y TP4; el árbol estático balanceado de TP2, para `experimentos/benchmark_tp2.py`. |
| RNF06 | Comparar estrategias de búsqueda con datos de hasta 100.000 títulos; resultados en `docs/tp2-complejidad.md`. |
| RNF07 | El Top 15 se obtiene desde un montículo máximo construido al cargar el catálogo, sin ordenar ni copiar todos los juegos por consulta. La consulta cuesta O(k log k), con k ≤ 15. |
| RNF08 | Las relaciones entre juegos deben precalcularse, para no comparar contra todo el catálogo en cada consulta. |

## 4. Alcance

- Catálogo de videojuegos con título, género, tags, desarrollador, rating y horas jugadas.
- Búsqueda, exploración, ranking y consulta de juegos relacionados por terminal.
- Comparación experimental de estrategias de búsqueda en TP2, TP3 y TP4; la aplicación integra
  un AVL por título (TP4) y un árbol general de categorías (TP5).
- Top 15 por rating mediante montículo máximo (TP6).
- Relaciones entre videojuegos mediante un grafo, con consultas de similitud directa y
  recorridos BFS/DFS para explorar conexiones indirectas (TP7–TP8).

## 5. Fuera de alcance

- Evaluar qué juegos conviene comprar según precio o descuentos (funcionalidad tipo
  SteamDB): requiere historial de precios y lógica ajena a las estructuras de la materia.
- Interfaz gráfica.
- Autenticación o cuentas de usuario.

