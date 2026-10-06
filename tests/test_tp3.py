import unittest

from algoritmos.busqueda_secuencial import buscar_secuencial
from estructuras.arbol_binario_busqueda import ArbolBinarioBusqueda
from modelos.videojuego import Videojuego
from servicios.catalogo import Catalogo


def juego(titulo: str, id: int = 1) -> Videojuego:
    return Videojuego(id, titulo, "Prueba", "Equipo", 8.0, 10)


class TestArbolBinarioBusqueda(unittest.TestCase):
    def setUp(self):
        # La raíz C produce ramas con más de un nivel para distinguir recorridos.
        self.juegos = [juego(titulo, id) for id, titulo in enumerate(("C", "A", "B", "E", "D"), 1)]
        self.arbol = ArbolBinarioBusqueda(self.juegos)

    def test_arbol_vacio(self):
        arbol = ArbolBinarioBusqueda()
        self.assertEqual(len(arbol), 0)
        self.assertEqual(arbol.altura(), 0)
        self.assertEqual(arbol.inorder(), [])
        self.assertEqual(arbol.preorder(), [])
        self.assertEqual(arbol.postorder(), [])
        self.assertIsNone(arbol.buscar("A"))

    def test_insertar_y_buscar_sin_distinguir_mayusculas(self):
        self.assertIs(self.arbol.buscar("b"), self.juegos[2])
        self.assertIs(self.arbol.buscar("NO EXISTE"), None)
        self.assertEqual(len(self.arbol), 5)

    def test_recorridos_visitan_los_nodos_en_el_orden_correcto(self):
        self.assertEqual([v.titulo for v in self.arbol.inorder()], ["A", "B", "C", "D", "E"])
        self.assertEqual([v.titulo for v in self.arbol.preorder()], ["C", "A", "B", "E", "D"])
        self.assertEqual([v.titulo for v in self.arbol.postorder()], ["B", "A", "D", "E", "C"])

    def test_conserva_titulos_duplicados_y_busca_primera_coincidencia(self):
        self.arbol.insertar(juego("c", 6))
        encontrados = [v for v in self.arbol.inorder() if v.titulo.casefold() == "c"]
        self.assertEqual(len(self.arbol), 6)
        self.assertEqual(len(encontrados), 2)
        self.assertIs(self.arbol.buscar("C"), self.juegos[0])

    def test_soporta_arbol_degenerado_mayor_al_limite_de_recursion(self):
        cantidad = 1200
        arbol = ArbolBinarioBusqueda(
            juego(f"Título {indice:04d}", indice)
            for indice in range(cantidad)
        )
        self.assertEqual(arbol.altura(), cantidad)
        self.assertEqual(len(arbol.inorder()), cantidad)
        self.assertEqual(len(arbol.preorder()), cantidad)
        self.assertEqual(len(arbol.postorder()), cantidad)


class TestIntegracionBSTCatalogo(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/videojuegos.json")

    def test_buscar_del_catalogo_coincide_con_la_busqueda_secuencial(self):
        videojuegos = self.catalogo.listar()
        for esperado in videojuegos:
            with self.subTest(titulo=esperado.titulo):
                secuencial = buscar_secuencial(videojuegos, esperado.titulo)
                arbol = self.catalogo.buscar(esperado.titulo.swapcase())
                self.assertIsNotNone(secuencial)
                self.assertIsNotNone(arbol)
                self.assertEqual(arbol.id, secuencial.id)

    def test_una_carga_repetida_conserva_los_juegos_con_titulos_duplicados(self):
        cantidad_inicial = len(self.catalogo)
        primero = self.catalogo.buscar("Hollow Knight")
        self.catalogo.cargar_desde_json("datos/videojuegos.json")
        self.assertEqual(len(self.catalogo), cantidad_inicial * 2)
        self.assertIs(self.catalogo.buscar("Hollow Knight"), primero)


if __name__ == "__main__":
    unittest.main()
