"""Categoría del catálogo; los juegos se guardan en las hojas del árbol."""

from dataclasses import dataclass, field

from modelos.videojuego import Videojuego


@dataclass(slots=True)
class Categoria:
    nombre: str
    videojuegos: list[Videojuego] = field(default_factory=list)
