# Pixperience
Sistema de recomendaciones de Videojuegos

Trabajo Práctico Integrador (TPI) — Estructuras de Datos

## Integrantes
- Santiago Giménez
- Martín Sánchez
- Gastón Neibert

## Estructura del proyecto

```
proyecto/
├── main.py                       # punto de entrada
├── estructuras/
│   ├── arbol_binario_busqueda.py  # BST dinámico por título (TP3)
│   ├── arbol_avl.py               # AVL autobalanceado por título (TP4)
│   ├── arbol_general.py           # jerarquía de categorías (TP5)
│   ├── monticulo_maximo.py        # Heap binario para el Top 15 (TP6)
│   └── grafo.py                   # grafo no dirigido y pesado, lista de adyacencia (TP7)
├── algoritmos/
│   └── busqueda_secuencial.py     # estrategia de referencia de TP2/TP3
├── modelos/
│   ├── categoria.py               # familia/categoría del árbol general (TP5)
│   └── videojuego.py             # clase de dominio (solo datos)
├── servicios/
│   ├── catalogo.py                # lógica: cargar, buscar, listar, filtrar, relacionados
│   └── relaciones.py              # criterio de similitud y construcción del grafo (TP7)
├── ui/
│   └── terminal.py                # interfaz de línea de comandos
├── datos/
│   └── videojuegos.json           # dataset de prueba
├── experimentos/
│   ├── benchmark_tp3.py           # comparación de estrategias integrada a TP3
│   └── benchmark_tp4.py           # BST vs AVL ante entradas desbalanceadas (TP4)
├── tests/
│   ├── test_catalogo.py           # pruebas de las operaciones
│   ├── test_tp2.py                # comparación TP2
│   ├── test_tp3.py                # árbol e integración con el catálogo
│   ├── test_tp4.py                # AVL: rotaciones, invariantes, integración
│   ├── test_tp5.py                # árbol general de categorías
│   ├── test_tp6.py                # montículo y Top 15
│   └── test_tp7.py                # grafo, relaciones y terminal v5
└── docs/
    ├── 01_requerimientos.md
    ├── 02_casos_de_uso.md
    ├── 03_diagrama_clases.md
    ├── 04_diagrama_datos.md
    ├── 05_gestion_proyecto.md
    ├── tp2-complejidad.md
    ├── tp3-complejidad.md
    ├── tp4-avl.md
    ├── tp6-heap.md
    └── tp7-grafo.md
```

## Requisitos

- Python 3.10 o superior (el código usa sintaxis como `Videojuego | None` en los type hints)

## Instalación

1. Clonar el repositorio y ubicarse en la raíz del proyecto (donde está este `README.md`).

2. Crear un entorno virtual:

   ```bash
   python3 -m venv venv
   ```

3. Activarlo:

   - Linux / Mac:
     ```bash
     source venv/bin/activate
     ```
   - Windows (CMD):
     ```bash
     venv\Scripts\activate.bat
     ```
   - Windows (PowerShell):
     ```bash
     venv\Scripts\Activate.ps1
     ```

   El prompt de la terminal debería mostrar `(venv)` al principio.

4. No hay dependencias externas que instalar: el proyecto solo usa la librería estándar de Python (`json`, `unittest`, etc.).

## Ejecución

**Importante:** hay que correr los comandos parado en la raíz del proyecto (la misma carpeta donde está `main.py`), porque el dataset se carga con una ruta relativa (`datos/videojuegos.json`).

```bash
python main.py
```

Esto levanta el menú interactivo por terminal:

```
1. Buscar videojuego
2. Listar todos los videojuegos
3. Filtrar por categoría
4. Explorar categorías
5. Ver Top 15 por rating
6. Ver juegos relacionados
7. Relación entre dos juegos
0. Salir
```

La búsqueda por título usa un árbol AVL, construido por inserción. Las categorías se
exploran mediante un árbol general. El Top 15 por rating se obtiene con un montículo
binario máximo implementado en el proyecto. Los juegos relacionados salen de un grafo
no dirigido y pesado (lista de adyacencia): dos juegos se conectan si comparten género,
familia de géneros o desarrollador, y el peso indica cuánto se parecen. La lista del catálogo se conserva para
listar y filtrar. El BST de TP3 se desbalancea con entradas ordenadas (búsqueda `O(n)` en
el peor caso); el AVL se autobalancea con rotaciones y garantiza `O(log n)` para
cualquier orden de carga. El BST se conserva para el experimento comparativo de TP4.

## Documentación

- [Requerimientos](docs/01_requerimientos.md)
- [Casos de uso](docs/02_casos_de_uso.md)
- [Diagrama de clases](docs/03_diagrama_clases.md)
- [Conexión entre estructuras](docs/04_diagrama_datos.md)
- [Gestión del proyecto](docs/05_gestion_proyecto.md)
- [Análisis TP2](docs/tp2-complejidad.md)
- [Comparación TP3](docs/tp3-complejidad.md)
- [AVL frente al BST desbalanceado (TP4)](docs/tp4-avl.md)
- [Montículo y Top 15 (TP6)](docs/tp6-heap.md)
- [Grafo de relaciones (TP7)](docs/tp7-grafo.md)

## Correr las pruebas

```bash
python3 -m unittest discover -s tests -t . -v
```

## Salir del entorno virtual

```bash
deactivate
```
