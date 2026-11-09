"""Reglas del dominio para relacionar videojuegos y construir el grafo (TP7)."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from estructuras.grafo import Grafo
from modelos.videojuego import Videojuego


PESO_MISMO_GENERO = 3
PESO_MISMO_DESARROLLADOR = 2
PESO_MISMA_FAMILIA = 1


@dataclass(frozen=True, slots=True)
class Relacion:
    """Resultado de comparar dos juegos: peso total y motivos que lo explican."""

    peso: int
    motivos: tuple[str, ...]


def calcular_relacion(
    a: Videojuego, b: Videojuego, familia_de: Mapping[str, str]
) -> Relacion | None:
    """Devuelve la relación entre dos juegos, o None si no comparten nada.

    Suma puntos por cada criterio compartido:
    - mismo género: 3 (la afinidad más fuerte);
    - mismo desarrollador: 2;
    - misma familia de géneros pero distinto género: 1 (jerarquía de TP5).

    ``familia_de`` mapea ``genero.casefold()`` a su familia. Es O(1) y simétrica:
    ``calcular_relacion(a, b) == calcular_relacion(b, a)``.
    """
    peso = 0
    motivos: list[str] = []

    genero_a, genero_b = a.genero.casefold(), b.genero.casefold()
    if genero_a == genero_b:
        peso += PESO_MISMO_GENERO
        motivos.append(f"mismo género ({a.genero})")
    else:
        familia_a = familia_de.get(genero_a)
        if familia_a is not None and familia_a == familia_de.get(genero_b):
            peso += PESO_MISMA_FAMILIA
            motivos.append(f"misma familia ({familia_a})")

    if a.desarrollador.casefold() == b.desarrollador.casefold():
        peso += PESO_MISMO_DESARROLLADOR
        motivos.append(f"mismo desarrollador ({a.desarrollador})")

    if peso == 0:
        return None
    return Relacion(peso, tuple(motivos))


def construir_grafo(
    videojuegos: Sequence[Videojuego], familia_de: Mapping[str, str]
) -> Grafo[Videojuego]:
    """Arma el grafo de relaciones: un vértice por juego, una arista por par relacionado.

    Compara cada par una sola vez, por lo que cuesta O(n²) y se paga al cargar el
    catálogo, no en cada consulta. Es razonable para catálogos de cientos de juegos;
    para catálogos mucho mayores convendría agrupar por género y desarrollador y
    comparar solo dentro de cada grupo.
    """
    grafo: Grafo[Videojuego] = Grafo()
    for videojuego in videojuegos:
        grafo.agregar_vertice(videojuego)

    for i, a in enumerate(videojuegos):
        for b in videojuegos[i + 1:]:
            relacion = calcular_relacion(a, b, familia_de)
            if relacion is not None:
                grafo.agregar_arista(a, b, relacion.peso)
    return grafo
