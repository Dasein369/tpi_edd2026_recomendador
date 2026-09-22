# Gestión del proyecto

## Tablero

- **Trello:** https://trello.com/b/oStQ2vvu/pixperience
- **Columnas:** Links de Trabajo · Backlog · En progreso · En revisión · Hecho (una lista por sprint).
- **Evidencia:** capturas del tablero en `docs/capturas/`.

## Metodología

Scrum simplificado, con un sprint por Trabajo Práctico. Cada sprint tiene tarjetas de
trabajo, historias de usuario o tareas técnicas con criterios de aceptación, y una
retrospectiva breve al cierre.

## Sprints

| Sprint | Contenido | Estado |
|--------|-----------|--------|
| TP0 — Lanzamiento | Nombre, dominio, problema, usuario objetivo, cinco funcionalidades, ejemplo de interacción, boceto de terminal, diagrama inicial, propuesta | Hecho (9 tarjetas) |
| TP1 — Objetos y clases | Clases del dominio, encapsulamiento, interfaces entre módulos, carga de datos, terminal, buscar/listar/filtrar | Hecho (6 tarjetas; demo pendiente) |
| TP2 — Complejidad | Operación crítica, dos estrategias de búsqueda, mediciones con 100 a 100.000 elementos, notación O/Ω/Θ, conclusión técnica | Hecho (6 tarjetas) |
| TP3 — Árbol binario | Árbol de búsqueda integrado a la aplicación | En curso |

## Historias de usuario

**HU-01 — Recomendar (RF01)**
Como jugador con una biblioteca grande quiero indicar uno o varios juegos que me gustaron
para que el sistema me sugiera cuál jugar a continuación.
*Criterios:* acepta uno o más títulos; termina al dejar la respuesta vacía; muestra al
menos un juego recomendado que no sea ninguno de los ingresados.

**HU-02 — Buscar (RF02)**
Como jugador quiero buscar un juego por título para ver su ficha completa.
*Criterios:* no distingue mayúsculas; si existe, muestra título, género, tags,
desarrollador, rating y horas jugadas; si no existe, lo informa.

**HU-03 — Top 15 (RF03)**
Como jugador quiero ver el Top 15 según un criterio para decidir rápido qué jugar.
*Criterios:* muestra exactamente 15 juegos, ordenados de mayor a menor según el criterio elegido.

**HU-04 — Explorar (RF04)**
Como jugador quiero explorar juegos por género o tags para descubrir opciones dentro de lo que me gusta.
*Criterios:* solo aparecen juegos que cumplen lo pedido; si no hay coincidencias, lo informa.

**HU-05 — Relación (RF05)**
Como jugador quiero saber qué tan relacionados están varios juegos para entender qué tienen en común.
*Criterios:* para cada par relacionado muestra el motivo; si no hay relación, lo indica.

**Tarea técnica TP2 — Comparar estrategias de búsqueda**
Como equipo necesitamos saber si conviene cambiar la búsqueda secuencial por una
estructura más eficiente antes de integrarla al producto.
*Criterios de aceptación:* dos estrategias implementadas y con pruebas; medición con
100, 1.000, 10.000 y 100.000 elementos; complejidad expresada en notación O/Ω/Θ;
conclusión técnica documentada.

## Retrospectivas

### Sprint TP1

- **Qué salió bien:** el código quedó separado en capas (`modelos`, `servicios`, `ui`) y
  `Catalogo` se puede probar sin la interfaz.
- **Qué mejorar:** la documentación de `docs/` quedó vacía hasta el cierre del sprint; conviene
  completarla a medida que se avanza. La demo del TP1 quedó pendiente.
- **Acción para TP2:** mantener el tablero al día y actualizar los documentos de `docs/`
  en cada tarea.

### Sprint TP2

- **Qué salió bien:** las dos estrategias quedaron con pruebas automatizadas
  (`tests/test_tp2.py`) desde el principio, y el script de experimentos genera solo la
  documentación de resultados (CSV + Markdown), sin transcripción manual de números.
- **Qué mejorar:** la segunda estrategia se decidió en equipo (árbol balanceado) sin
  coordinar antes con todos los integrantes cuál sería exactamente; conviene acordar el
  enfoque técnico de cada etapa antes de empezar a programarla, para no tener que
  revisar decisiones ya implementadas.
- **Acción para TP3:** acordar entre los tres integrantes, antes de escribir código,
  que el árbol de TP3 se construye por inserción (no reutiliza el árbol balanceado de
  TP2), para que TP4 tenga un caso real de desbalance que resolver.
