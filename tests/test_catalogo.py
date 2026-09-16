import unittest

from servicios.catalogo import Catalogo


class TestCatalogo(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/videojuegos.json")

    def test_buscar_por_titulo(self):
        resultado = self.catalogo.buscar("hollow knight")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.titulo, "Hollow Knight")

    def test_buscar_devuelve_none_si_no_existe(self):
        self.assertIsNone(self.catalogo.buscar("no-existe"))

    def test_listar_devuelve_todos(self):
        self.assertTrue(len(self.catalogo.listar()) > 0)

    def test_filtrar_por_genero(self):
        resultados = self.catalogo.filtrar("RPG")
        self.assertTrue(all(v.genero.lower() == "rpg" for v in resultados))


if __name__ == "__main__":
    unittest.main()
