"""Compara el BST de TP3 con el AVL de TP4 ante entradas que desbalancean.

Desde la raíz del proyecto: ``python -m experimentos.benchmark_tp4``.

Se miden dos tipos de magnitud:
  * Estructurales y deterministas (altura, pasos de búsqueda, rotaciones): no dependen
    del equipo y son la evidencia principal sobre el orden de crecimiento.
  * Tiempos (construcción y búsqueda): dependen del equipo e intérprete, sirven como
    observación complementaria.

Ambos árboles comparan igual (``titulo.casefold()`` en cada paso), de modo que la
diferencia de tiempos se debe a la forma del árbol y no a trucos de implementación.
"""

from __future__ import annotations

import csv
import json
import math
import random
import statistics
import time
from collections.abc import Callable
from pathlib import Path

from estructuras.arbol_avl import ArbolAVL
from estructuras.arbol_binario_busqueda import ArbolBinarioBusqueda
from modelos.videojuego import Videojuego


ROOT = Path(__file__).resolve().parents[1]
TAMANOS = (100, 1_000, 5_000, 10_000)
TAMANO_SOLO_AVL = 100_000
ESCENARIOS = ("ascendente", "descendente", "zigzag", "casi_ordenado", "aleatorio")
MUESTRA_BUSQUEDAS = 500
REPETICIONES = 5
SEMILLA = 2026
CSV_PATH = ROOT / "experimentos" / "resultados_tp4.csv"
DOC_PATH = ROOT / "docs" / "tp4-avl.md"

DESCRIPCION_ESCENARIOS = {
    "ascendente": "Títulos ya ordenados de la A a la Z (catálogo exportado alfabéticamente).",
    "descendente": "Títulos ordenados de la Z a la A.",
    "zigzag": "Se alterna el menor y el mayor que quedan: A, Z, B, Y, C, X…",
    "casi_ordenado": "Ordenados, con el 5 % de los títulos intercambiados con un vecino cercano.",
    "aleatorio": "Orden mezclado con semilla fija (caso favorable, grupo de control).",
}


# --------------------------------------------------------------------------- datos


def cargar_videojuegos_base() -> list[Videojuego]:
    with (ROOT / "datos" / "videojuegos.json").open(encoding="utf-8") as archivo:
        datos = json.load(archivo)
    elementos = datos.get("videojuegos", datos) if isinstance(datos, dict) else datos
    return [Videojuego(**item) for item in elementos]


def generar_videojuegos(base: list[Videojuego], cantidad: int) -> list[Videojuego]:
    """Videojuegos con títulos únicos, a partir del dataset real."""
    return [
        Videojuego(
            id=indice + 1,
            titulo=f"{base[indice % len(base)].titulo} [TP4-{indice + 1:06d}]",
            genero=base[indice % len(base)].genero,
            desarrollador=base[indice % len(base)].desarrollador,
            rating=base[indice % len(base)].rating,
            horas_jugadas=base[indice % len(base)].horas_jugadas,
        )
        for indice in range(cantidad)
    ]


def ordenar_para_escenario(escenario: str, videojuegos: list[Videojuego], semilla: int) -> list[Videojuego]:
    """Devuelve los videojuegos en el orden de inserción propio del escenario."""
    ordenados = sorted(videojuegos, key=lambda v: v.titulo.casefold())
    n = len(ordenados)

    if escenario == "ascendente":
        return ordenados
    if escenario == "descendente":
        return ordenados[::-1]
    if escenario == "zigzag":
        return [ordenados[i // 2] if i % 2 == 0 else ordenados[n - 1 - i // 2] for i in range(n)]
    if escenario == "casi_ordenado":
        resultado = ordenados.copy()
        azar = random.Random(semilla)
        for _ in range(max(1, n // 20)):
            i = azar.randrange(n)
            j = min(n - 1, i + azar.randint(1, 10))
            resultado[i], resultado[j] = resultado[j], resultado[i]
        return resultado
    if escenario == "aleatorio":
        resultado = ordenados.copy()
        random.Random(semilla).shuffle(resultado)
        return resultado
    raise ValueError(f"Escenario desconocido: {escenario}")


# ------------------------------------------------------------------------- medición


def altura_minima(n: int) -> int:
    """Menor altura posible (en niveles) para un árbol binario de n nodos."""
    return math.ceil(math.log2(n + 1))


def cota_avl(n: int) -> int:
    """Máximo de niveles de un AVL con n nodos: ⌊1,4405·log2(n+2) - 0,3277⌋."""
    return math.floor(1.4405 * math.log2(n + 2) - 0.3277)


def medir_construccion_ms(construir: Callable[[], object], repeticiones: int) -> tuple[object, float]:
    """Construye el árbol ``repeticiones`` veces; devuelve el último y la mediana en ms."""
    tiempos: list[float] = []
    arbol: object = None
    for _ in range(repeticiones):
        inicio = time.perf_counter_ns()
        arbol = construir()
        tiempos.append((time.perf_counter_ns() - inicio) / 1_000_000)
    return arbol, statistics.median(tiempos)


def medir_busqueda_ns(arbol, muestra: list[str]) -> float:
    """Mediana de ns por búsqueda sobre una muestra de títulos existentes."""
    # Los árboles degenerados ya son lentos: una sola pasada alcanza para medirlos.
    pasadas = 1 if arbol.altura() > 1_000 else 5
    buscar = arbol.buscar
    for titulo in muestra:  # calentamiento
        buscar(titulo)

    mediciones: list[float] = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter_ns()
        for _ in range(pasadas):
            for titulo in muestra:
                buscar(titulo)
        mediciones.append((time.perf_counter_ns() - inicio) / (pasadas * len(muestra)))
    return statistics.median(mediciones)


def pasos_promedio(arbol, muestra: list[str]) -> float:
    return sum(arbol.pasos_busqueda(titulo) for titulo in muestra) / len(muestra)


def medir_escenario(escenario: str, cantidad: int, videojuegos: list[Videojuego]) -> dict:
    entrada = ordenar_para_escenario(escenario, videojuegos, SEMILLA + cantidad)
    muestra = [
        v.titulo for v in random.Random(SEMILLA).sample(videojuegos, min(MUESTRA_BUSQUEDAS, cantidad))
    ]
    repeticiones = 3 if cantidad <= 1_000 else 1

    bst, construccion_bst = medir_construccion_ms(lambda: ArbolBinarioBusqueda(entrada), repeticiones)
    avl, construccion_avl = medir_construccion_ms(lambda: ArbolAVL(entrada), repeticiones)

    # Validación cruzada: ambos árboles deben devolver lo mismo.
    assert [v.id for v in bst.inorder()] == [v.id for v in avl.inorder()]
    assert avl.es_valido()

    return {
        "escenario": escenario,
        "elementos": cantidad,
        "altura_minima": altura_minima(cantidad),
        "altura_bst": bst.altura(),
        "altura_avl": avl.altura(),
        "pasos_promedio_bst": round(pasos_promedio(bst, muestra), 1),
        "pasos_promedio_avl": round(pasos_promedio(avl, muestra), 1),
        "busqueda_bst_ns": round(medir_busqueda_ns(bst, muestra), 1),
        "busqueda_avl_ns": round(medir_busqueda_ns(avl, muestra), 1),
        "construccion_bst_ms": round(construccion_bst, 2),
        "construccion_avl_ms": round(construccion_avl, 2),
        "rotaciones_avl": avl.rotaciones,
    }


def medir_solo_avl(videojuegos: list[Videojuego]) -> dict:
    """Escala donde el BST degenerado ya no es práctico de construir (≈ n²/2 pasos)."""
    n = len(videojuegos)
    entrada = ordenar_para_escenario("ascendente", videojuegos, SEMILLA)
    muestra = [v.titulo for v in random.Random(SEMILLA).sample(videojuegos, MUESTRA_BUSQUEDAS)]
    avl, construccion = medir_construccion_ms(lambda: ArbolAVL(entrada), 1)
    assert avl.es_valido()
    return {
        "escenario": "ascendente",
        "elementos": n,
        "altura_minima": altura_minima(n),
        "altura_bst": "",
        "altura_avl": avl.altura(),
        "pasos_promedio_bst": "",
        "pasos_promedio_avl": round(pasos_promedio(avl, muestra), 1),
        "busqueda_bst_ns": "",
        "busqueda_avl_ns": round(medir_busqueda_ns(avl, muestra), 1),
        "construccion_bst_ms": "",
        "construccion_avl_ms": round(construccion, 2),
        "rotaciones_avl": avl.rotaciones,
    }


def construir_resultados() -> list[dict]:
    base = cargar_videojuegos_base()
    resultados: list[dict] = []

    for cantidad in TAMANOS:
        videojuegos = generar_videojuegos(base, cantidad)
        for escenario in ESCENARIOS:
            print(f"  {escenario:>13} n={cantidad:>7,} ...", flush=True)
            resultados.append(medir_escenario(escenario, cantidad, videojuegos))

    print(f"  {'ascendente':>13} n={TAMANO_SOLO_AVL:>7,} (solo AVL) ...", flush=True)
    resultados.append(medir_solo_avl(generar_videojuegos(base, TAMANO_SOLO_AVL)))
    return resultados


# ---------------------------------------------------------------------- salida


def escribir_csv(resultados: list[dict]) -> None:
    with CSV_PATH.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(resultados[0]))
        escritor.writeheader()
        escritor.writerows(resultados)


def numero_espanol(valor: int | float | str, decimales: int = 1) -> str:
    if valor == "":
        return "—"
    formateado = f"{valor:,.{decimales}f}"
    return formateado.replace(",", "_").replace(".", ",").replace("_", ".")


def escribir_documentacion(resultados: list[dict]) -> None:
    n = numero_espanol
    comparados = [f for f in resultados if f["altura_bst"] != ""]
    solo_avl = next(f for f in resultados if f["altura_bst"] == "")
    mayor = max(TAMANOS)

    def fila_de(escenario: str, cantidad: int) -> dict:
        return next(f for f in comparados if f["escenario"] == escenario and f["elementos"] == cantidad)

    asc = fila_de("ascendente", mayor)
    ale = fila_de("aleatorio", mayor)
    casi = fila_de("casi_ordenado", mayor)

    exceso_max = max(f["altura_avl"] - f["altura_minima"] for f in comparados + [solo_avl])
    factor_construccion_aleatorio = ale["construccion_avl_ms"] / ale["construccion_bst_ms"]

    tabla_alturas = "\n".join(
        f"| {f['escenario']} | {n(f['elementos'], 0)} | {f['altura_minima']} | {f['altura_bst']} | "
        f"{f['altura_avl']} | {cota_avl(f['elementos'])} |"
        for f in comparados
    )
    tabla_pasos = "\n".join(
        f"| {f['escenario']} | {n(f['elementos'], 0)} | {n(f['pasos_promedio_bst'])} | "
        f"{n(f['pasos_promedio_avl'])} | {n(f['busqueda_bst_ns'])} | {n(f['busqueda_avl_ns'])} | "
        f"{n(f['busqueda_bst_ns'] / f['busqueda_avl_ns'], 1)}× |"
        for f in comparados
    )
    tabla_construccion = "\n".join(
        f"| {f['escenario']} | {n(f['elementos'], 0)} | {n(f['construccion_bst_ms'], 2)} | "
        f"{n(f['construccion_avl_ms'], 2)} | {n(f['rotaciones_avl'], 0)} | "
        f"{n(f['rotaciones_avl'] / f['elementos'], 2)} |"
        for f in comparados
    )
    lista_escenarios = "\n".join(f"- **{k}**: {v}" for k, v in DESCRIPCION_ESCENARIOS.items())
    comparaciones_bst_100k = TAMANO_SOLO_AVL * (TAMANO_SOLO_AVL - 1) // 2

    contenido = f"""# TP4 — AVL frente al BST desbalanceado

## 1. El problema: la forma del BST depende del orden de inserción

El BST de TP3 no se reorganiza: cada título nuevo cuelga de la hoja que le toca y ahí
queda. Si los títulos llegan ya ordenados, cada nuevo es mayor que todos los anteriores
y siempre baja por la derecha: el árbol se convierte en una **lista enlazada** de altura
`n`. La búsqueda pasa de `O(log n)` a `O(n)` y construir el árbol pasa de `O(n log n)` a
`O(n²)`.

No es un caso exótico. Un catálogo exportado alfabéticamente, una base ordenada por
título o un archivo que ya viene ordenado producen exactamente esta entrada.

```
Insertar A, B, C, D, E (en ese orden)

BST (TP3)                    AVL (TP4)

A                                B
 \\                              / \\
  B                            A   D
   \\                            / \\
    C                          C   E
     \\
      D          altura 5               altura 3
       \\
        E
```

## 2. Escenarios de desbalance generados

`experimentos/benchmark_tp4.py` arma cinco órdenes de inserción para el mismo conjunto
de títulos únicos (construidos a partir de `datos/videojuegos.json`):

{lista_escenarios}

## 3. AVL: invariante y rotaciones

Un árbol AVL es un BST que cumple, **en cada nodo**, que las alturas de sus subárboles
izquierdo y derecho difieren a lo sumo en 1. El *factor de balance*
`altura(izq) − altura(der)` solo puede valer −1, 0 o +1. La altura de cada subárbol se
guarda en el nodo (`NodoAVL.altura`), así que calcular el balance cuesta `O(1)`.

Tras insertar, se vuelve por el camino hacia la raíz actualizando alturas. El primer
nodo cuyo factor llega a ±2 se corrige con una rotación, que reordena unos pocos
enlaces en `O(1)` **sin alterar el orden inorder** (el árbol sigue siendo un BST válido).
Hay cuatro casos:

| Caso | Se detecta cuando | Corrección |
|---|---|---|
| Izquierda-izquierda | factor del nodo = +2 y de su hijo izquierdo ≥ 0 | rotación simple a la derecha |
| Derecha-derecha | factor del nodo = −2 y de su hijo derecho ≤ 0 | rotación simple a la izquierda |
| Izquierda-derecha | factor del nodo = +2 y de su hijo izquierdo < 0 | rotación izquierda del hijo, luego derecha del nodo |
| Derecha-izquierda | factor del nodo = −2 y de su hijo derecho > 0 | rotación derecha del hijo, luego izquierda del nodo |

```
Rotación simple a la derecha (LL)          Rotación doble izquierda-derecha (LR)

      y               x                      z             z               y
     / \\             / \\                    /             /              /   \\
    x   C    -->    A   y                  x      -->    y      -->     x     z
   / \\                 / \\                  \\            /
  A   B               B   C                  y          x
```

Una inserción provoca como máximo una corrección (simple o doble), pero se revisa el
balance en todos los nodos del camino de vuelta: `O(log n)` en total.

Implementación: `estructuras/arbol_avl.py`, con `_rotar_derecha`, `_rotar_izquierda` y
`_rebalancear`. El método `es_valido()` recalcula todo el árbol desde cero y se usa en
las pruebas para verificar el invariante tras cada inserción.

### Decisiones de diseño

- **Misma interfaz que el BST** (`insertar`, `buscar`, recorridos, `altura`, `len`),
  por lo que el catálogo cambió de estructura modificando solo la línea que la crea.
  `Catalogo.buscar()` ahora consulta el AVL.
- **Títulos repetidos.** Se desempata por orden de inserción, lo que da un orden total y
  estable que las rotaciones no alteran. `buscar` devuelve siempre el primer título
  insertado, igual que el BST de TP3. Esto mantiene válidas las pruebas de carga
  repetida de TP3.
- **Comparación idéntica** a la del BST (`casefold()` en cada paso) para que el
  experimento compare formas de árbol y no detalles de implementación.

## 4. Complejidad teórica

Sea `n` la cantidad de videojuegos y `h` la altura del árbol.

| Operación | BST (TP3) | AVL (TP4) |
|---|---:|---:|
| Altura | entre ⌈log₂(n+1)⌉ y n | siempre ≤ 1,44·log₂(n+2) |
| Buscar | O(h): O(log n) promedio, **O(n) peor caso** | **O(log n) garantizado** |
| Insertar | O(h): O(log n) promedio, **O(n) peor caso** | **O(log n) garantizado** |
| Construir con n inserciones | O(n log n) promedio, **O(n²) peor caso** | **O(n log n) garantizado** |
| Rotaciones por inserción | no tiene | O(1) amortizado, máximo 2 |
| Espacio | O(n) | O(n) (un entero extra por nodo) |

## 5. Resultados

Cada escenario se mide con `n` = {", ".join(n(t, 0) for t in TAMANOS)} títulos. Las
búsquedas usan una muestra fija de {MUESTRA_BUSQUEDAS} títulos existentes elegidos al
azar; los pasos son nodos visitados (comparaciones). Los tiempos son la mediana de
{REPETICIONES} tandas (la construcción, de 3 repeticiones hasta 1.000 elementos y 1 en
adelante) y dependen del equipo.

### 5.1 Altura

La altura mínima posible para `n` nodos es ⌈log₂(n+1)⌉. La última columna es el máximo
que la teoría permite a un AVL.

| Escenario | Elementos | Altura mínima | Altura BST | Altura AVL | Cota AVL |
|---|---:|---:|---:|---:|---:|
{tabla_alturas}

### 5.2 Búsqueda

| Escenario | Elementos | Pasos prom. BST | Pasos prom. AVL | BST (ns/búsqueda) | AVL (ns/búsqueda) | BST / AVL |
|---|---:|---:|---:|---:|---:|---:|
{tabla_pasos}

### 5.3 Construcción

| Escenario | Elementos | Construir BST (ms) | Construir AVL (ms) | Rotaciones AVL | Rotaciones por inserción |
|---|---:|---:|---:|---:|---:|
{tabla_construccion}

### 5.4 Una escala donde el BST degenerado ya no es práctico

Con {n(TAMANO_SOLO_AVL, 0)} títulos ya ordenados, el BST necesitaría
{n(comparaciones_bst_100k, 0)} comparaciones solo para construirse (`n(n−1)/2`), por lo
que no se ejecuta. El AVL, en cambio, lo construye en
{n(solo_avl['construccion_avl_ms'], 0)} ms con altura {solo_avl['altura_avl']} (mínima posible:
{solo_avl['altura_minima']}), {n(solo_avl['rotaciones_avl'], 0)} rotaciones y
{n(solo_avl['pasos_promedio_avl'])} pasos promedio por búsqueda.

## 6. Por qué importa el balance

El costo de buscar en un árbol de búsqueda es la cantidad de niveles que hay que bajar,
o sea su altura. Cada comparación descarta un subárbol; que ese subárbol sea la mitad
de los nodos o apenas uno depende de la forma del árbol:

- **Árbol balanceado:** cada comparación descarta aproximadamente la mitad de los nodos,
  así que alcanzan `log₂ n` pasos. Con un millón de títulos son unos 20 pasos.
- **Árbol degenerado:** cada comparación descarta un solo nodo, así que hay que recorrer
  hasta `n`. Con un millón de títulos son hasta un millón de pasos, igual que una búsqueda
  secuencial. Todo lo que se ganó con el árbol se pierde.

Los resultados lo confirman. Con {n(mayor, 0)} títulos ordenados, el BST alcanzó altura
**{n(asc['altura_bst'], 0)}** y {n(asc['pasos_promedio_bst'])} pasos promedio por búsqueda, contra
**{asc['altura_avl']}** y {n(asc['pasos_promedio_avl'])} del AVL. Con entrada aleatoria el BST llegó a
altura {ale['altura_bst']} y {n(ale['pasos_promedio_bst'])} pasos promedio, contra altura {ale['altura_avl']} y
{n(ale['pasos_promedio_avl'])} del AVL: con orden aleatorio el BST se defiende bien en promedio, aunque su peor
rama sigue siendo más profunda. **El BST rinde solo si el orden de entrada tiene suerte**, y
el catálogo no controla en qué orden llegan los datos. El escenario `casi_ordenado` muestra que no hace falta
una entrada perfectamente ordenada para sufrir: con solo el 5 % de títulos
desordenados, el BST llegó a altura {n(casi['altura_bst'], 0)} frente a {casi['altura_avl']} del AVL.

### Por qué el AVL garantiza `O(log n)`

Sea `N(h)` la mínima cantidad de nodos de un AVL de altura `h`. El árbol más escaso
tiene un subárbol de altura `h−1` y otro de altura `h−2`, así que
`N(h) = N(h−1) + N(h−2) + 1`. Es la recurrencia de Fibonacci: `N(h)` crece como
`φ^h` con `φ ≈ 1,618`. Despejando, `h ≤ 1,44·log₂(n+2)`. Es decir, la altura de un AVL
es `O(log n)` **para cualquier orden de inserción**, y como búsqueda e inserción cuestan
`O(h)`, ambas son `O(log n)` en el peor caso y no solo en promedio.

## 7. Costos y límites del AVL

- **Más trabajo por inserción.** Cada inserción actualiza alturas en el camino de vuelta
  y puede rotar. Con entrada aleatoria el BST ya queda razonablemente balanceado y el
  AVL no mejora de forma apreciable los pasos promedio, pero construirlo tomó
  {n(factor_construccion_aleatorio, 1)}× más tiempo que el BST ({n(ale['construccion_avl_ms'], 1)} ms contra
  {n(ale['construccion_bst_ms'], 1)} ms con {n(mayor, 0)} títulos). Lo que se paga es la garantía.
- **Más memoria.** Un entero extra (la altura) por nodo.
- **Más complejidad de código.** Cuatro casos de rotación que hay que probar con cuidado.
- **Comparación con TP2.** El árbol estático de TP2 también tiene altura mínima, pero se
  construye ordenando los datos de una vez y no admite inserciones sin reconstruirse. El
  AVL logra esa altura de forma incremental, que es lo que necesita un catálogo que
  recibe cargas repetidas.

## 8. Conclusión

1. El BST de TP3 depende del orden de los datos: con entradas ordenadas, descendentes o
   en zigzag, su altura es `n` y su costo de búsqueda e inserción es `O(n)`, el mismo
   de la búsqueda secuencial.
2. El AVL mantiene la altura en `O(log n)` con rotaciones de costo constante, sin
   importar el orden de entrada: en todos los escenarios medidos su altura está dentro
   de la cota teórica y a no más de {exceso_max} niveles de la mínima posible.
3. La garantía tiene un precio pequeño (una altura por nodo y algo de trabajo extra al
   insertar), muy inferior al riesgo de que el catálogo degenere. Como la carga del
   catálogo no controla el orden de los datos, el proyecto adopta el AVL para la
   búsqueda por título.

Para repetir el experimento desde la raíz (tarda alrededor de un minuto por los casos
degenerados del BST):

```bash
python -m experimentos.benchmark_tp4
```

El comando actualiza `experimentos/resultados_tp4.csv` y este documento.
"""
    DOC_PATH.write_text(contenido, encoding="utf-8")


def main() -> None:
    print("Ejecutando experimento TP4 (BST vs AVL)...")
    resultados = construir_resultados()
    escribir_csv(resultados)
    escribir_documentacion(resultados)
    print(f"CSV generado: {CSV_PATH.relative_to(ROOT)}")
    print(f"Documentación actualizada: {DOC_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
