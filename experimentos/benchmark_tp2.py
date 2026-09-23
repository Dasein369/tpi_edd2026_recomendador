from __future__ import annotations

import csv
import json
import platform
import statistics
import sys
from pathlib import Path
from time import perf_counter_ns

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from algoritmos.busqueda_arbol_tp2 import ArbolBusquedaBalanceada
from algoritmos.busqueda_secuencial import buscar_secuencial
from modelos.videojuego import Videojuego

TAMANOS = (100, 1_000, 10_000, 100_000)
REPETICIONES = 7
COMPARACIONES_OBJETIVO = 5_000_000
SEED_PATH = ROOT / "datos" / "videojuegos.json"
RESULTADOS_PATH = ROOT / "experimentos" / "resultados_tp2.csv"
DOCUMENTACION_PATH = ROOT / "docs" / "tp2-complejidad.md"


def cargar_semillas() -> list[dict]:
    with SEED_PATH.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)
    elementos = datos.get("videojuegos", datos) if isinstance(datos, dict) else datos
    if not elementos:
        raise ValueError("El dataset base está vacío.")
    return elementos


def generar_datos(cantidad: int, semillas: list[dict]) -> list[Videojuego]:
    """Genera N objetos con títulos únicos a partir del dataset real del proyecto."""
    resultado: list[Videojuego] = []

    for i in range(cantidad):
        base = semillas[i % len(semillas)]
        titulo = f"{base['titulo']} [TP2-{i + 1:06d}]"

        resultado.append(
            Videojuego(
                id=i + 1,
                titulo=titulo,
                genero=base["genero"],
                desarrollador=base["desarrollador"],
                rating=base["rating"],
                horas_jugadas=base["horas_jugadas"],
            )
        )

    return resultado


def iteraciones_para(n: int) -> int:
    """Mantiene aproximadamente constante el trabajo interno de cada medición."""
    return max(20, COMPARACIONES_OBJETIVO // n)


def medir(funcion, objetivo: str, iteraciones: int) -> int:
    """Devuelve nanosegundos por búsqueda usando la mediana de varias repeticiones."""
    muestras: list[float] = []
    resultado = None

    for _ in range(REPETICIONES):
        # Calentamiento corto para reducir ruido inicial.
        funcion(objetivo)

        inicio = perf_counter_ns()
        for _ in range(iteraciones):
            resultado = funcion(objetivo)
        fin = perf_counter_ns()

        if resultado is None:
            raise AssertionError(f"La búsqueda falló para '{objetivo}'.")

        muestras.append((fin - inicio) / iteraciones)

    return int(statistics.median(muestras))


def construir_resultados() -> list[dict]:
    semillas = cargar_semillas()
    resultados: list[dict] = []

    print("TP2 — Benchmark de búsqueda secuencial vs. árbol balanceado")
    print(f"Python: {platform.python_version()} | {platform.system()} {platform.machine()}")
    print("La construcción del árbol NO está incluida en el tiempo de búsqueda.")
    print()
    print(f"{'N':>8} {'Iteraciones':>12} {'Secuencial (µs)':>20} {'Árbol (µs)':>16} {'Relación':>12} {'Altura':>8}")
    print("-" * 82)

    for n in TAMANOS:
        videojuegos = generar_datos(n, semillas)
        objetivo = videojuegos[-1].titulo  # peor caso de la búsqueda secuencial.

        arbol = ArbolBusquedaBalanceada(videojuegos)
        iteraciones = iteraciones_para(n)

        secuencial_ns = medir(lambda titulo: buscar_secuencial(videojuegos, titulo), objetivo, iteraciones)
        arbol_ns = medir(arbol.buscar, objetivo, iteraciones)

        if arbol.buscar(objetivo) is None:
            raise AssertionError("El árbol no encontró el objetivo del experimento.")

        velocidad_relativa = secuencial_ns / arbol_ns if arbol_ns else float("inf")

        fila = {
            "n_elementos": n,
            "iteraciones": iteraciones,
            "secuencial_ns": secuencial_ns,
            "arbol_ns": arbol_ns,
            "secuencial_us": round(secuencial_ns / 1_000, 4),
            "arbol_us": round(arbol_ns / 1_000, 4),
            "relacion_secuencial_vs_arbol": round(velocidad_relativa, 2),
            "altura_arbol": arbol.altura(),
        }
        resultados.append(fila)

        print(
            f"{n:>8,} {iteraciones:>12,} {fila['secuencial_us']:>20.4f} "
            f"{fila['arbol_us']:>16.4f} {velocidad_relativa:>11.2f}x {arbol.altura():>8}"
        )

    return resultados


def escribir_csv(resultados: list[dict]) -> None:
    RESULTADOS_PATH.parent.mkdir(parents=True, exist_ok=True)
    campos = list(resultados[0].keys())

    with RESULTADOS_PATH.open("w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos, lineterminator="\n")
        writer.writeheader()
        writer.writerows(resultados)


def escribir_documentacion(resultados: list[dict]) -> None:
    filas = "\n".join(
        f"| {r['n_elementos']:,} | {r['secuencial_us']:.4f} µs | "
        f"{r['arbol_us']:.4f} µs | {r['relacion_secuencial_vs_arbol']:.2f}x | {r['altura_arbol']} |"
        for r in resultados
    )

    DOCUMENTACION_PATH.parent.mkdir(parents=True, exist_ok=True)
    contenido = f'''# TP2 — Análisis de complejidad y comparación de búsquedas

## 1. Objetivo

El sistema **PixExperience** debe permitir encontrar un videojuego por título. En TP1 esa operación se resuelve recorriendo secuencialmente la lista del catálogo. En TP2 se comparan dos estrategias para la misma necesidad:

1. **Búsqueda secuencial** sobre una lista.
2. **Búsqueda en un árbol binario de búsqueda balanceado**, construido a partir de los mismos elementos.

La comparación se realiza con 100, 1.000, 10.000 y 100.000 elementos.

## 2. Estrategia A — Búsqueda secuencial

La función `buscar_secuencial` recorre los elementos desde el comienzo y compara el título de cada videojuego con el buscado.

- Mejor caso: **Θ(1)**, cuando el primer elemento coincide.
- Caso promedio: **Θ(n)**.
- Peor caso: **Θ(n)**, cuando el elemento está al final o no existe.
- Espacio adicional: **O(1)**.

En el benchmark se busca deliberadamente el último elemento de la lista para observar el peor caso temporal.

## 3. Estrategia B — Búsqueda en árbol

`ArbolBusquedaBalanceada` ordena los elementos por título y construye un árbol binario tomando el elemento central de cada intervalo. Esto mantiene una altura logarítmica para los datasets del experimento.

En cada comparación, si el título buscado es menor se continúa por la izquierda y, si es mayor, por la derecha.

- Mejor caso: **Θ(1)**, si la raíz coincide.
- Caso promedio: **Θ(log n)**.
- Peor caso en este experimento: **Θ(log n)**, porque el árbol se construye balanceado.
- Espacio del árbol: **O(n)**.

La construcción del árbol se excluye de la medición de búsqueda. En esta implementación la construcción incluye ordenar los datos, por lo que cuesta **O(n log n)**; es un costo de preparación amortizable cuando el catálogo se consulta muchas veces.

> Esta estructura es específica del experimento de TP2. El TP3 puede incorporar un BST dinámico con inserción y recorridos dentro de la aplicación.

## 4. Diseño experimental

Para cada tamaño `n`:

1. Se generan exactamente `n` objetos `Videojuego` a partir del dataset base del proyecto.
2. Se agregan sufijos `[TP2-XXXXXX]` para garantizar títulos únicos sin cambiar el dominio.
3. Se construye el árbol antes de medir.
4. Se selecciona el último videojuego de la lista como objetivo, lo que fuerza el peor caso de la búsqueda secuencial.
5. Cada estrategia se ejecuta varias veces y se informa la **mediana de los nanosegundos por consulta**.
6. Se utiliza una cantidad de iteraciones adaptada a `n` para evitar que una medición muy corta quede dominada por el overhead del reloj.

## 5. Resultados de la última ejecución

> Los tiempos son dependientes del hardware, del sistema operativo y de la versión de Python. La tabla se actualiza automáticamente ejecutando `python -m experimentos.benchmark_tp2`.

| N elementos | Secuencial | Árbol | Relación | Altura del árbol |
|---:|---:|---:|---:|---:|
{filas}

## 6. Interpretación

La búsqueda secuencial aumenta aproximadamente en proporción al tamaño de la entrada porque, en el escenario medido, tiene que revisar todos los elementos hasta llegar al objetivo. El árbol balanceado crece mucho más lentamente porque cada comparación elimina una parte importante del espacio de búsqueda.

La diferencia experimental no reemplaza el análisis teórico: los tiempos absolutos cambian según la máquina, pero las funciones de crecimiento siguen siendo distintas. Por eso la conclusión principal se expresa con complejidad asintótica: **Θ(n) frente a Θ(log n)** para los casos representados por este experimento.

## 7. Conclusión técnica

Para un catálogo pequeño, ambas estrategias pueden responder rápidamente y la simplicidad de la lista puede ser suficiente. A medida que el catálogo crece y la búsqueda se realiza muchas veces, un árbol balanceado reduce el número de comparaciones necesarias para localizar un título.

Por lo tanto, el experimento muestra una diferencia fundamental de escalabilidad: la estrategia secuencial requiere un trabajo proporcional a `n` en el peor caso, mientras que la búsqueda sobre el árbol balanceado requiere un número de pasos proporcional a `log n`.

La siguiente etapa del proyecto, TP3, consiste en llevar esta idea al producto mediante un BST integrado a la aplicación.

## 8. Cómo ejecutar

Desde la raíz del repositorio:

```bash
python -m experimentos.benchmark_tp2
```

El script genera/actualiza:

- `experimentos/resultados_tp2.csv`
- `docs/tp2-complejidad.md`

## 9. Pruebas

Desde la raíz del repositorio:

```bash
python -m unittest discover -s tests -t . -v
```
'''
    DOCUMENTACION_PATH.write_text(contenido, encoding="utf-8")


def main() -> None:
    resultados = construir_resultados()
    escribir_csv(resultados)
    escribir_documentacion(resultados)
    print()
    print(f"CSV generado: {RESULTADOS_PATH.relative_to(ROOT)}")
    print(f"Documentación actualizada: {DOCUMENTACION_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
