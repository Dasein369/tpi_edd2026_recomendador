# Diagrama de clases

> Actualizado en TP1 con la implementación.

```mermaid
classDiagram
    class Videojuego {
        -id: int
        -titulo: str
        -genero: str
        -desarrollador: str
        -rating: float
        -horas_jugadas: int
        +id() int
        +titulo() str
        +genero() str
        +desarrollador() str
        +rating() float
        +horas_jugadas() int
        +repr() str
    }

    class Catalogo {
        -elementos: list
        +cargar_desde_json(ruta) None
        +buscar(titulo) Videojuego
        +buscar_parcial(texto) list
        +listar() list
        +filtrar(genero, desarrollador, rating_minimo) list
        +len() int
    }

    class Terminal {
        -catalogo: Catalogo
        +iniciar() None
    }

    Terminal --> Catalogo : usa
    Catalogo "1" o-- "*" Videojuego : contiene
```
