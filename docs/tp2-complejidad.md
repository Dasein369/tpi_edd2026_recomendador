# TP2 — Análisis de complejidad y comparación de búsquedas

## 1. Objetivo

El sistema **PixExperience** debe permitir encontrar un videojuego por título. En TP1 esa operación se resuelve recorriendo secuencialmente la lista del catálogo. En TP2 se comparan dos estrategias para la misma necesidad:

1. **Búsqueda secuencial** sobre una lista.
2. **Búsqueda en un árbol binario de búsqueda balanceado**, construido a partir de los mismos elementos.

La comparación se realiza con 100, 1.000, 10.000 y 100.000 elementos.

## 2. Estrategia A — Búsqueda secuencial

La función `buscar_secuencial` recorre los elementos desde el comienzo y compara el título de cada videojuego con el buscado.

- Mejor caso: **Θ(1)**, cuando el primer elemento coincide.
- Caso promedio: **Θ(n)**.
- Peor caso: **Θ(n)**, cuando el elemento está al final o no existe.
- Espacio adicional: **O(1)**.

En el benchmark se busca deliberadamente el último elemento de la lista para observar el peor caso temporal.

## 3. Estrategia B — Búsqueda en árbol

`ArbolBusquedaBalanceada` ordena los elementos por título y construye un árbol binario tomando el elemento central de cada intervalo. Esto mantiene una altura logarítmica para los datasets del experimento.

En cada comparación, si el título buscado es menor se continúa por la izquierda y, si es mayor, por la derecha.

- Mejor caso: **Θ(1)**, si la raíz coincide.
- Caso promedio: **Θ(log n)**.
- Peor caso en este experimento: **Θ(log n)**, porque el árbol se construye balanceado.
- Espacio del árbol: **O(n)**.

La construcción del árbol se excluye de la medición de búsqueda. En esta implementación la construcción incluye ordenar los datos, por lo que cuesta **O(n log n)**; es un costo de preparación amortizable cuando el catálogo se consulta muchas veces.

> Esta estructura es específica del experimento de TP2. El TP3 puede incorporar un BST dinámico con inserción y recorridos dentro de la aplicación.

## 4. Diseño experimental

Para cada tamaño `n`:

1. Se generan exactamente `n` objetos `Videojuego` a partir del dataset base del proyecto.
2. Se agregan sufijos `[TP2-XXXXXX]` para garantizar títulos únicos sin cambiar el dominio.
3. Se construye el árbol antes de medir.
4. Se selecciona el último videojuego de la lista como objetivo, lo que fuerza el peor caso de la búsqueda secuencial.
5. Cada estrategia se ejecuta varias veces y se informa la **mediana de los nanosegundos por consulta**.
6. Se utiliza una cantidad de iteraciones adaptada a `n` para evitar que una medición muy corta quede dominada por el overhead del reloj.

## 5. Resultados de la última ejecución

> Los tiempos son dependientes del hardware, del sistema operativo y de la versión de Python. La tabla se actualiza automáticamente ejecutando `python -m experimentos.benchmark_tp2`.

| N elementos | Secuencial | Árbol | Relación | Altura del árbol |
|---:|---:|---:|---:|---:|
| 100 | 9.8560 µs | 0.6370 µs | 15.47x | 7 |
| 1,000 | 90.6320 µs | 1.9700 µs | 46.01x | 10 |
| 10,000 | 921.8440 µs | 1.9530 µs | 472.01x | 14 |
| 100,000 | 10121.6320 µs | 3.2380 µs | 3125.89x | 17 |

## 6. Interpretación

La búsqueda secuencial aumenta aproximadamente en proporción al tamaño de la entrada porque, en el escenario medido, tiene que revisar todos los elementos hasta llegar al objetivo. El árbol balanceado crece mucho más lentamente porque cada comparación elimina una parte importante del espacio de búsqueda.

La diferencia experimental no reemplaza el análisis teórico: los tiempos absolutos cambian según la máquina, pero las funciones de crecimiento siguen siendo distintas. Por eso la conclusión principal se expresa con complejidad asintótica: **Θ(n) frente a Θ(log n)** para los casos representados por este experimento.

## 7. Conclusión técnica

Para un catálogo pequeño, ambas estrategias pueden responder rápidamente y la simplicidad de la lista puede ser suficiente. A medida que el catálogo crece y la búsqueda se realiza muchas veces, un árbol balanceado reduce el número de comparaciones necesarias para localizar un título.

Por lo tanto, el experimento muestra una diferencia fundamental de escalabilidad: la estrategia secuencial requiere un trabajo proporcional a `n` en el peor caso, mientras que la búsqueda sobre el árbol balanceado requiere un número de pasos proporcional a `log n`.

La siguiente etapa del proyecto, TP3, consiste en llevar esta idea al producto mediante un BST integrado a la aplicación.

## 8. Cómo ejecutar

Desde la raíz del repositorio:

```bash
python -m experimentos.benchmark_tp2
```

El script genera/actualiza:

- `experimentos/resultados_tp2.csv`
- `docs/tp2-complejidad.md`

## 9. Pruebas

Desde la raíz del repositorio:

```bash
python -m unittest discover -s tests -t . -v
```
