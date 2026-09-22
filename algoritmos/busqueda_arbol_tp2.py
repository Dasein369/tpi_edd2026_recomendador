from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

from modelos.videojuego import Videojuego


@dataclass(slots=True)
class NodoBusqueda:
    """Nodo de un árbol binario de búsqueda estático y balanceado."""

    videojuego: Videojuego
    izquierda: NodoBusqueda | None = None
    derecha: NodoBusqueda | None = None


class ArbolBusquedaBalanceada:
    """BST estático balanceado usado exclusivamente para el experimento del TP2.

    El árbol se construye ordenando los datos y tomando recursivamente el elemento
    central. De esta forma, para cada tamaño probado la altura es O(log n) y la
    búsqueda puede analizarse como Θ(log n).

    Importante: esta estructura NO reemplaza todavía al BST dinámico del TP3.
    En TP3 podrá trasladarse/refactorizarse a la carpeta `estructuras/` para
    incorporar inserción y recorridos dentro de la aplicación.
    """

    def __init__(self, videojuegos: Iterable[Videojuego] = ()) -> None:
        elementos = list(videojuegos)
        elementos.sort(key=self._clave)

        claves = [self._clave(v) for v in elementos]
        if len(claves) != len(set(claves)):
            raise ValueError("El árbol del experimento requiere títulos únicos.")

        self._raiz = self._construir(elementos, 0, len(elementos) - 1)
        self._tam = len(elementos)

    @staticmethod
    def _clave(videojuego: Videojuego) -> str:
        return videojuego.titulo.casefold()

    @classmethod
    def _construir(
        cls,
        elementos: list[Videojuego],
        inicio: int,
        fin: int,
    ) -> NodoBusqueda | None:
        if inicio > fin:
            return None

        medio = (inicio + fin) // 2
        nodo = NodoBusqueda(elementos[medio])
        nodo.izquierda = cls._construir(elementos, inicio, medio - 1)
        nodo.derecha = cls._construir(elementos, medio + 1, fin)
        return nodo

    def buscar(self, titulo: str) -> Videojuego | None:
        """Busca por título navegando izquierda/derecha según el orden alfabético.

        En este árbol balanceado: Ω(1) mejor caso y Θ(log n) promedio/peor caso.
        """
        objetivo = titulo.casefold()
        actual = self._raiz

        while actual is not None:
            clave_actual = self._clave(actual.videojuego)

            if objetivo == clave_actual:
                return actual.videojuego

            if objetivo < clave_actual:
                actual = actual.izquierda
            else:
                actual = actual.derecha

        return None

    def altura(self) -> int:
        """Devuelve la altura en cantidad de niveles; árbol vacío = 0."""
        def calcular(nodo: NodoBusqueda | None) -> int:
            if nodo is None:
                return 0
            return 1 + max(calcular(nodo.izquierda), calcular(nodo.derecha))

        return calcular(self._raiz)

    def inorder(self) -> list[Videojuego]:
        """Devuelve los elementos en orden alfabético; útil para tests."""
        resultado: list[Videojuego] = []

        def recorrer(nodo: NodoBusqueda | None) -> None:
            if nodo is None:
                return
            recorrer(nodo.izquierda)
            resultado.append(nodo.videojuego)
            recorrer(nodo.derecha)

        recorrer(self._raiz)
        return resultado

    def __len__(self) -> int:
        return self._tam
