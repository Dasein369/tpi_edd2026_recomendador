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

| ID | Requerimiento | Etapa prevista | Estado actual |
|----|---------------|-----------------|---------------|
| RF01 | El sistema debe recomendar un juego a partir de uno o varios juegos que le gustaron al usuario. | TP10 — Integración y defensa (Demo Day) | Objetivo del producto final: integrar catálogo, ranking y grafo en la selección personalizada que se presenta en la demo. |
| RF02 | El sistema debe permitir buscar un juego por título y ver su ficha completa. | TP1; eficiencia en TP2–TP4 | Implementado: búsqueda exacta sin distinguir mayúsculas mediante AVL; muestra título, género, desarrollador, rating, horas jugadas y tags. |
| RF03 | El sistema debe mostrar el Top 15 de juegos según un criterio (rating, popularidad, etc.). | TP6 | Implementado: usa un montículo binario máximo por rating y muestra hasta 15 juegos en orden descendente. |
| RF04 | El sistema debe permitir explorar juegos por género, tag o categoría. | TP1 (filtro); TP5 (jerarquía); TP7 (tags) | Implementado: filtra por género o tag y explora familias/categorías en un árbol general. |
| RF05 | El sistema debe mostrar qué tan relacionados están dos o más juegos elegidos por el usuario. | TP7–TP10 | La terminal muestra motivos de relación directa y cadenas indirectas entre dos juegos; la comparación conjunta forma parte del producto integrado para el Demo Day. |

### Requerimientos de apoyo (surgidos en TP1)

| ID | Requerimiento | Estado actual |
|----|---------------|---------------|
| RF06 | El sistema debe cargar el catálogo de videojuegos desde un archivo JSON. | Implementado |
| RF07 | El sistema debe listar todos los videojuegos del catálogo. | Implementado |
| RF08 | El sistema debe permitir buscar por texto parcial del título (ej: "zeld" encuentra "Zelda"). | Implementado en `Catalogo`, no expuesto en el menú |
| RF09 | El sistema debe permitir filtrar por desarrollador y por rating mínimo. | Implementado en `Catalogo`, no expuesto en el menú |

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
- Las horas jugadas se usan como aproximación de cuánto disfruta el usuario un juego,
  para intuir su perfil de gustos.
- Búsqueda, exploración, ranking y relaciones por terminal. La recomendación personalizada
  forma parte de la integración final prevista para TP10.
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

## 6. Producto integrado para TP10 (Demo Day)

- Llegar al Demo Day con el flujo de recomendación personalizada integrado: partir de
  uno o varios juegos elegidos por el usuario y combinar las relaciones del grafo con
  el ranking disponible.
- Definir la fuente de datos para una versión ampliada del catálogo: importación desde
  Steam o perfil de usuario simulado. El formato de entrada actual es JSON.
- Presentar RF05 con las consultas por pares ya disponibles y la comparación conjunta
  de varios juegos dentro del flujo final.
