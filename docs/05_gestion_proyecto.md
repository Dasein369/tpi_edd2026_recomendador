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
| TP3 — Árbol binario | BST por título, búsqueda integrada, recorridos, comparación con la búsqueda secuencial, pruebas y documentación | Hecho (5 tarjetas) |
| TP4 — AVL | Rotaciones, pruebas de desbalance del BST, comparación experimental y explicación de la complejidad | Hecho (4 tarjetas) |
| TP5 — Árbol general | Jerarquía de categorías y exploración integrada en terminal | Hecho |
| TP6 — Heap | Montículo máximo por rating, Top 15 en terminal y análisis de complejidad | Hecho |
| TP7 — Grafos | Modelo del grafo (vértices, aristas, tipo), lista de adyacencia, consultas de relacionados y relación entre dos juegos, terminal v5 | Hecho |
| TP8 — BFS y DFS | Cadena con menos relaciones, exploración en profundidad, análisis y terminal v6 | Implementado en código; revisión del equipo pendiente |
| TP10 — Integración y defensa | Producto final, documentación, demo y defensa | Pendiente |

El profesor indicó que TP9 no se requiere para esta entrega.


## Historias de usuario

**HU-01 — Recomendar (RF01)**
Como jugador con una biblioteca grande quiero indicar uno o varios juegos que me gustaron
para que el sistema me sugiera cuál jugar a continuación.
*Criterios:* acepta uno o más títulos; termina al dejar la respuesta vacía; muestra al
menos un juego recomendado que no sea ninguno de los ingresados.

**HU-02 — Buscar (RF02)**
Como jugador quiero buscar un juego por título para ver su ficha completa.
*Criterios TP3:* no distingue mayúsculas; si existe, muestra título, género,
desarrollador, rating, horas jugadas y tags; si no existe, lo informa.

**HU-03 — Top 15 (RF03)**
Como jugador quiero ver los juegos mejor valorados para decidir rápido qué jugar.
*Criterios:* muestra hasta 15 juegos, ordenados por rating descendente; si hay menos
de 15, muestra todos; si el catálogo está vacío, informa que no hay resultados.

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

**Tarea técnica TP3 — Integrar un BST por título**
Como equipo queremos reemplazar la búsqueda secuencial de producción por un árbol
binario de búsqueda dinámico, para consultar el catálogo navegando por título.
*Criterios de aceptación:* clave `titulo.casefold()`; inserción, búsqueda y recorridos
inorder/preorder/postorder; uso desde `Catalogo.buscar()`; misma respuesta que la
búsqueda secuencial de TP2; casos cubiertos con `unittest`; comparación y complejidad
documentadas; aplicación identificada como versión 2.

**Tarea técnica TP6 — Integrar un montículo máximo para el Top 15**
Como jugador quiero consultar rápido los juegos mejor valorados para elegir qué jugar.
*Criterios de aceptación:* montículo binario implementado manualmente; prioridad basada
en `rating`; heapify al cargar; consulta de hasta 15 juegos en orden descendente sin
mutar el montículo ni ordenar/copiar el catálogo; opción disponible en la terminal v4;
complejidad explicada.

**Tarea técnica TP7 — Modelar y construir el grafo de relaciones**
Como jugador quiero ver qué juegos se parecen a uno que me gustó, y por qué, para
descubrir qué jugar a continuación.
*Criterios de aceptación:* vértice = videojuego; arista = comparten género, familia,
desarrollador o tags; grafo no dirigido y pesado, con la elección documentada; lista de
adyacencia justificada con la densidad medida; consultas de juegos relacionados y de
relación entre dos juegos desde la terminal v5; sin aristas a sí mismo ni duplicadas;
casos cubiertos con `unittest`; complejidad documentada en `docs/tp7-grafo.md`.

**Tarea técnica TP8 — Recorrer el grafo con BFS y DFS**
Como jugador quiero conocer cómo se conectan dos juegos y explorar toda la red desde
uno para descubrir relaciones indirectas.
*Criterios de aceptación:* BFS devuelve una cadena con la menor cantidad de aristas;
DFS visita cada juego alcanzable una sola vez; ambos manejan vértices aislados y
catálogos vacíos; dos consultas disponibles en la terminal v6; pruebas automatizadas
y análisis en `docs/tp8-recorridos.md`.

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

### Sprint TP3

- **Qué salió bien:** el BST quedó conectado a `Catalogo.buscar()` y se conservó la
  búsqueda secuencial para comparar estrategias; inserciones y recorridos se
  implementaron de forma iterativa para admitir árboles degenerados grandes.
- **Qué mejorar:** el BST no garantiza altura logarítmica; insertar títulos ordenados
  puede llevar búsqueda e inserción a O(n).
- **Acción para TP4:** implementar AVL y comparar altura y búsqueda con el BST usando
  inserciones aleatorias y títulos ordenados.

### Sprint TP4

- **Qué salió bien:** el AVL quedó integrado al catálogo y las pruebas cubren las rotaciones, el balance, los títulos duplicados y la búsqueda. El experimento compara su altura y sus pasos de búsqueda con el BST.
- **Qué mejorar:** había explicaciones imprecisas sobre la altura del AVL y sobre la cantidad de títulos movidos en el escenario casi ordenado. También faltaba registrar el cierre de TP4 en este documento.
- **Acción para TP5:** revisar que el código, los resultados y las explicaciones coincidan antes de cerrar el sprint, y actualizar este documento junto con el tablero.

### Sprint TP5

- **Qué salió bien:** el árbol general quedó conectado con `Catalogo` y permite recorrer
  familias y géneros desde la terminal.
- **Qué mejorar:** la documentación general conservaba estados de TP4 y no reflejaba con
  precisión la versión activa de la terminal.
- **Acción para TP6:** registrar la estructura nueva tanto en los diagramas como en el
  README y mantener alineadas las versiones mostradas por la aplicación.

### Sprint TP6

- **Qué salió bien:** el montículo se construye al cargar el catálogo; la consulta Top-N
  recorre solo los candidatos necesarios y preserva la estructura.
- **Qué mejorar:** la prioridad actual usa el rating global como criterio único; la
  popularidad y la personalización quedan para una etapa posterior.
- **Acción para TP7:** modelar relaciones del dominio y definir con claridad el criterio
  de conexión antes de construir el grafo.

### Sprint TP7

- **Qué salió bien:** el grafo quedó integrado al catálogo y a la terminal; las pruebas
  cubren simetría, pesos, consultas y consistencia tras una carga inválida.
- **Qué mejorar:** la primera versión de la regla omitía los tags acordados para esta
  etapa y los documentos conservaban ejemplos y estados anteriores.
- **Acción para TP8:** definir una consulta real para BFS y otra para DFS, integrarlas
  en la terminal y documentar cuándo conviene cada recorrido.
