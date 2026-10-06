"""Compara la búsqueda secuencial y el BST integrado de TP3.

Desde la raíz del proyecto: ``python -m experimentos.benchmark_tp3``.
La construcción se excluye de la medición de consultas, igual que en TP2.
"""

from __future__ import annotations

import csv
import json
import random
import statistics
import time
from pathlib import Path

from algoritmos.busqueda_secuencial import buscar_secuencial
from estructuras.arbol_binario_busqueda import ArbolBinarioBusqueda
from modelos.videojuego import Videojuego


ROOT = Path(__file__).resolve().parents[1]
TAMANOS = (100, 1_000, 10_000, 100_000)
REPETICIONES = 7
SEMILLA = 2026
CSV_PATH = ROOT / "experimentos" / "resultados_tp3.csv"
DOC_PATH = ROOT / "docs" / "tp3-complejidad.md"


def cargar_videojuegos_base() -> list[Videojuego]:
    with (ROOT / "datos" / "videojuegos.json").open(encoding="utf-8") as archivo:
        datos = json.load(archivo)
    elementos = datos.get("videojuegos", datos) if isinstance(datos, dict) else datos
    return [Videojuego(**item) for item in elementos]


def generar_videojuegos(base: list[Videojuego], cantidad: int) -> list[Videojuego]:
    return [
        Videojuego(
            id=indice + 1,
            titulo=f"{base[indice % len(base)].titulo} [TP3-{indice + 1:06d}]",
            genero=base[indice % len(base)].genero,
            desarrollador=base[indice % len(base)].desarrollador,
            rating=base[indice % len(base)].rating,
            horas_jugadas=base[indice % len(base)].horas_jugadas,
        )
        for indice in range(cantidad)
    ]


def medir_mediana_ns(consulta, cantidad: int) -> float:
    """Devuelve la mediana de nanosegundos por consulta."""
    consulta()
    iteraciones = max(10, 500_000 // cantidad)
    mediciones: list[float] = []

    for _ in range(REPETICIONES):
        inicio = time.perf_counter_ns()
        for _ in range(iteraciones):
            consulta()
        duracion = time.perf_counter_ns() - inicio
        mediciones.append(duracion / iteraciones)

    return statistics.median(mediciones)


def construir_resultados() -> list[dict[str, int | float]]:
    base = cargar_videojuegos_base()
    resultados: list[dict[str, int | float]] = []

    for cantidad in TAMANOS:
        videojuegos = generar_videojuegos(base, cantidad)
        objetivo = videojuegos[-1]
        secuencia_insercion = videojuegos.copy()
        random.Random(SEMILLA + cantidad).shuffle(secuencia_insercion)
        arbol = ArbolBinarioBusqueda(secuencia_insercion)

        ns_secuencial = medir_mediana_ns(
            lambda: buscar_secuencial(videojuegos, objetivo.titulo), cantidad
        )
        ns_arbol = medir_mediana_ns(
            lambda: arbol.buscar(objetivo.titulo), cantidad
        )

        resultados.append(
            {
                "elementos": cantidad,
                "busqueda_secuencial_ns": round(ns_secuencial, 1),
                "busqueda_bst_ns": round(ns_arbol, 1),
                "altura_bst": arbol.altura(),
                "relacion_secuencial_bst": round(ns_secuencial / ns_arbol, 2),
            }
        )

    return resultados


def escribir_csv(resultados: list[dict[str, int | float]]) -> None:
    with CSV_PATH.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(resultados[0]))
        escritor.writeheader()
        escritor.writerows(resultados)


def escribir_documentacion(resultados: list[dict[str, int | float]]) -> None:
    def numero_espanol(valor: int | float, decimales: int = 1) -> str:
        formateado = f"{valor:,.{decimales}f}"
        return formateado.replace(",", "_").replace(".", ",").replace("_", ".")

    filas = "\n".join(
        f"| {numero_espanol(fila['elementos'], 0)} | "
        f"{numero_espanol(fila['busqueda_secuencial_ns'])} | "
        f"{numero_espanol(fila['busqueda_bst_ns'])} | {fila['altura_bst']} | "
        f"{numero_espanol(fila['relacion_secuencial_bst'], 2)}× |"
        for fila in resultados
    )
    contenido = f"""# TP3 — Búsqueda secuencial frente al BST integrado

## Decisión de diseño

El árbol binario de búsqueda ordena por `titulo.casefold()`, por lo que una consulta
no distingue mayúsculas. Se construye insertando los videojuegos de a uno, en el orden
en que se cargan; no ordena ni balancea la entrada. Los títulos equivalentes sin
distinción de mayúsculas se insertan a la derecha y se conservan; `buscar` devuelve
la primera coincidencia encontrada desde la raíz.

`Catalogo.buscar()` consulta este árbol en producción. La lista del catálogo se conserva
para listar, filtrar y mantener el orden original de carga. El árbol es una estructura
distinta de `ArbolBusquedaBalanceada`, que sigue siendo exclusiva del experimento TP2.

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
degenerar en una cadena; esa limitación es el caso que se resolverá con AVL en TP4.

## Comparación experimental

El script `experimentos/benchmark_tp3.py` compara la búsqueda secuencial de TP2 con el
BST integrado. Genera entradas de 100, 1.000, 10.000 y 100.000 títulos, fija una semilla
para mezclar el orden de inserción, busca el último elemento de la lista (peor caso de
la secuencial) y toma la mediana de siete tandas. El tiempo de construcción del árbol
queda fuera de la medición de consultas, pero se analiza por separado en la tabla
teórica. La altura se informa para hacer visible la forma obtenida en cada tamaño.

Los tiempos están expresados en nanosegundos por consulta y dependen del equipo. La
medición de una ejecución sirve como observación, no como garantía de crecimiento:
esa garantía depende de la forma del árbol.

| Elementos | Secuencial (ns) | BST (ns) | Altura BST | Relación secuencial / BST |
|---:|---:|---:|---:|---:|
{filas}

## Conclusión

El BST integrado reduce las comparaciones frente al recorrido lineal cuando las
inserciones mantienen una forma de altura baja. A diferencia del árbol balanceado
experimental de TP2, este BST refleja el orden real de carga y puede desbalancearse.
La mejora promedio viene con ese límite: tanto búsqueda como inserción pueden llegar
a O(n). TP4 agregará AVL para acotar la altura y garantizar búsquedas O(log n).

Para repetir el experimento desde la raíz:

```bash
python -m experimentos.benchmark_tp3
```

El comando actualiza `experimentos/resultados_tp3.csv` y esta tabla.
"""
    DOC_PATH.write_text(contenido, encoding="utf-8")


def main() -> None:
    resultados = construir_resultados()
    escribir_csv(resultados)
    escribir_documentacion(resultados)
    print(f"CSV generado: {CSV_PATH.relative_to(ROOT)}")
    print(f"Documentación actualizada: {DOC_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
