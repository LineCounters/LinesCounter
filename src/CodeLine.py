class CodeLine():
    def __init__(self, line_type:str, physical_lines_amount:int, logical_lines_amount:int):
        self._line_type:str = line_type
        self._physical_lines_amount:int = physical_lines_amount
        self._logical_lines_amount:int = logical_lines_amount
    
    def get_physical_lines_amount(self) -> int:
        return self._physical_lines_amount
    
    def get_logical_lines_amount(self) -> int:
        return self._logical_lines_amount
    