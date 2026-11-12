# Diagrama de clases

> Actualizado en TP8: búsqueda AVL, categorías, ranking, grafo y recorridos BFS/DFS.
> Se conservan el BST de TP3 y el árbol estático experimental de TP2.

```mermaid
classDiagram
    class Videojuego {
        -id: int
        -titulo: str
        -genero: str
        -tags: tuple
        -desarrollador: str
        -rating: float
        -horas_jugadas: int
        +id() int
        +titulo() str
        +genero() str
        +tags() tuple
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
        -grafo: Grafo
        +cargar_desde_json(ruta) None
        +buscar(titulo) Videojuego
        +top_n(cantidad=15) list
        +juegos_relacionados(videojuego, limite) list
        +relacion_entre(a, b) Relacion
        +camino_de_relaciones(origen, destino) list
        +explorar_red(origen) list
        +resumen_red() dict
        +buscar_parcial(texto) list
        +listar() list
        +filtrar(genero, desarrollador, rating_minimo, tag) list
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

    class Grafo {
        -adyacencia: dict
        +agregar_vertice(vertice) None
        +agregar_arista(a, b, peso) None
        +tiene_arista(a, b) bool
        +peso(a, b) float
        +vecinos(vertice) dict
        +grado(vertice) int
        +camino_bfs(origen, destino) list
        +recorrido_dfs(origen) list
        +aristas() Iterator
        +cantidad_aristas() int
        +densidad() float
        +len() int
    }

    class Relacion {
        +peso: int
        +motivos: tuple
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
    Catalogo --> Grafo : juegos relacionados
    Grafo "1" o-- "*" Videojuego : vértices
    Catalogo ..> Relacion : motivo y peso
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
> `Catalogo` construye el `Grafo` al cargar los datos (`servicios/relaciones.py` define el
> criterio de similitud y la clase `Relacion`) y lo consulta en `juegos_relacionados()` y
> `relacion_entre()`.
> `ArbolBinarioBusqueda` ya no
> está en producción: queda como punto de comparación de `benchmark_tp4.py`. La búsqueda
> secuencial (`algoritmos/busqueda_secuencial.py`) se conserva para la comparación. El
> `ArbolBusquedaBalanceada` sigue aislado en el experimento TP2 y no se reutiliza: la
> nueva estructura se construye insertando cada juego en el orden de carga.

## Diferencias respecto del diagrama inicial (TP0)

- La clase de dominio se llama `Videojuego` (en TP0 figuraba como `Juego`).
- `Videojuego` incorpora `tags` en TP7 para ampliar RF04 y RF05.
- `ArbolGeneral` se integró en TP5, `MonticuloMaximo` en TP6 y `Grafo` en TP7. El
  `Recomendador` se incorpora en etapas posteriores. Ver `04_diagrama_datos.md`.
- Se agregaron `Catalogo` y `Terminal`, que en TP0 no estaban diagramadas.
- TP2 agregó `ArbolBusquedaBalanceada` y `NodoBusqueda`, exclusivas del experimento de
  comparación de estrategias de búsqueda; no reemplazan al BST que se construye en TP3.
