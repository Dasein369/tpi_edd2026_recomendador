import json

from estructuras.arbol_binario_busqueda import ArbolBinarioBusqueda
from modelos.videojuego import Videojuego


class Catalogo:
    """Lógica de negocio: carga y operaciones sobre el catálogo."""

    def __init__(self) -> None:
        self._elementos: list[Videojuego] = []
        self._arbol_titulos = ArbolBinarioBusqueda()

    def cargar_desde_json(self, ruta: str) -> None:
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        elementos = datos.get("videojuegos", datos) if isinstance(datos, dict) else datos
        nuevos = [Videojuego(**item) for item in elementos]
        catalogo_actualizado = [*self._elementos, *nuevos]

        # Se construye un índice nuevo por inserción para evitar que un error de
        # los datos deje desincronizados la lista del catálogo y el árbol.
        arbol_actualizado = ArbolBinarioBusqueda(catalogo_actualizado)
        self._elementos = catalogo_actualizado
        self._arbol_titulos = arbol_actualizado

    def buscar(self, titulo: str) -> Videojuego | None:
        """Búsqueda por título con el BST integrado, sin distinguir mayúsculas."""
        return self._arbol_titulos.buscar(titulo)

    def buscar_parcial(self, texto: str) -> list[Videojuego]:
        """Búsqueda flexible: 'zeld' encuentra 'Zelda'."""
        texto = texto.lower()
        return [v for v in self._elementos if texto in v.titulo.lower()]

    def listar(self) -> list[Videojuego]:
        return list(self._elementos)

    def filtrar(self, genero: str = None, desarrollador: str = None, rating_minimo: float = None) -> list[Videojuego]:
        resultado = self._elementos
        if genero:
            resultado = [v for v in resultado if v.genero.lower() == genero.lower()]

        if desarrollador:
            resultado = [v for v in resultado if desarrollador.lower() in v.desarrollador.lower()]

        if rating_minimo is not None:
            resultado = [v for v in resultado if v.rating >= rating_minimo]

        return resultado

    def __len__(self) -> int:
        return len(self._elementos)
