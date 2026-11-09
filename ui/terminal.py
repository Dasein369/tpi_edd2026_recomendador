from servicios.catalogo import Catalogo


class Terminal:
    """Interfaz de línea de comandos."""

    def __init__(self, catalogo: Catalogo) -> None:
        self._catalogo = catalogo

    def iniciar(self) -> None:
        while True:
            self._mostrar_menu()
            opcion = input("Opción: ").strip()

            if opcion == "1":
                self._buscar()
            elif opcion == "2":
                self._listar()
            elif opcion == "3":
                self._filtrar()
            elif opcion == "4":
                self._explorar_categorias()
            elif opcion == "5":
                self._ver_top_15()
            elif opcion == "6":
                self._ver_relacionados()
            elif opcion == "7":
                self._ver_relacion_entre_dos()
            elif opcion == "0":
                print("¡Hasta la próxima!")
                break
            else:
                print("Opción inválida.")
            print()

    def _mostrar_menu(self) -> None:
        print("=" * 40)
        print(" 🎮 PIXPERIENCE — TERMINAL (v5)")
        print("=" * 40)
        print("1. Buscar videojuego")
        print("2. Listar todos los videojuegos")
        print("3. Filtrar por categoría")
        print("4. Explorar categorías")
        print("5. Ver Top 15 por rating")
        print("6. Ver juegos relacionados")
        print("7. Relación entre dos juegos")
        print("0. Salir")
        print("-" * 40)

    def _buscar(self) -> None:
        titulo = input("Título a buscar: ").strip()
        resultado = self._catalogo.buscar(titulo)
        if resultado:
            print("Ficha del videojuego:")
            print(f"Título: {resultado.titulo}")
            print(f"Género: {resultado.genero}")
            print(f"Desarrollador: {resultado.desarrollador}")
            print(f"Rating: {resultado.rating}")
            print(f"Horas jugadas (usuario): {resultado.horas_jugadas}")
        else:
            print(f"No encontramos '{titulo}'.")

    def _listar(self) -> None:
        for videojuego in self._catalogo.listar():
            print(f"- {videojuego}")

    def _filtrar(self) -> None:
        genero = input("Categoría: ").strip()
        resultados = self._catalogo.filtrar(genero)
        if resultados:
            for videojuego in resultados:
                print(f"- {videojuego}")
        else:
            print(f"No hay elementos en '{genero}'.")

    def _explorar_categorias(self) -> None:
        print("Categorías disponibles:")
        for profundidad, nombre in self._catalogo.listar_categorias():
            print(f"{'  ' * profundidad}{nombre}")

        nombre = input("Categoría a explorar (Enter para volver): ").strip()
        if not nombre:
            return

        videojuegos = self._catalogo.explorar_categoria(nombre)
        if videojuegos is None:
            print(f"No existe la categoría '{nombre}'.")
        elif not videojuegos:
            print(f"No hay videojuegos en '{nombre}'.")
        else:
            print(f"Videojuegos en '{nombre}':")
            for videojuego in videojuegos:
                print(f"- {videojuego}")

    def _ver_top_15(self) -> None:
        videojuegos = self._catalogo.top_n(15)
        if not videojuegos:
            print("No hay videojuegos para armar el ranking.")
            return

        print("Top 15 de videojuegos por rating:")
        for puesto, videojuego in enumerate(videojuegos, start=1):
            print(f"{puesto:>2}. {videojuego.titulo} — ⭐ {videojuego.rating:.1f}")

    def _ver_relacionados(self) -> None:
        titulo = input("Título del videojuego: ").strip()
        videojuego = self._catalogo.buscar(titulo)
        if videojuego is None:
            print(f"No encontramos '{titulo}'.")
            return

        relacionados = self._catalogo.juegos_relacionados(videojuego, limite=10)
        if not relacionados:
            print(f"'{videojuego.titulo}' no tiene juegos relacionados.")
            return

        print(f"Juegos relacionados con '{videojuego.titulo}':")
        for otro, relacion in relacionados:
            print(f"- {otro.titulo} — similitud {relacion.peso} ({', '.join(relacion.motivos)})")

    def _ver_relacion_entre_dos(self) -> None:
        titulo_a = input("Primer título: ").strip()
        primero = self._catalogo.buscar(titulo_a)
        if primero is None:
            print(f"No encontramos '{titulo_a}'.")
            return

        titulo_b = input("Segundo título: ").strip()
        segundo = self._catalogo.buscar(titulo_b)
        if segundo is None:
            print(f"No encontramos '{titulo_b}'.")
            return
        if primero is segundo:
            print("Elegí dos videojuegos distintos.")
            return

        relacion = self._catalogo.relacion_entre(primero, segundo)
        if relacion is None:
            print(f"'{primero.titulo}' y '{segundo.titulo}' no tienen relación directa.")
        else:
            print(f"'{primero.titulo}' y '{segundo.titulo}' están relacionados (similitud {relacion.peso}):")
            for motivo in relacion.motivos:
                print(f"- {motivo}")
