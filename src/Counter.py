from LineBuilder import LineBuilder
from Line import Line


class Counter:
    def __init__(self, raw_lines: str):
        self._classified_lines: list[Line] = LineBuilder(
            raw_lines=raw_lines
        ).get_built_lines()

    def count_logical_lines(self) -> int:
        logical_count: int = 0
        for line in self._classified_lines:
            logical_count += line._logical_lines_count
        return logical_count

    def count_physical_lines(self) -> int:
        physical_count = 0
        for line in self._classified_lines:
            physical_count += line._physical_lines_count
        return physical_count
