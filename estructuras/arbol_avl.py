from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from modelos.videojuego import Videojuego


@dataclass(slots=True)
class NodoAVL:
    """Nodo de un árbol AVL por título.

    ``altura`` es la cantidad de niveles del subárbol que nace en el nodo: una hoja
    vale 1 y un hijo ausente vale 0. Se guarda en el nodo para que calcular el factor
    de balance cueste O(1). ``orden`` es el número de inserción y desempata títulos
    equivalentes (ver ``ArbolAVL``).
    """

    videojuego: Videojuego
    orden: int
    altura: int = 1
    izquierda: NodoAVL | None = None
    derecha: NodoAVL | None = None


class ArbolAVL:
    """Árbol binario de búsqueda autobalanceado (AVL) ordenado por título.

    Invariante AVL: en todo nodo, las alturas de sus dos subárboles difieren como
    máximo en 1. Después de cada inserción se recorre de vuelta el camino hacia la
    raíz, se actualizan las alturas y, si algún nodo queda con factor de balance
    +2 o -2, se corrige con una rotación simple o doble. Con ese invariante la
    altura nunca supera ``1,44 · log2(n + 2)``, sin importar el orden de inserción.

    Misma interfaz que ``ArbolBinarioBusqueda`` (``insertar``, ``buscar``, recorridos,
    ``altura``, ``len``), de modo que ambos son intercambiables en el catálogo.

    Títulos repetidos: la comparación ignora mayúsculas (``casefold``) y, si dos
    títulos son equivalentes, desempata por orden de inserción. Así el orden entre
    ellos es total y estable, las rotaciones nunca lo alteran y ``buscar`` devuelve
    siempre el primero que se insertó, igual que el BST de TP3.
    """

    def __init__(self, videojuegos: Iterable[Videojuego] = ()) -> None:
        self._raiz: NodoAVL | None = None
        self._tam = 0
        self._siguiente_orden = 0
        self._rotaciones = 0
        for videojuego in videojuegos:
            self.insertar(videojuego)

    # ------------------------------------------------------------------ utilidades

    @staticmethod
    def _clave(videojuego: Videojuego) -> str:
        return videojuego.titulo.casefold()

    @staticmethod
    def _altura_de(nodo: NodoAVL | None) -> int:
        return nodo.altura if nodo is not None else 0

    @classmethod
    def _actualizar_altura(cls, nodo: NodoAVL) -> None:
        nodo.altura = 1 + max(cls._altura_de(nodo.izquierda), cls._altura_de(nodo.derecha))

    @classmethod
    def _factor_balance(cls, nodo: NodoAVL | None) -> int:
        """altura(izquierda) - altura(derecha). Un árbol AVL mantiene -1, 0 o +1."""
        if nodo is None:
            return 0
        return cls._altura_de(nodo.izquierda) - cls._altura_de(nodo.derecha)

    # ------------------------------------------------------------------ rotaciones

    def _rotar_derecha(self, y: NodoAVL) -> NodoAVL:
        """Rotación simple a la derecha (caso izquierda-izquierda). O(1).

                y                x
               / \\              / \\
              x   C    -->     A   y
             / \\                  / \\
            A   B                B   C
        """
        x = y.izquierda
        y.izquierda = x.derecha
        x.derecha = y
        self._actualizar_altura(y)  # y quedó debajo de x: se actualiza primero
        self._actualizar_altura(x)
        self._rotaciones += 1
        return x

    def _rotar_izquierda(self, x: NodoAVL) -> NodoAVL:
        """Rotación simple a la izquierda (caso derecha-derecha). O(1).

              x                    y
             / \\                  / \\
            A   y      -->        x   C
               / \\              / \\
              B   C             A   B
        """
        y = x.derecha
        x.derecha = y.izquierda
        y.izquierda = x
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        self._rotaciones += 1
        return y

    def _rebalancear(self, nodo: NodoAVL) -> NodoAVL:
        """Actualiza la altura de ``nodo`` y lo rota si perdió el balance. O(1).

        Devuelve la raíz del subárbol resultante, que reemplaza a ``nodo`` en su padre.
        """
        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)

        if balance > 1:  # pesa la izquierda
            if self._factor_balance(nodo.izquierda) < 0:  # izquierda-derecha
                nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)

        if balance < -1:  # pesa la derecha
            if self._factor_balance(nodo.derecha) > 0:  # derecha-izquierda
                nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)

        return nodo

    # ------------------------------------------------------------------- operaciones

    def insertar(self, videojuego: Videojuego) -> None:
        """Inserta un juego y rebalancea. O(log n) garantizado.

        Baja O(h) niveles y vuelve rebalanceando O(1) por nivel. Como h = O(log n)
        por el invariante AVL, el total es O(log n) también en el peor caso. La
        recursión tiene la profundidad de la altura (unas decenas de niveles), lejos
        del límite de recursión de Python.
        """
        nuevo = NodoAVL(videojuego, self._siguiente_orden)
        self._siguiente_orden += 1
        self._raiz = self._insertar(self._raiz, nuevo, self._clave(videojuego))
        self._tam += 1

    def _insertar(self, nodo: NodoAVL | None, nuevo: NodoAVL, clave: str) -> NodoAVL:
        if nodo is None:
            return nuevo

        clave_nodo = self._clave(nodo.videojuego)
        # (clave, orden) es un orden total: nunca hay empates exactos.
        if (clave, nuevo.orden) < (clave_nodo, nodo.orden):
            nodo.izquierda = self._insertar(nodo.izquierda, nuevo, clave)
        else:
            nodo.derecha = self._insertar(nodo.derecha, nuevo, clave)
        return self._rebalancear(nodo)

    def buscar(self, titulo: str) -> Videojuego | None:
        """Busca por título en O(log n) garantizado (peor caso incluido).

        Si hay títulos equivalentes devuelve el primero insertado: al encontrar una
        coincidencia sigue hacia la izquierda por si hay otra anterior.
        """
        objetivo = titulo.casefold()
        actual = self._raiz
        encontrado: Videojuego | None = None

        while actual is not None:
            clave_actual = self._clave(actual.videojuego)
            if objetivo == clave_actual:
                encontrado = actual.videojuego
                actual = actual.izquierda
            elif objetivo < clave_actual:
                actual = actual.izquierda
            else:
                actual = actual.derecha

        return encontrado

    def pasos_busqueda(self, titulo: str) -> int:
        """Cantidad de nodos visitados al buscar ``titulo``, para los experimentos.

        Mide el costo en comparaciones, independiente del hardware y del intérprete.
        """
        objetivo = titulo.casefold()
        actual = self._raiz
        pasos = 0

        while actual is not None:
            pasos += 1
            # Igual que buscar(): ante una coincidencia sigue a la izquierda.
            if objetivo <= self._clave(actual.videojuego):
                actual = actual.izquierda
            else:
                actual = actual.derecha

        return pasos

    # ---------------------------------------------------------------------- recorridos

    def inorder(self) -> list[Videojuego]:
        """Recorre izquierda-raíz-derecha y devuelve los juegos por título."""
        resultado: list[Videojuego] = []
        pila: list[NodoAVL] = []
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
        pila: list[tuple[NodoAVL, bool]] = []
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

    # ------------------------------------------------------------------- inspección

    def altura(self) -> int:
        """Cantidad de niveles (árbol vacío = 0). O(1): la altura vive en la raíz."""
        return self._altura_de(self._raiz)

    @property
    def rotaciones(self) -> int:
        """Rotaciones simples realizadas desde la creación (una doble cuenta como 2)."""
        return self._rotaciones

    def es_valido(self) -> bool:
        """Verifica por completo las propiedades del árbol, recalculando todo. O(n).

        Comprueba que (1) el recorrido inorder respeta el orden de búsqueda, (2) la
        altura guardada en cada nodo coincide con la real y (3) ningún factor de
        balance sale de [-1, 1]. Sirve para las pruebas y para depurar.
        """
        if self._raiz is None:
            return True

        alturas: dict[int, int] = {}
        pila: list[tuple[NodoAVL, bool]] = [(self._raiz, False)]
        while pila:
            nodo, visitado = pila.pop()
            if not visitado:
                pila.append((nodo, True))
                for hijo in (nodo.izquierda, nodo.derecha):
                    if hijo is not None:
                        pila.append((hijo, False))
                continue

            h_izq = alturas[id(nodo.izquierda)] if nodo.izquierda is not None else 0
            h_der = alturas[id(nodo.derecha)] if nodo.derecha is not None else 0
            real = 1 + max(h_izq, h_der)
            if nodo.altura != real or abs(h_izq - h_der) > 1:
                return False
            alturas[id(nodo)] = real

        ordenes: list[tuple[str, int]] = []
        pila_nodos: list[NodoAVL] = []
        actual = self._raiz
        while actual is not None or pila_nodos:
            while actual is not None:
                pila_nodos.append(actual)
                actual = actual.izquierda
            actual = pila_nodos.pop()
            ordenes.append((self._clave(actual.videojuego), actual.orden))
            actual = actual.derecha
        return all(a < b for a, b in zip(ordenes, ordenes[1:]))

    def __len__(self) -> int:
        return self._tam
