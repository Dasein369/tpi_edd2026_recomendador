"""Grafo no dirigido y pesado implementado con lista de adyacencia."""

from collections import deque
from collections.abc import Hashable, Iterator
from typing import Generic, TypeVar


V = TypeVar("V", bound=Hashable)


class Grafo(Generic[V]):
    """Grafo no dirigido y pesado, representado con una lista de adyacencia.

    Cada vértice guarda un diccionario ``{vecino: peso}``. Una arista entre
    ``a`` y ``b`` se registra en ambos sentidos, por lo que la relación es
    simétrica. No admite lazos (``a`` con ``a``) ni aristas paralelas: volver a
    agregar una arista existente solo actualiza su peso.

    Espacio: O(V + E). Los vértices deben ser hashables; se conserva el orden de
    inserción, así que los recorridos son deterministas.
    """

    def __init__(self) -> None:
        self._adyacencia: dict[V, dict[V, float]] = {}

    def agregar_vertice(self, vertice: V) -> None:
        """Agrega un vértice aislado en O(1). Si ya existe, no hace nada."""
        self._adyacencia.setdefault(vertice, {})

    def agregar_arista(self, a: V, b: V, peso: float = 1.0) -> None:
        """Conecta ``a`` y ``b`` en O(1); crea los vértices si faltan."""
        if a == b:
            raise ValueError("no se admiten aristas de un vértice consigo mismo")
        if peso <= 0:
            raise ValueError("el peso de una arista debe ser positivo")
        self.agregar_vertice(a)
        self.agregar_vertice(b)
        self._adyacencia[a][b] = peso
        self._adyacencia[b][a] = peso

    def tiene_arista(self, a: V, b: V) -> bool:
        """Indica si ``a`` y ``b`` están conectados, en O(1)."""
        return b in self._adyacencia.get(a, {})

    def peso(self, a: V, b: V) -> float | None:
        """Devuelve el peso de la arista, o None si no existe, en O(1)."""
        return self._adyacencia.get(a, {}).get(b)

    def vecinos(self, vertice: V) -> dict[V, float]:
        """Devuelve una copia de ``{vecino: peso}`` en O(grado)."""
        return dict(self._vecinos(vertice))

    def grado(self, vertice: V) -> int:
        """Cantidad de aristas del vértice, en O(1)."""
        return len(self._vecinos(vertice))

    def camino_bfs(self, origen: V, destino: V) -> list[V] | None:
        """Camino con menos aristas entre dos vértices, o None si no existe.

        BFS considera cada arista como un paso; no minimiza la suma de pesos.
        Tiempo y espacio: O(V + E). Lanza KeyError si falta un extremo.
        """
        self._vecinos(origen)
        self._vecinos(destino)
        anteriores: dict[V, V | None] = {origen: None}
        pendientes = deque([origen])

        while pendientes:
            actual = pendientes.popleft()
            if actual == destino:
                camino: list[V] = []
                while actual is not None:
                    camino.append(actual)
                    actual = anteriores[actual]
                return camino[::-1]
            for vecino in self._adyacencia[actual]:
                if vecino not in anteriores:
                    anteriores[vecino] = actual
                    pendientes.append(vecino)
        return None

    def recorrido_dfs(self, origen: V) -> list[V]:
        """Visita en profundidad los vértices alcanzables desde origen.

        Usa una pila para no depender del límite de recursión. Conserva el orden
        de inserción de los vecinos. Tiempo y espacio: O(V + E).
        """
        self._vecinos(origen)
        visitados: set[V] = set()
        recorrido: list[V] = []
        pendientes = [origen]
        while pendientes:
            actual = pendientes.pop()
            if actual in visitados:
                continue
            visitados.add(actual)
            recorrido.append(actual)
            pendientes.extend(reversed(self._adyacencia[actual]))
        return recorrido

    def vertices(self) -> list[V]:
        return list(self._adyacencia)

    def aristas(self) -> Iterator[tuple[V, V, float]]:
        """Recorre cada arista una sola vez, en O(V + E)."""
        procesados: set[V] = set()
        for a, vecinos in self._adyacencia.items():
            for b, peso in vecinos.items():
                if b not in procesados:
                    yield a, b, peso
            procesados.add(a)

    def cantidad_aristas(self) -> int:
        return sum(len(vecinos) for vecinos in self._adyacencia.values()) // 2

    def densidad(self) -> float:
        """Proporción de aristas existentes sobre las posibles: 2E / (V(V-1))."""
        n = len(self._adyacencia)
        if n < 2:
            return 0.0
        return 2 * self.cantidad_aristas() / (n * (n - 1))

    def __contains__(self, vertice: object) -> bool:
        return vertice in self._adyacencia

    def __len__(self) -> int:
        return len(self._adyacencia)

    def _vecinos(self, vertice: V) -> dict[V, float]:
        if vertice not in self._adyacencia:
            raise KeyError(f"el vértice no pertenece al grafo: {vertice!r}")
        return self._adyacencia[vertice]
