"""Recorridos y consultas de la terminal v6."""

import io
import unittest
from unittest.mock import patch

from estructuras.grafo import Grafo
from servicios.catalogo import Catalogo
from ui.terminal import Terminal


class TestRecorridosGrafo(unittest.TestCase):
    def setUp(self):
        self.grafo = Grafo[str]()
        self.grafo.agregar_arista("A", "B", 1)
        self.grafo.agregar_arista("A", "C", 9)
        self.grafo.agregar_arista("B", "C", 1)
        self.grafo.agregar_arista("B", "D", 1)
        self.grafo.agregar_vertice("Z")

    def test_bfs_elige_menos_aristas_aunque_pesen_mas(self):
        self.assertEqual(self.grafo.camino_bfs("A", "C"), ["A", "C"])
        self.assertEqual(self.grafo.camino_bfs("A", "D"), ["A", "B", "D"])
        self.assertEqual(self.grafo.camino_bfs("A", "A"), ["A"])

    def test_bfs_sin_camino_y_vertices_inexistentes(self):
        self.assertIsNone(self.grafo.camino_bfs("A", "Z"))
        with self.assertRaises(KeyError):
            self.grafo.camino_bfs("A", "X")
        with self.assertRaises(KeyError):
            Grafo[str]().camino_bfs("A", "B")

    def test_dfs_visita_una_vez_solo_la_componente_alcanzable(self):
        self.assertEqual(self.grafo.recorrido_dfs("A"), ["A", "B", "C", "D"])
        self.assertEqual(self.grafo.recorrido_dfs("Z"), ["Z"])
        with self.assertRaises(KeyError):
            self.grafo.recorrido_dfs("X")


class TestIntegracionTP8(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/videojuegos.json")

    def ejecutar(self, entradas):
        salida = io.StringIO()
        with patch("builtins.input", side_effect=entradas), patch("sys.stdout", salida):
            Terminal(self.catalogo).iniciar()
        return salida.getvalue()

    def test_camino_entre_juegos_sin_relacion_directa(self):
        origen = self.catalogo.buscar("Elden Ring")
        destino = self.catalogo.buscar("Portal 2")
        self.assertIsNone(self.catalogo.relacion_entre(origen, destino))
        camino = self.catalogo.camino_de_relaciones(origen, destino)
        self.assertIs(camino[0], origen)
        self.assertIs(camino[-1], destino)
        self.assertTrue(all(self.catalogo.relacion_entre(a, b) for a, b in zip(camino, camino[1:])))
        self.assertEqual(len(camino), 3)

    def test_dfs_catalogo_no_repite_juegos(self):
        origen = self.catalogo.buscar("Elden Ring")
        recorrido = self.catalogo.explorar_red(origen)
        self.assertIs(recorrido[0], origen)
        self.assertEqual(len(recorrido), len(set(recorrido)))
        self.assertEqual(len(recorrido), len(self.catalogo))

    def test_terminal_v6_expone_ambas_consultas(self):
        bfs = self.ejecutar(["8", "Elden Ring", "Portal 2", "0"])
        self.assertIn("TERMINAL (v6)", bfs)
        self.assertIn("Cadena más corta (2 relaciones):", bfs)
        self.assertIn("Elden Ring →", bfs)
        self.assertIn("→ Portal 2", bfs)
        dfs = self.ejecutar(["9", "Elden Ring", "0"])
        self.assertIn("Juegos alcanzables desde 'Elden Ring' (DFS):", dfs)
        self.assertIn("Portal 2", dfs)

    def test_terminal_maneja_titulos_invalidos_y_mismo_juego(self):
        self.assertIn("No encontramos 'xyz'.", self.ejecutar(["8", "xyz", "0"]))
        self.assertIn("No encontramos 'xyz'.", self.ejecutar(["8", "Elden Ring", "xyz", "0"]))
        self.assertIn("No encontramos 'xyz'.", self.ejecutar(["9", "xyz", "0"]))
        self.assertIn("mismo videojuego", self.ejecutar(["8", "Elden Ring", "Elden Ring", "0"]))


if __name__ == "__main__":
    unittest.main()
