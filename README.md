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
├── modelos/
│   └── videojuego.py             # clase de dominio (solo datos)
├── servicios/
│   └── catalogo.py                # lógica: cargar, buscar, listar, filtrar
├── ui/
│   └── terminal.py                # interfaz de línea de comandos
├── datos/
│   └── videojuegos.json           # dataset de prueba
├── tests/
│   └── test_catalogo.py           # pruebas de las operaciones
└── docs/
    └── 03-diagrama-clases.md      # diagrama UML actualizado
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

## Correr las pruebas

```bash
python3 -m unittest discover -s tests -t . -v
```

## Salir del entorno virtual

```bash
deactivate
```
