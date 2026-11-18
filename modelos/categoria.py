"""Categoría del catálogo; los juegos se guardan en las hojas del árbol."""

from modelos.videojuego import Videojuego


class Categoria:
    """Nodo de la jerarquía de géneros: un nombre y los juegos que contiene."""

    __slots__ = ("nombre", "videojuegos")

    def __init__(self, nombre: str, videojuegos: list[Videojuego] | None = None) -> None:
        self.nombre = nombre
        self.videojuegos = videojuegos if videojuegos is not None else []

    def __repr__(self) -> str:
        return f"Categoria(nombre={self.nombre!r}, videojuegos={self.videojuegos!r})"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Categoria):
            return NotImplemented
        return self.nombre == otro.nombre and self.videojuegos == otro.videojuegos

    # Es mutable (la lista de juegos cambia), así que no puede ser hashable.
    __hash__ = None