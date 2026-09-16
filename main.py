from servicios.catalogo import Catalogo
from ui.terminal import Terminal


def main() -> None:
    catalogo = Catalogo()
    catalogo.cargar_desde_json("datos/videojuegos.json")
    print(f"Se cargaron {len(catalogo)} elementos.")
    Terminal(catalogo).iniciar()


if __name__ == "__main__":
    main()
