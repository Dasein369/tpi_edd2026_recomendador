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
            elif opcion == "0":
                print("¡Hasta la próxima!")
                break
            else:
                print("Opción inválida.")
            print()

    def _mostrar_menu(self) -> None:
        print("=" * 40)
        print(" 🎮 PIXEXPERIENCE — TERMINAL")
        print("=" * 40)
        print("1. Buscar videojuego")
        print("2. Listar todos los videojuegos")
        print("3. Filtrar por categoría")
        print("0. Salir")
        print("-" * 40)

    def _buscar(self) -> None:
        titulo = input("Título a buscar: ").strip()
        resultado = self._catalogo.buscar(titulo)
        if resultado:
            print(f"Encontrado: {resultado}")
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
