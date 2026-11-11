import json

from estructuras.arbol_avl import ArbolAVL
from estructuras.arbol_general import ArbolGeneral, NodoGeneral
from modelos.categoria import Categoria
from modelos.videojuego import Videojuego


JERARQUIA_GENEROS = {
    "Acción y aventura": ("Aventura", "Metroidvania", "Plataformas", "Shooter", "Roguelike"),
    "Rol y estrategia": ("RPG", "Estrategia", "MOBA"),
    "Creatividad y lógica": ("Simulacion", "Sandbox", "Puzzle"),
    "Social y deportes": ("Fiesta", "Deportes"),
}


class Catalogo:
    """Lógica de negocio: carga y operaciones sobre el catálogo."""

    def __init__(self) -> None:
        self._elementos: list[Videojuego] = []
        self._arbol_titulos = ArbolAVL()
        self._arbol_categorias = self._construir_arbol_categorias([])

    @staticmethod
    def _construir_arbol_categorias(videojuegos: list[Videojuego]) -> ArbolGeneral[Categoria]:
        raiz = NodoGeneral(Categoria("Videojuegos"))
        hojas_por_genero: dict[str, NodoGeneral[Categoria]] = {}

        for familia, generos in JERARQUIA_GENEROS.items():
            nodo_familia = raiz.agregar_hijo(Categoria(familia))
            for genero in generos:
                hojas_por_genero[genero.casefold()] = nodo_familia.agregar_hijo(Categoria(genero))

        otros: NodoGeneral[Categoria] | None = None
        for videojuego in videojuegos:
            clave = videojuego.genero.casefold()
            hoja = hojas_por_genero.get(clave)
            if hoja is None:
                if otros is None:
                    otros = raiz.agregar_hijo(Categoria("Otros géneros"))
                hoja = otros.agregar_hijo(Categoria(videojuego.genero))
                hojas_por_genero[clave] = hoja
            hoja.valor.videojuegos.append(videojuego)

        return ArbolGeneral(raiz)

    def cargar_desde_json(self, ruta: str) -> None:
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        elementos = datos.get("videojuegos", datos) if isinstance(datos, dict) else datos
        nuevos = [Videojuego(**item) for item in elementos]
        catalogo_actualizado = [*self._elementos, *nuevos]

        # Se construye un índice nuevo por inserción para evitar que un error de
        # los datos deje desincronizados la lista del catálogo y el árbol. El AVL se
        # autobalancea: la altura se mantiene en O(log n) con cualquier orden de carga.
        arbol_actualizado = ArbolAVL(catalogo_actualizado)
        categorias_actualizadas = self._construir_arbol_categorias(catalogo_actualizado)
        self._elementos = catalogo_actualizado
        self._arbol_titulos = arbol_actualizado
        self._arbol_categorias = categorias_actualizadas

    def buscar(self, titulo: str) -> Videojuego | None:
        """Búsqueda por título con el AVL integrado, O(log n) garantizado, sin distinguir mayúsculas."""
        return self._arbol_titulos.buscar(titulo)

    def buscar_parcial(self, texto: str) -> list[Videojuego]:
        """Búsqueda flexible: 'zeld' encuentra 'Zelda'."""
        texto = texto.lower()
        return [v for v in self._elementos if texto in v.titulo.lower()]

    def listar(self) -> list[Videojuego]:
        return list(self._elementos)

    def listar_categorias(self) -> list[tuple[int, str]]:
        """Devuelve la jerarquía en preorden, con la profundidad para mostrarla."""
        return [(profundidad, nodo.valor.nombre) for profundidad, nodo in self._arbol_categorias.preorden()]

    def explorar_categoria(self, nombre: str) -> list[Videojuego] | None:
        """Devuelve los juegos de una categoría y todas sus subcategorías."""
        clave = nombre.strip().casefold()
        nodo = self._arbol_categorias.buscar(lambda categoria: categoria.nombre.casefold() == clave)
        if nodo is None:
            return None
        return [
            videojuego
            for _, actual in self._arbol_categorias.preorden(nodo)
            for videojuego in actual.valor.videojuegos
        ]

    def filtrar(self, genero: str = None, desarrollador: str = None, rating_minimo: float = None) -> list[Videojuego]:
        resultado = list(self._elementos)
        if genero:
            resultado = [v for v in resultado if v.genero.lower() == genero.lower()]

        if desarrollador:
            resultado = [v for v in resultado if desarrollador.lower() in v.desarrollador.lower()]

        if rating_minimo is not None:
            resultado = [v for v in resultado if v.rating >= rating_minimo]

        return resultado

    def __len__(self) -> int:
        return len(self._elementos)
