# Requerimientos — Pixperience

## 1. Descripción

Pixperience es un sistema de recomendaciones de videojuegos que funciona por terminal.
Trabaja sobre datos de Steam (el dataset de referencia es el FronkonGames Steam Games
Dataset, +83.000 juegos con género, tags, desarrollador y rating), aunque por el
momento el catálogo de prueba es un JSON armado a mano con 25 juegos reales.

**Problema que resuelve.** Un jugador con una biblioteca grande de juegos comprados en
Steam muchas veces no sabe cuál elegir entre todos los que ya tiene. El sistema lo
orienta en su próxima elección.

**Usuario objetivo.** Jugador con una biblioteca grande en Steam, que prefiere juegos de
rol y que no siempre sabe cuál de los que ya tiene le conviene jugar.

## 2. Requerimientos funcionales

### Funcionalidades iniciales (definidas en TP0)

| ID | Requerimiento | Etapa prevista | Estado actual |
|----|---------------|-----------------|---------------|
| RF01 | El sistema debe recomendar un juego a partir de uno o varios juegos que le gustaron al usuario. | TP7–TP8 | Pendiente |
| RF02 | El sistema debe permitir buscar un juego por título y ver su ficha completa. | TP1; eficiencia en TP2–TP4 | Parcial: busca por título exacto (sin distinguir mayúsculas) y muestra título, género y rating. Falta la ficha completa (tags, desarrollador, horas jugadas). |
| RF03 | El sistema debe mostrar el Top 15 de juegos según un criterio (rating, popularidad, etc.). | TP6 | Pendiente |
| RF04 | El sistema debe permitir explorar juegos por género o categoría. | TP1 (filtro); TP5 (jerarquía) | Parcial: filtra por género exacto. Faltan tags y jerarquía de categorías. |
| RF05 | El sistema debe mostrar qué tan relacionados están dos o más juegos elegidos por el usuario. | TP7–TP8 | Pendiente |

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
| RNF03 | El código debe separarse en capas: `modelos` (datos), `servicios` (lógica), `algoritmos` (estrategias de búsqueda/ordenamiento) y `ui` (interacción). |
| RNF04 | Las operaciones del catálogo deben tener pruebas automatizadas (`unittest`). |
| RNF05 | La búsqueda por título en producción es actualmente secuencial: **Θ(n)**. TP2 comparó esto contra una segunda estrategia (árbol binario balanceado, Θ(log n)) a nivel experimental (`experimentos/benchmark_tp2.py`, `docs/tp2-complejidad.md`), sin integrarla todavía a la aplicación. Migrar la búsqueda de producción a una estructura de tiempo logarítmico es el objetivo de TP3. |
| RNF06 | El sistema debe soportar catálogos grandes sin degradación perceptible. TP2 midió ambas estrategias hasta 100.000 elementos: la secuencial escala linealmente (~6.1 ms en el peor caso con 100.000 elementos, en la máquina de prueba); el árbol balanceado se mantiene prácticamente constante (~2.4 µs). Los tiempos absolutos dependen del hardware; lo relevante es la diferencia de orden de crecimiento. |
| RNF07 | El Top 15 debe obtenerse sin ordenar todo el catálogo en cada consulta. |
| RNF08 | Las relaciones entre juegos deben precalcularse, para no comparar contra todo el catálogo en cada consulta. |

## 4. Alcance

- Catálogo de videojuegos con título, género, tags, desarrollador, rating y horas jugadas.
- Las horas jugadas se usan como aproximación de cuánto disfruta el usuario un juego,
  para intuir su perfil de gustos.
- Búsqueda, exploración, ranking, relaciones y recomendaciones, todo por terminal.
- Comparación experimental de estrategias de búsqueda (TP2), como base para elegir
  la estructura de datos a integrar en TP3.

## 5. Fuera de alcance

- Evaluar qué juegos conviene comprar según precio o descuentos (funcionalidad tipo
  SteamDB): requiere historial de precios y lógica ajena a las estructuras de la materia.
- Interfaz gráfica.
- Autenticación o cuentas de usuario.

## 6. Decisiones pendientes

- Usar la API real de Steam o un perfil de usuario simulado.
- Incorporar `tags` al modelo `Videojuego` (hoy no los tiene; son necesarios para RF04 y
  RF05). Decisión pospuesta a TP5 (jerarquía de categorías), registrada en el Backlog de Trello.
- El árbol balanceado usado en el experimento de TP2 (`ArbolBusquedaBalanceada`) no se
  reutiliza en TP3: se construye ordenando los datos y particionando recursivamente, por
  lo que nunca se desbalancea. TP3 requiere un árbol construido por inserción uno a uno,
  para que TP4 pueda mostrar un caso real de desbalance.
