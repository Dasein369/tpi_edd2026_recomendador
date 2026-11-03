"""Montículo binario máximo implementado sobre una lista dinámica."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class _Entrada(Generic[T]):
    prioridad: Any
    orden: int
    valor: T


class MonticuloMaximo(Generic[T]):
    """Cola de prioridad máxima con desempate estable por orden de inserción.

    La construcción desde un iterable usa heapify bottom-up en O(n). Los
    elementos con igual prioridad se extraen en el mismo orden en que entraron.
    """

    def __init__(
        self,
        elementos: Iterable[T] = (),
        prioridad: Callable[[T], Any] | None = None,
    ) -> None:
        self._prioridad = prioridad if prioridad is not None else (lambda valor: valor)
        self._entradas = [
            _Entrada(self._prioridad(valor), orden, valor)
            for orden, valor in enumerate(elementos)
        ]
        self._siguiente_orden = len(self._entradas)

        for indice in range(len(self._entradas) // 2 - 1, -1, -1):
            self._bajar(indice)

    def insertar(self, valor: T) -> None:
        """Agrega un elemento en O(log n)."""
        entrada = _Entrada(self._prioridad(valor), self._siguiente_orden, valor)
        self._siguiente_orden += 1
        self._entradas.append(entrada)
        self._subir(len(self._entradas) - 1)

    def ver_maximo(self) -> T:
        """Devuelve el elemento prioritario sin quitarlo."""
        if not self._entradas:
            raise IndexError("el montículo está vacío")
        return self._entradas[0].valor

    def extraer_maximo(self) -> T:
        """Quita y devuelve el elemento prioritario en O(log n)."""
        if not self._entradas:
            raise IndexError("el montículo está vacío")

        maximo = self._entradas[0].valor
        ultimo = self._entradas.pop()
        if self._entradas:
            self._entradas[0] = ultimo
            self._bajar(0)
        return maximo

    def mayores(self, cantidad: int) -> list[T]:
        """Devuelve los primeros N sin modificar el montículo.

        Recorre los nodos del montículo usando una segunda cola de candidatos,
        que contiene como máximo N posiciones. El costo es O(N log N), luego de
        la construcción O(n), sin copiar ni ordenar el catálogo completo.
        """
        if cantidad < 0:
            raise ValueError("la cantidad no puede ser negativa")
        if cantidad == 0 or not self._entradas:
            return []

        cantidad = min(cantidad, len(self._entradas))
        candidatos: MonticuloMaximo[tuple[Any, int, int]] = MonticuloMaximo(
            prioridad=lambda candidato: (candidato[0], candidato[1])
        )
        raiz = self._entradas[0]
        candidatos.insertar((raiz.prioridad, -raiz.orden, 0))
        resultado: list[T] = []

        for _ in range(cantidad):
            _, _, indice = candidatos.extraer_maximo()
            entrada = self._entradas[indice]
            resultado.append(entrada.valor)

            for hijo in (2 * indice + 1, 2 * indice + 2):
                if hijo < len(self._entradas):
                    candidato = self._entradas[hijo]
                    candidatos.insertar((candidato.prioridad, -candidato.orden, hijo))

        return resultado

    def _es_mayor(self, izquierda: _Entrada[T], derecha: _Entrada[T]) -> bool:
        if izquierda.prioridad != derecha.prioridad:
            return izquierda.prioridad > derecha.prioridad
        return izquierda.orden < derecha.orden

    def _subir(self, indice: int) -> None:
        while indice > 0:
            padre = (indice - 1) // 2
            if not self._es_mayor(self._entradas[indice], self._entradas[padre]):
                break
            self._entradas[indice], self._entradas[padre] = (
                self._entradas[padre], self._entradas[indice]
            )
            indice = padre

    def _bajar(self, indice: int) -> None:
        cantidad = len(self._entradas)
        while True:
            izquierdo = 2 * indice + 1
            derecho = izquierdo + 1
            mayor = indice

            if izquierdo < cantidad and self._es_mayor(
                self._entradas[izquierdo], self._entradas[mayor]
            ):
                mayor = izquierdo
            if derecho < cantidad and self._es_mayor(
                self._entradas[derecho], self._entradas[mayor]
            ):
                mayor = derecho
            if mayor == indice:
                return

            self._entradas[indice], self._entradas[mayor] = (
                self._entradas[mayor], self._entradas[indice]
            )
            indice = mayor

    def __len__(self) -> int:
        return len(self._entradas)
