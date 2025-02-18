from Counter import Counter
from FileReader import FileReader


class CodeFile:
    def __init__(self, file_path: str):
        self._file_path: str = file_path
        self._lines: list[str] = FileReader(self._file_path).get_lines()
        self._logical_lines: int = Counter(self._lines).count_logical_lines()
        self._physical_lines: int = Counter(self._lines).count_physical_lines()

    def __str__(self) -> str:
        return (
            f"The file: {self._file_path}.\n"
            "Has the following metrics:\n"
            f"Physical Lines: {self._physical_lines}\n"
            f"Logical Lines: {self._logical_lines}"
        )
