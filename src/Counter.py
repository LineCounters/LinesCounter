from LineBuilder import LineBuilder
from CodeLine import CodeLine

class Counter():
    def __init__(self, raw_lines: str):
        self._classified_lines: list[CodeLine] = LineBuilder(raw_lines=raw_lines).get_built_lines()
    
    def count_logical_lines(self) -> int:
        logical_count = 0
        for line in self._classified_lines:
            logical_count += line.get_logical_lines_amount()
        return logical_count
    
    def count_physical_lines(self) -> int:
        physical_count = 0
        for line in self._classified_lines:
            physical_count += line.get_physical_lines_amount()
        return physical_count
