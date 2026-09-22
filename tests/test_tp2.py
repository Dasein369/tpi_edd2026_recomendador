import unittest

from algoritmos.busqueda_arbol_tp2 import ArbolBusquedaBalanceada
from algoritmos.busqueda_secuencial import buscar_secuencial
from modelos.videojuego import Videojuego


def videojuegos_de_prueba(cantidad: int) -> list[Videojuego]:
    return [
        Videojuego(
            id=i,
            titulo=f"Videojuego de prueba {i:05d}",
            genero="Prueba",
            desarrollador="TP2",
            rating=8.0,
            horas_jugadas=10,
        )
        for i in range(1, cantidad + 1)
    ]


class TestTP2(unittest.TestCase):
    def setUp(self):
        self.videojuegos = videojuegos_de_prueba(100)
        self.arbol = ArbolBusquedaBalanceada(self.videojuegos)

    def test_ambas_estrategias_encuentran_el_mismo_videojuego(self):
        titulo = self.videojuegos[-1].titulo

        resultado_secuencial = buscar_secuencial(self.videojuegos, titulo)
        resultado_arbol = self.arbol.buscar(titulo)

        self.assertIsNotNone(resultado_secuencial)
        self.assertIsNotNone(resultado_arbol)
        self.assertEqual(resultado_secuencial.id, resultado_arbol.id)

    def test_busqueda_no_existente(self):
        titulo = "Este videojuego no existe"
        self.assertIsNone(buscar_secuencial(self.videojuegos, titulo))
        self.assertIsNone(self.arbol.buscar(titulo))

    def test_busqueda_no_distingue_mayusculas(self):
        titulo = self.videojuegos[10].titulo.upper()
        self.assertEqual(
            buscar_secuencial(self.videojuegos, titulo).id,
            self.arbol.buscar(titulo).id,
        )

    def test_inorder_queda_ordenado(self):
        titulos = [v.titulo.casefold() for v in self.arbol.inorder()]
        self.assertEqual(titulos, sorted(titulos))

    def test_tamano(self):
        self.assertEqual(len(self.arbol), 100)

    def test_rechaza_titulos_duplicados(self):
        datos = videojuegos_de_prueba(2)
        datos[1] = Videojuego(2, datos[0].titulo, "Prueba", "TP2", 8.0, 10)
        with self.assertRaises(ValueError):
            ArbolBusquedaBalanceada(datos)


if __name__ == "__main__":
    unittest.main()
