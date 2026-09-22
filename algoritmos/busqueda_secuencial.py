from collections.abc import Sequence

from modelos.videojuego import Videojuego


def buscar_secuencial(videojuegos: Sequence[Videojuego], titulo: str) -> Videojuego | None:
    """Busca un videojuego recorriendo la secuencia desde el principio.

    Complejidad temporal:
        - Mejor caso: Ω(1), si el elemento está primero.
        - Caso promedio: Θ(n).
        - Peor caso: O(n), si está al final o no existe.

    Complejidad espacial adicional: O(1).
    """
    objetivo = titulo.casefold()

    for videojuego in videojuegos:
        if videojuego.titulo.casefold() == objetivo:
            return videojuego

    return None
