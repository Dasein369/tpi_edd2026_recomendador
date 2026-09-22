import json

from algoritmos.busqueda_secuencial import buscar_secuencial
from modelos.videojuego import Videojuego


class Catalogo:
    """Lógica de negocio: carga y operaciones sobre el catálogo."""

    def __init__(self) -> None:
        self._elementos: list[Videojuego] = []

    def cargar_desde_json(self, ruta: str) -> None:
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        elementos = datos.get("videojuegos", datos) if isinstance(datos, dict) else datos
        for item in elementos:
            self._elementos.append(Videojuego(**item))

    def buscar(self, titulo: str) -> Videojuego | None:
        """Búsqueda secuencial por título, sin distinguir mayúsculas."""
        return buscar_secuencial(self._elementos, titulo)

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
