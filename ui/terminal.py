import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from estructuras.grafo import Grafo
from modelos.videojuego import Videojuego
from servicios.catalogo import FAMILIA_POR_GENERO, Catalogo
from servicios.relaciones import calcular_relacion
from ui.terminal import Terminal


class TestGrafo(unittest.TestCase):
    def setUp(self):
        self.grafo = Grafo()
        self.grafo.agregar_arista("A", "B", 3)
        self.grafo.agregar_arista("A", "C", 1)
        self.grafo.agregar_vertice("D")

    def test_aristas_son_simetricas_y_con_peso(self):
        self.assertTrue(self.grafo.tiene_arista("A", "B"))
        self.assertTrue(self.grafo.tiene_arista("B", "A"))
        self.assertEqual(self.grafo.peso("B", "A"), 3)
        self.assertIsNone(self.grafo.peso("B", "C"))
        self.assertFalse(self.grafo.tiene_arista("B", "C"))

    def test_cantidades_grado_y_vertice_aislado(self):
        self.assertEqual(len(self.grafo), 4)
        self.assertEqual(self.grafo.cantidad_aristas(), 2)
        self.assertEqual(self.grafo.grado("A"), 2)
        self.assertEqual(self.grafo.grado("D"), 0)
        self.assertEqual(self.grafo.vecinos("D"), {})

    def test_aristas_se_recorren_una_sola_vez(self):
        aristas = list(self.grafo.aristas())
        self.assertEqual(len(aristas), 2)
        self.assertEqual({frozenset((a, b)) for a, b, _ in aristas},
                         {frozenset("AB"), frozenset("AC")})

    def test_densidad(self):
        self.assertAlmostEqual(self.grafo.densidad(), 2 * 2 / (4 * 3))
        self.assertEqual(Grafo().densidad(), 0.0)

    def test_reagregar_arista_actualiza_el_peso_sin_duplicar(self):
        self.grafo.agregar_arista("B", "A", 5)
        self.assertEqual(self.grafo.peso("A", "B"), 5)
        self.assertEqual(self.grafo.cantidad_aristas(), 2)

    def test_vecinos_devuelve_copia(self):
        self.grafo.vecinos("A").clear()
        self.assertEqual(self.grafo.grado("A"), 2)

    def test_rechaza_lazos_pesos_invalidos_y_vertices_inexistentes(self):
        with self.assertRaises(ValueError):
            self.grafo.agregar_arista("A", "A")
        with self.assertRaises(ValueError):
            self.grafo.agregar_arista("A", "B", 0)
        with self.assertRaises(KeyError):
            self.grafo.vecinos("Z")
        self.assertNotIn("Z", self.grafo)


class TestRelacionesYCatalogo(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/videojuegos.json")

    def juego(self, titulo):
        return self.catalogo.buscar(titulo)

    def test_un_vertice_por_videojuego(self):
        resumen = self.catalogo.resumen_red()
        self.assertEqual(resumen["vertices"], len(self.catalogo))
        self.assertGreater(resumen["aristas"], 0)
        self.assertLess(resumen["densidad"], 0.5)  # grafo ralo: lista de adyacencia

    def test_pesos_por_criterio(self):
        elden = self.juego("Elden Ring")
        dark = self.juego("Dark Souls III")
        witcher = self.juego("The Witcher 3: Wild Hunt")
        zelda = self.juego("The Legend of Zelda: Breath of the Wild")
        hollow = self.juego("Hollow Knight")

        mismo_genero_y_dev = calcular_relacion(elden, dark, FAMILIA_POR_GENERO)
        self.assertEqual(mismo_genero_y_dev.peso, 7)
        self.assertEqual(len(mismo_genero_y_dev.motivos), 3)
        self.assertIn("tags compartidos (difícil, fantasía oscura)", mismo_genero_y_dev.motivos)

        self.assertEqual(calcular_relacion(elden, witcher, FAMILIA_POR_GENERO).peso, 4)
        # Aventura y Metroidvania son hermanos en "Acción y aventura"
        self.assertEqual(calcular_relacion(zelda, hollow, FAMILIA_POR_GENERO).peso, 2)
        # Familias distintas: un tag compartido también puede crear la relación.
        self.assertEqual(calcular_relacion(elden, zelda, FAMILIA_POR_GENERO).peso, 1)

    def test_relacion_es_simetrica(self):
        a, b = self.juego("Elden Ring"), self.juego("The Witcher 3: Wild Hunt")
        self.assertEqual(self.catalogo.relacion_entre(a, b), self.catalogo.relacion_entre(b, a))

    def test_relacion_entre_sin_conexion_devuelve_none(self):
        elden = self.juego("Elden Ring")
        portal = self.juego("Portal 2")
        self.assertIsNone(self.catalogo.relacion_entre(elden, portal))

    def test_tags_se_normalizan_y_el_modelo_sigue_aceptando_datos_anteriores(self):
        datos = (99, "Nuevo", "Puzzle", "Estudio", 8.0, 2)
        self.assertEqual(Videojuego(*datos).tags, ())
        self.assertEqual(
            Videojuego(*datos, tags=["  Cooperativo ", "cooperativo", "HUMOR"]).tags,
            ("cooperativo", "humor"),
        )

    def test_filtro_por_tag_no_altera_el_filtro_por_genero(self):
        por_tag = self.catalogo.filtrar(tag="  MUNDO ABIERTO ")
        self.assertIn(self.juego("Elden Ring"), por_tag)
        self.assertIn(self.juego("Minecraft"), por_tag)
        self.assertNotIn(self.juego("Portal 2"), por_tag)
        self.assertEqual(len(self.catalogo.filtrar(genero="RPG")), 5)

    def test_el_grafo_coincide_con_la_regla_para_todos_los_pares(self):
        juegos = self.catalogo.listar()
        for i, a in enumerate(juegos):
            for b in juegos[i + 1:]:
                esperado = calcular_relacion(a, b, FAMILIA_POR_GENERO)
                self.assertEqual(self.catalogo.relacion_entre(a, b), esperado)

    def test_juegos_relacionados_ordenados_sin_incluir_al_propio_juego(self):
        elden = self.juego("Elden Ring")
        relacionados = self.catalogo.juegos_relacionados(elden)

        self.assertTrue(relacionados)
        self.assertTrue(all(otro is not elden for otro, _ in relacionados))
        pesos = [relacion.peso for _, relacion in relacionados]
        self.assertEqual(pesos, sorted(pesos, reverse=True))
        self.assertEqual(relacionados[0][0].titulo, "Dark Souls III")  # género + estudio

    def test_juegos_relacionados_respeta_el_limite(self):
        elden = self.juego("Elden Ring")
        self.assertEqual(len(self.catalogo.juegos_relacionados(elden, limite=2)), 2)
        self.assertEqual(self.catalogo.juegos_relacionados(elden, limite=0), [])

    def test_carga_invalida_no_deja_el_grafo_desincronizado(self):
        antes = self.catalogo.resumen_red()
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "roto.json"
            ruta.write_text(
                json.dumps([{"id": 99, "titulo": "Roto", "genero": "RPG"}]),
                encoding="utf-8",
            )
            with self.assertRaises(TypeError):
                self.catalogo.cargar_desde_json(str(ruta))

        self.assertEqual(self.catalogo.resumen_red(), antes)
        self.assertEqual(self.catalogo.resumen_red()["vertices"], len(self.catalogo))


class TestTerminalV5(unittest.TestCase):
    def setUp(self):
        self.catalogo = Catalogo()
        self.catalogo.cargar_desde_json("datos/videojuegos.json")

    def ejecutar(self, entradas):
        salida = io.StringIO()
        with patch("builtins.input", side_effect=entradas), patch("sys.stdout", salida):
            Terminal(self.catalogo).iniciar()
        return salida.getvalue()

    def test_menu_v5_y_juegos_relacionados(self):
        texto = self.ejecutar(["6", "elden ring", "0"])
        self.assertIn("TERMINAL (v5)", texto)
        self.assertIn("6. Ver juegos relacionados", texto)
        self.assertIn("7. Relación entre dos juegos", texto)
        self.assertIn("Juegos relacionados con 'Elden Ring':", texto)
        self.assertIn("Dark Souls III — similitud 7", texto)

    def test_juegos_relacionados_con_titulo_inexistente(self):
        self.assertIn("No encontramos 'xyz'.", self.ejecutar(["6", "xyz", "0"]))

    def test_relacion_entre_dos_juegos(self):
        texto = self.ejecutar(["7", "elden ring", "dark souls iii", "0"])
        self.assertIn("están relacionados (similitud 7)", texto)
        self.assertIn("- mismo género (RPG)", texto)
        self.assertIn("- mismo desarrollador (FromSoftware)", texto)
        self.assertIn("- tags compartidos (difícil, fantasía oscura)", texto)

    def test_relacion_entre_dos_juegos_sin_conexion_o_invalidos(self):
        sin_relacion = self.ejecutar(
            ["7", "elden ring", "portal 2", "0"]
        )
        self.assertIn("no tienen relación directa", sin_relacion)
        self.assertIn("No encontramos 'xyz'.", self.ejecutar(["7", "xyz", "0"]))
        self.assertIn("No encontramos 'abc'.", self.ejecutar(["7", "elden ring", "abc", "0"]))
        self.assertIn(
            "Elegí dos videojuegos distintos.",
            self.ejecutar(["7", "elden ring", "ELDEN RING", "0"]),
        )

    def test_terminal_permite_buscar_por_tag_y_muestra_tags_en_la_ficha(self):
        filtrados = self.ejecutar(["3", "mundo abierto", "0"])
        self.assertIn("Elden Ring", filtrados)
        self.assertIn("Minecraft", filtrados)
        self.assertNotIn("Portal 2 (", filtrados)
        ficha = self.ejecutar(["1", "elden ring", "0"])
        self.assertIn("Tags: mundo abierto, difícil, fantasía oscura", ficha)


if __name__ == "__main__":
    unittest.main()
