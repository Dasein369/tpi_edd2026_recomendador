from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from modelos.videojuego import Videojuego


@dataclass(slots=True)
class NodoArbol:
    """Nodo de un árbol binario de búsqueda por título."""

    videojuego: Videojuego
    izquierda: NodoArbol | None = None
    derecha: NodoArbol | None = None


class ArbolBinarioBusqueda:
    """Árbol binario de búsqueda dinámico ordenado por título.

    Cada videojuego se incorpora mediante inserción, sin ordenar ni balancear los
    datos al construir el árbol. La comparación de títulos no distingue mayúsculas.
    Las claves repetidas se insertan a la derecha para conservar todos los juegos.
    """

    def __init__(self, videojuegos: Iterable[Videojuego] = ()) -> None:
        self._raiz: NodoArbol | None = None
        self._tam = 0
        for videojuego in videojuegos:
            self.insertar(videojuego)

    @staticmethod
    def _clave(videojuego: Videojuego) -> str:
        return videojuego.titulo.casefold()

    def insertar(self, videojuego: Videojuego) -> None:
        """Inserta un juego en O(h), donde h es la altura actual del árbol."""
        clave = self._clave(videojuego)
        nuevo = NodoArbol(videojuego)

        if self._raiz is None:
            self._raiz = nuevo
            self._tam = 1
            return

        actual = self._raiz
        while True:
            clave_actual = self._clave(actual.videojuego)

            if clave < clave_actual:
                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    self._tam += 1
                    return
                actual = actual.izquierda
            else:
                if actual.derecha is None:
                    actual.derecha = nuevo
                    self._tam += 1
                    return
                actual = actual.derecha

    def buscar(self, titulo: str) -> Videojuego | None:
        """Busca por título en O(h): O(log n) promedio y O(n) en el peor caso."""
        objetivo = titulo.casefold()
        actual = self._raiz

        while actual is not None:
            clave_actual = self._clave(actual.videojuego)
            if objetivo == clave_actual:
                return actual.videojuego
            actual = actual.izquierda if objetivo < clave_actual else actual.derecha

        return None

    def inorder(self) -> list[Videojuego]:
        """Recorre izquierda-raíz-derecha y devuelve los juegos por título."""
        resultado: list[Videojuego] = []
        pila: list[NodoArbol] = []
        actual = self._raiz

        while actual is not None or pila:
            while actual is not None:
                pila.append(actual)
                actual = actual.izquierda
            actual = pila.pop()
            resultado.append(actual.videojuego)
            actual = actual.derecha

        return resultado

    def preorder(self) -> list[Videojuego]:
        """Recorre raíz-izquierda-derecha."""
        if self._raiz is None:
            return []

        resultado: list[Videojuego] = []
        pila = [self._raiz]
        while pila:
            actual = pila.pop()
            resultado.append(actual.videojuego)
            if actual.derecha is not None:
                pila.append(actual.derecha)
            if actual.izquierda is not None:
                pila.append(actual.izquierda)

        return resultado

    def postorder(self) -> list[Videojuego]:
        """Recorre izquierda-derecha-raíz."""
        resultado: list[Videojuego] = []
        pila: list[tuple[NodoArbol, bool]] = []
        if self._raiz is not None:
            pila.append((self._raiz, False))

        while pila:
            actual, visitado = pila.pop()
            if visitado:
                resultado.append(actual.videojuego)
                continue
            pila.append((actual, True))
            if actual.derecha is not None:
                pila.append((actual.derecha, False))
            if actual.izquierda is not None:
                pila.append((actual.izquierda, False))

        return resultado

    def altura(self) -> int:
        """Devuelve la cantidad de niveles; un árbol vacío tiene altura cero."""
        if self._raiz is None:
            return 0

        altura = 0
        nivel = [self._raiz]
        while nivel:
            altura += 1
            siguiente: list[NodoArbol] = []
            for nodo in nivel:
                if nodo.izquierda is not None:
                    siguiente.append(nodo.izquierda)
                if nodo.derecha is not None:
                    siguiente.append(nodo.derecha)
            nivel = siguiente

        return altura

    def __len__(self) -> int:
        return self._tam
