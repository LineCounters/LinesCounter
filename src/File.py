from Counter import Counter
from Reader import Reader


class File:
    def __init__(self, file_path: str):
        self._file_path: str = file_path
        self._lines: list[str] = Reader(self._file_path).get_lines()
        self._logical_lines: int = Counter(self._lines).count_logical_lines()
        self._physical_lines: int = Counter(self._lines).count_physical_lines()

    def get_formatted_metrics(self) -> str:
        return (
            f"El archivo: {self._file_path}.\n"
            "Cuenta con las siguientes métricas:\n"
            f"Líneas Físicas: {self._physical_lines}\n"
            f"Líneas Lógicas: {self._logical_lines}"
        )
