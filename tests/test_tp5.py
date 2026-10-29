import io
import json
import unittest
from unittest.mock import mock_open, patch

from estructuras.arbol_general import ArbolGeneral, NodoGeneral
from servicios.catalogo import Catalogo
from ui.terminal import Terminal


class TestArbolGeneral(unittest.TestCase):
    def test_un_nodo_puede_tener_mas_de_dos_hijos_y_se_recorre_en_orden(self):
        raiz = NodoGeneral("raiz")
        a = raiz.agregar_hijo("a")
        raiz.agregar_hijo("b")
        raiz.agregar_hijo("c")
        a.agregar_hijo("a1")
        arbol = ArbolGeneral(raiz)

        self.assertEqual([(profundidad, nodo.valor) for profundidad, nodo in arbol.preorden()],
                         [(0, "raiz"), (1, "a"), (2, "a1"), (1, "b"), (1, "c")])
        self.assertEqual([nodo.valor for _, nodo in arbol.postorden()],
                         ["a1", "a", "b", "c", "raiz"])
        self.assertIs(arbol.buscar(lambda valor: valor == "a1"), a.hijos[0])
        self.assertIsNone(arbol.buscar(lambda valor: valor == "inexistente"))

    def test_arbol_vacio(self):
        arbol = ArbolGeneral[str]()
        self.assertEqual(arbol.preorden(), [])
        self.assertEqual(arbol.postorden(), [])
        self.assertIsNone(arbol.buscar(lambda _: True))


class TestIntegracionCategorias(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/videojuegos.json")

    def test_categorias_y_subcategorias_agrupan_los_juegos(self):
        categorias = self.catalogo.listar_categorias()
        self.assertEqual(categorias[0], (0, "Videojuegos"))
        self.assertIn((1, "Rol y estrategia"), categorias)
        self.assertIn((2, "RPG"), categorias)
        self.assertEqual(len(self.catalogo.explorar_categoria("rpg")), 5)
        self.assertEqual(len(self.catalogo.explorar_categoria("ROL Y ESTRATEGIA")), 7)
        self.assertEqual(len(self.catalogo.explorar_categoria("Videojuegos")), len(self.catalogo))
        self.assertIsNone(self.catalogo.explorar_categoria("Categoría inexistente"))

    def test_genero_nuevo_se_ubica_en_otros_sin_perder_el_indice_avl(self):
        nuevos = json.dumps([{
            "id": 26, "titulo": "Juego de terror", "genero": "Terror",
            "desarrollador": "Estudio", "rating": 8.0, "horas_jugadas": 3,
        }])
        with patch("builtins.open", mock_open(read_data=nuevos)):
            self.catalogo.cargar_desde_json("nuevos.json")

        self.assertIn((1, "Otros géneros"), self.catalogo.listar_categorias())
        nuevo = self.catalogo.buscar("juego de terror")
        self.assertIs(self.catalogo.explorar_categoria("Terror")[0], nuevo)
        self.assertEqual(len(self.catalogo.explorar_categoria("Otros géneros")), 1)
        self.assertEqual(len(self.catalogo.explorar_categoria("Videojuegos")), 26)
        self.assertTrue(self.catalogo._arbol_titulos.es_valido())

    def test_terminal_explora_una_rama_del_arbol(self):
        salida = io.StringIO()
        with patch("builtins.input", side_effect=["4", "Rol y estrategia", "0"]), patch("sys.stdout", salida):
            Terminal(self.catalogo).iniciar()

        texto = salida.getvalue()
        self.assertIn("TERMINAL (v3)", texto)
        self.assertIn("Videojuegos en 'Rol y estrategia':", texto)
        self.assertIn("Elden Ring", texto)
        self.assertIn("Civilization VI", texto)
        self.assertNotIn("Hollow Knight (", texto)


if __name__ == "__main__":
    unittest.main()
