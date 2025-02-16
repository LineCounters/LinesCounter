class Line:
    def __init__(
        self, line_type: str, physical_lines_count: int, _logical_lines_count: int
    ):
        self._line_type: str = line_type
        self._physical_lines_count: int = physical_lines_count
        self._logical_lines_count: int = _logical_lines_count

    def get_physical_lines_count(self) -> int:
        return self._physical_lines_count

    def get_logical_lines_count(self) -> int:
        return self._logical_lines_count
