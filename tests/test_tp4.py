import math
import random
import unittest

from algoritmos.busqueda_secuencial import buscar_secuencial
from estructuras.arbol_avl import ArbolAVL
from estructuras.arbol_binario_busqueda import ArbolBinarioBusqueda
from modelos.videojuego import Videojuego
from servicios.catalogo import Catalogo


def juego(titulo: str, id: int = 1) -> Videojuego:
    return Videojuego(id, titulo, "Prueba", "Equipo", 8.0, 10)


def titulos(videojuegos: list[Videojuego]) -> list[str]:
    return [v.titulo for v in videojuegos]


def cota_altura_avl(n: int) -> float:
    """Cota teórica de niveles de un AVL con n nodos: 1,4405·log2(n+2) - 0,3277."""
    return 1.4405 * math.log2(n + 2) - 0.3277


class TestRotacionesAVL(unittest.TestCase):
    """Cada caso de desbalance, con la forma exacta que debe quedar (preorder)."""

    def test_rotacion_simple_izquierda_izquierda(self):
        arbol = ArbolAVL(juego(t) for t in ("C", "B", "A"))
        self.assertEqual(titulos(arbol.preorder()), ["B", "A", "C"])
        self.assertEqual(arbol.rotaciones, 1)

    def test_rotacion_simple_derecha_derecha(self):
        arbol = ArbolAVL(juego(t) for t in ("A", "B", "C"))
        self.assertEqual(titulos(arbol.preorder()), ["B", "A", "C"])
        self.assertEqual(arbol.rotaciones, 1)

    def test_rotacion_doble_izquierda_derecha(self):
        arbol = ArbolAVL(juego(t) for t in ("C", "A", "B"))
        self.assertEqual(titulos(arbol.preorder()), ["B", "A", "C"])
        self.assertEqual(arbol.rotaciones, 2)

    def test_rotacion_doble_derecha_izquierda(self):
        arbol = ArbolAVL(juego(t) for t in ("A", "C", "B"))
        self.assertEqual(titulos(arbol.preorder()), ["B", "A", "C"])
        self.assertEqual(arbol.rotaciones, 2)

    def test_rotacion_en_subarbol_actualiza_alturas_y_enlaces(self):
        # El desbalance aparece en un nodo interno, no en la raíz.
        arbol = ArbolAVL(juego(t) for t in ("M", "F", "T", "A", "H", "P", "Z", "B", "C"))
        self.assertTrue(arbol.es_valido())
        self.assertEqual(titulos(arbol.inorder()), sorted("MFTAHPZBC"))
        self.assertGreaterEqual(arbol.rotaciones, 1)

    def test_sin_desbalance_no_rota(self):
        arbol = ArbolAVL(juego(t) for t in ("B", "A", "C"))
        self.assertEqual(arbol.rotaciones, 0)
        self.assertEqual(arbol.altura(), 2)


class TestArbolAVL(unittest.TestCase):
    def test_arbol_vacio(self):
        arbol = ArbolAVL()
        self.assertEqual(len(arbol), 0)
        self.assertEqual(arbol.altura(), 0)
        self.assertEqual(arbol.inorder(), [])
        self.assertEqual(arbol.preorder(), [])
        self.assertEqual(arbol.postorder(), [])
        self.assertIsNone(arbol.buscar("A"))
        self.assertEqual(arbol.pasos_busqueda("A"), 0)
        self.assertTrue(arbol.es_valido())

    def test_insertar_y_buscar_sin_distinguir_mayusculas(self):
        juegos = [juego(titulo, id) for id, titulo in enumerate(("C", "A", "B", "E", "D"), 1)]
        arbol = ArbolAVL(juegos)
        self.assertIs(arbol.buscar("b"), juegos[2])
        self.assertIsNone(arbol.buscar("NO EXISTE"))
        self.assertEqual(len(arbol), 5)

    def test_recorridos_en_el_orden_correcto(self):
        arbol = ArbolAVL(juego(t) for t in "ABCDEFG")  # entrada ordenada
        self.assertEqual(titulos(arbol.inorder()), list("ABCDEFG"))
        self.assertEqual(titulos(arbol.preorder()), list("DBACFEG"))
        self.assertEqual(titulos(arbol.postorder()), list("ACBEGFD"))

    def test_conserva_duplicados_y_busca_el_primero_insertado(self):
        juegos = [juego(t, i) for i, t in enumerate(("c", "a", "C", "b", "C", "d", "C"), 1)]
        arbol = ArbolAVL(juegos)
        self.assertEqual(len(arbol), 7)
        self.assertTrue(arbol.es_valido())
        iguales = [v for v in arbol.inorder() if v.titulo.casefold() == "c"]
        self.assertEqual([v.id for v in iguales], [1, 3, 5, 7])  # orden de inserción
        self.assertIs(arbol.buscar("C"), juegos[0])

    def test_muchos_duplicados_mantienen_balance_y_primero_insertado(self):
        juegos = [juego("Repetido", i) for i in range(500)]
        arbol = ArbolAVL(juegos)
        self.assertTrue(arbol.es_valido())
        self.assertLessEqual(arbol.altura(), cota_altura_avl(500))
        self.assertIs(arbol.buscar("repetido"), juegos[0])

    def test_entrada_ordenada_mantiene_altura_logaritmica(self):
        # Con 1200 el BST de TP3 llega a altura 1200 (ver test_tp3).
        cantidad = 1200
        for orden in (range(cantidad), reversed(range(cantidad))):
            with self.subTest(orden=type(orden).__name__):
                arbol = ArbolAVL(juego(f"Título {i:04d}", i) for i in orden)
                self.assertEqual(len(arbol), cantidad)
                self.assertTrue(arbol.es_valido())
                self.assertLessEqual(arbol.altura(), cota_altura_avl(cantidad))
                self.assertLessEqual(arbol.altura(), 2 * math.ceil(math.log2(cantidad + 1)))

    def test_entrada_en_zigzag_y_aleatoria_cumplen_el_invariante(self):
        n = 2000
        ordenados = [juego(f"Título {i:05d}", i) for i in range(n)]
        zigzag = [ordenados[i // 2] if i % 2 == 0 else ordenados[n - 1 - i // 2] for i in range(n)]
        aleatorio = ordenados.copy()
        random.Random(7).shuffle(aleatorio)

        for nombre, entrada in (("zigzag", zigzag), ("aleatorio", aleatorio)):
            with self.subTest(entrada=nombre):
                arbol = ArbolAVL(entrada)
                self.assertTrue(arbol.es_valido())
                self.assertLessEqual(arbol.altura(), cota_altura_avl(n))
                self.assertEqual(titulos(arbol.inorder()), titulos(ordenados))

    def test_invariantes_se_cumplen_tras_cada_insercion(self):
        arbol = ArbolAVL()
        entrada = [juego(f"T{i:03d}", i) for i in range(300)]
        random.Random(11).shuffle(entrada)
        for indice, videojuego in enumerate(entrada, 1):
            arbol.insertar(videojuego)
            self.assertEqual(len(arbol), indice)
            self.assertTrue(arbol.es_valido(), f"inválido tras {indice} inserciones")

    def test_peor_caso_de_busqueda_es_logaritmico(self):
        n = 5000
        arbol = ArbolAVL(juego(f"Título {i:05d}", i) for i in range(n))
        peor = max(arbol.pasos_busqueda(f"Título {i:05d}") for i in range(0, n, 7))
        self.assertLessEqual(peor, arbol.altura())
        self.assertLessEqual(peor, cota_altura_avl(n))

    def test_es_valido_detecta_un_arbol_corrupto(self):
        arbol = ArbolAVL(juego(t) for t in "ABC")
        arbol._raiz.altura = 99
        self.assertFalse(arbol.es_valido())

    def test_misma_respuesta_que_el_bst_y_la_busqueda_secuencial(self):
        entrada = [juego(f"Juego {i % 40:02d}", i) for i in range(200)]  # con repetidos
        random.Random(3).shuffle(entrada)
        avl, bst = ArbolAVL(entrada), ArbolBinarioBusqueda(entrada)

        self.assertEqual(titulos(avl.inorder()), titulos(bst.inorder()))
        for i in range(45):
            consulta = f"JUEGO {i:02d}"
            with self.subTest(consulta=consulta):
                esperado = buscar_secuencial(entrada, consulta)
                self.assertIs(avl.buscar(consulta), esperado)
                self.assertIs(bst.buscar(consulta), esperado)


class TestPasosBusquedaBST(unittest.TestCase):
    def test_bst_degenerado_recorre_todos_los_nodos(self):
        n = 300
        arbol = ArbolBinarioBusqueda(juego(f"T{i:04d}", i) for i in range(n))
        self.assertEqual(arbol.altura(), n)
        self.assertEqual(arbol.pasos_busqueda(f"T{n - 1:04d}"), n)
        self.assertEqual(arbol.pasos_busqueda("T0000"), 1)
        self.assertEqual(arbol.pasos_busqueda("zzz"), n)  # mayor que todas: baja por la derecha

    def test_arbol_vacio(self):
        self.assertEqual(ArbolBinarioBusqueda().pasos_busqueda("A"), 0)


class TestIntegracionAVLCatalogo(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/videojuegos.json")

    def test_el_catalogo_indexa_con_un_avl(self):
        self.assertIsInstance(self.catalogo._arbol_titulos, ArbolAVL)
        self.assertTrue(self.catalogo._arbol_titulos.es_valido())

    def test_buscar_coincide_con_la_busqueda_secuencial(self):
        videojuegos = self.catalogo.listar()
        for esperado in videojuegos:
            with self.subTest(titulo=esperado.titulo):
                self.assertIs(self.catalogo.buscar(esperado.titulo.swapcase()), esperado)

    def test_carga_repetida_conserva_el_primero_y_el_balance(self):
        primero = self.catalogo.buscar("Hollow Knight")
        self.catalogo.cargar_desde_json("datos/videojuegos.json")
        self.assertIs(self.catalogo.buscar("Hollow Knight"), primero)
        self.assertTrue(self.catalogo._arbol_titulos.es_valido())


if __name__ == "__main__":
    unittest.main()
