import io
import unittest
from unittest.mock import patch

from estructuras.monticulo_maximo import MonticuloMaximo
from servicios.catalogo import Catalogo
from ui.terminal import Terminal


class TestMonticuloMaximo(unittest.TestCase):
    def test_heapify_insertar_consultar_y_extraer(self):
        monticulo = MonticuloMaximo([4, 1, 9, 3], prioridad=lambda numero: numero)

        self.assertEqual(monticulo.ver_maximo(), 9)
        monticulo.insertar(12)
        self.assertEqual(monticulo.extraer_maximo(), 12)
        self.assertEqual(monticulo.extraer_maximo(), 9)
        self.assertEqual(monticulo.extraer_maximo(), 4)
        self.assertEqual(monticulo.extraer_maximo(), 3)
        self.assertEqual(monticulo.extraer_maximo(), 1)
        self.assertEqual(len(monticulo), 0)

    def test_mayores_respeta_prioridad_empates_y_no_muta_el_heap(self):
        juegos = [
            {"titulo": "Primero", "rating": 8.5},
            {"titulo": "Mejor", "rating": 9.7},
            {"titulo": "Segundo empate", "rating": 9.7},
            {"titulo": "Último", "rating": 7.0},
        ]
        monticulo = MonticuloMaximo(juegos, prioridad=lambda juego: juego["rating"])

        resultado = monticulo.mayores(3)

        self.assertEqual(
            [juego["titulo"] for juego in resultado],
            ["Mejor", "Segundo empate", "Primero"],
        )
        self.assertEqual(len(monticulo), len(juegos))
        self.assertEqual([j["titulo"] for j in monticulo.mayores(3)],
                         [j["titulo"] for j in resultado])

    def test_mayores_maneja_limites_y_monticulo_vacio(self):
        monticulo = MonticuloMaximo([2, 1], prioridad=lambda valor: valor)

        self.assertEqual(monticulo.mayores(0), [])
        self.assertEqual(monticulo.mayores(5), [2, 1])
        self.assertEqual(MonticuloMaximo().mayores(15), [])
        with self.assertRaises(ValueError):
            monticulo.mayores(-1)
        with self.assertRaises(IndexError):
            MonticuloMaximo().extraer_maximo()


class TestIntegracionTop15(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/videojuegos.json")

    def test_top_15_ordenado_por_rating_y_consulta_repetible(self):
        esperado = sorted(
            self.catalogo.listar(), key=lambda juego: juego.rating, reverse=True
        )[:15]

        primero = self.catalogo.top_n()
        segundo = self.catalogo.top_n()

        self.assertEqual(primero, esperado)
        self.assertEqual(segundo, esperado)
        self.assertEqual(len(primero), 15)

    def test_terminal_expone_el_top_15(self):
        salida = io.StringIO()
        with patch("builtins.input", side_effect=["5", "0"]), patch("sys.stdout", salida):
            Terminal(self.catalogo).iniciar()

        texto = salida.getvalue()
        self.assertIn("TERMINAL (v5)", texto)
        self.assertIn("5. Ver Top 15 por rating", texto)
        self.assertIn("Top 15 de videojuegos por rating:", texto)
        self.assertIn("The Legend of Zelda: Breath of the Wild", texto)


if __name__ == "__main__":
    unittest.main()
