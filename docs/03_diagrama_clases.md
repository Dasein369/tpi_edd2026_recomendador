# Diagrama de clases

> Actualizado en TP6: búsqueda AVL, jerarquía de categorías y ranking mediante montículo.
> Se conservan el BST de TP3 y el árbol estático experimental de TP2.

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
        -arbol_titulos: ArbolAVL
        -arbol_categorias: ArbolGeneral
        -monticulo_rating: MonticuloMaximo
        +cargar_desde_json(ruta) None
        +buscar(titulo) Videojuego
        +top_n(cantidad=15) list
        +buscar_parcial(texto) list
        +listar() list
        +filtrar(genero, desarrollador, rating_minimo) list
        +len() int
    }

    class Terminal {
        -catalogo: Catalogo
        +iniciar() None
    }

    class ArbolAVL {
        -raiz: NodoAVL
        -tam: int
        -rotaciones: int
        +insertar(videojuego) None
        +buscar(titulo) Videojuego
        +pasos_busqueda(titulo) int
        +inorder() list
        +preorder() list
        +postorder() list
        +altura() int
        +es_valido() bool
        +len() int
    }

    class NodoAVL {
        -videojuego: Videojuego
        -orden: int
        -altura: int
        -izquierda: NodoAVL
        -derecha: NodoAVL
    }

    class ArbolBinarioBusqueda {
        -raiz: NodoArbol
        -tam: int
        +insertar(videojuego) None
        +buscar(titulo) Videojuego
        +inorder() list
        +preorder() list
        +postorder() list
        +altura() int
        +len() int
    }

    class NodoArbol {
        -videojuego: Videojuego
        -izquierda: NodoArbol
        -derecha: NodoArbol
    }

    class ArbolBusquedaBalanceada {
        -raiz: NodoBusqueda
        -tam: int
        +buscar(titulo) Videojuego
        +altura() int
        +inorder() list
        +len() int
    }

    class NodoBusqueda {
        -videojuego: Videojuego
        -izquierda: NodoBusqueda
        -derecha: NodoBusqueda
    }

    class MonticuloMaximo {
        -entradas: list
        +insertar(valor) None
        +ver_maximo() Videojuego
        +extraer_maximo() Videojuego
        +mayores(cantidad) list
    }

    class ArbolGeneral {
        -raiz: NodoGeneral
        +buscar(predicado) NodoGeneral
        +preorden() list
        +postorden() list
    }

    class NodoGeneral {
        -valor: Categoria
        -hijos: list
        +agregar_hijo(valor) NodoGeneral
    }

    Terminal --> Catalogo : usa
    Catalogo "1" o-- "*" Videojuego : contiene
    Catalogo --> ArbolAVL : buscar por título
    Catalogo --> ArbolGeneral : explorar categorías
    Catalogo --> MonticuloMaximo : Top 15 por rating
    ArbolGeneral "1" o-- "*" NodoGeneral : contiene
    ArbolAVL "1" o-- "*" NodoAVL : contiene
    NodoAVL --> Videojuego : referencia
    ArbolBinarioBusqueda "1" o-- "*" NodoArbol : contiene
    NodoArbol --> Videojuego : referencia
    ArbolBusquedaBalanceada "1" o-- "*" NodoBusqueda : contiene
    NodoBusqueda --> Videojuego : referencia
```

> **Nota:** `Catalogo.buscar()` delega en `ArbolAVL.buscar()`. `Catalogo.top_n()` consulta
> el montículo construido al cargar el catálogo; `mayores()` no altera su contenido.
> `ArbolBinarioBusqueda` ya no
> está en producción: queda como punto de comparación de `benchmark_tp4.py`. La búsqueda
> secuencial (`algoritmos/busqueda_secuencial.py`) se conserva para la comparación. El
> `ArbolBusquedaBalanceada` sigue aislado en el experimento TP2 y no se reutiliza: la
> nueva estructura se construye insertando cada juego en el orden de carga.

## Diferencias respecto del diagrama inicial (TP0)

- La clase de dominio se llama `Videojuego` (en TP0 figuraba como `Juego`).
- `Videojuego` todavía no tiene el atributo `tags`; se mantiene pendiente para ampliar
  RF04 y RF05.
- `ArbolGeneral` se integró en TP5 y `MonticuloMaximo` en TP6. El grafo y el
  `Recomendador` se incorporan en etapas posteriores. Ver `04-diagrama-datos.md`.
- Se agregaron `Catalogo` y `Terminal`, que en TP0 no estaban diagramadas.
- TP2 agregó `ArbolBusquedaBalanceada` y `NodoBusqueda`, exclusivas del experimento de
  comparación de estrategias de búsqueda; no reemplazan al BST que se construye en TP3.
