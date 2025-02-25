class LinesCountReport:
    project_name: str
    logical_lines_count: int
    physical_lines_count: int

    def __init__(
        self, project_name: str, logical_lines_count: int, physical_lines_count: int
    ):
        self.project_name = project_name
        self.logical_lines_count = logical_lines_count
        self.physical_lines_count = physical_lines_count

    def __str__(self):
        return (
            f"Project: {self.project_name}\n"
            f"Logical lines: {self.logical_lines_count}\n"
            f"Physical lines: {self.physical_lines_count}\n"
        )
