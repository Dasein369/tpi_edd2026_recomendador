class Videojuego:
    """Representa un elemento del catálogo."""

    def __init__(self, id: int, titulo: str, genero: str, desarrollador: str, rating: float, horas_jugadas: int):
        self._id = id
        self._titulo = titulo
        self._genero = genero
        self._desarrollador = desarrollador
        self._rating = rating
        self._horas_jugadas = horas_jugadas

    @property
    def id(self) -> int:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def genero(self) -> str:
        return self._genero

    @property
    def desarrollador(self) -> str:
        return self._desarrollador

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def horas_jugadas(self) -> int:
        return self._horas_jugadas

    def __repr__(self) -> str:
        return f"{self._titulo} ({self._genero}) ⭐{self._rating}"
