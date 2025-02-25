from .models.lines_count_report import LinesCountReport

from .usecases.count_logical_lines_from_project import (
    count_logical_lines_from_project,
)
from .usecases.count_physical_lines_from_project import (
    count_physical_lines_from_project,
)


def main():
    project_name = input("Please enter the project name: ")

    project_path = input("Please enter the project path: ")

    try:
        project_logical_lines_count = count_logical_lines_from_project(project_path)
        project_physical_lines_count = count_physical_lines_from_project(project_path)

        print(
            LinesCountReport(
                project_name, project_logical_lines_count, project_physical_lines_count
            )
        )
    except Exception as error:
        print(
            f"Oh no! An error ocurred while getting the lines count. Verify that the project path is correct: {error}"
        )


if __name__ == "__main__":
    main()
