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
│   └── arbol_binario_busqueda.py  # BST dinámico por título (TP3)
├── algoritmos/
│   └── busqueda_secuencial.py     # estrategia de referencia de TP2/TP3
├── modelos/
│   └── videojuego.py             # clase de dominio (solo datos)
├── servicios/
│   └── catalogo.py                # lógica: cargar, buscar, listar, filtrar
├── ui/
│   └── terminal.py                # interfaz de línea de comandos
├── datos/
│   └── videojuegos.json           # dataset de prueba
├── experimentos/
│   └── benchmark_tp3.py           # comparación de estrategias integrada a TP3
├── tests/
│   ├── test_catalogo.py           # pruebas de las operaciones
│   ├── test_tp2.py                # comparación TP2
│   └── test_tp3.py                # árbol e integración con el catálogo
└── docs/
    ├── 01_requerimientos.md
    ├── 02_casos_de_uso.md
    ├── 03_diagrama_clases.md
    ├── 04_diagrama_datos.md
    ├── 05_gestion_proyecto.md
    ├── tp2-complejidad.md
    └── tp3-complejidad.md
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
0. Salir
```

La versión 2 integra un árbol binario de búsqueda construido por inserción para buscar
por título. La lista del catálogo se conserva para listar y filtrar. El BST no se
balancea: su búsqueda cuesta `O(h)`, con `O(log n)` promedio si su forma acompaña y
`O(n)` en el peor caso. TP4 abordará ese límite con AVL.

## Documentación

- [Requerimientos](docs/01_requerimientos.md)
- [Casos de uso](docs/02_casos_de_uso.md)
- [Diagrama de clases](docs/03_diagrama_clases.md)
- [Conexión entre estructuras](docs/04_diagrama_datos.md)
- [Gestión del proyecto](docs/05_gestion_proyecto.md)
- [Análisis TP2](docs/tp2-complejidad.md)
- [Comparación TP3](docs/tp3-complejidad.md)

## Correr las pruebas

```bash
python3 -m unittest discover -s tests -t . -v
```

## Salir del entorno virtual

```bash
deactivate
```
