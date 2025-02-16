class Reader:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._lines = self._read_lines()

    def _read_lines(self):
        with open(self._file_path, "r", encoding="utf-8") as file:
            lines: list[str] = file.readlines()
            return lines

    def get_lines(self) -> list[str]:
        return self._lines
