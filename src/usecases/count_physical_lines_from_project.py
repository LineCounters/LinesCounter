from ..helpers.get_all_python_file_paths_from_directory import (
    get_all_python_file_paths_from_directory,
)
from ..helpers.get_lines_with_visible_content_from_file import (
    get_lines_with_visible_content_from_file,
)
from ..helpers.remove_all_comments_from_content_lines import (
    remove_all_comments_from_content_lines,
)


def count_physical_lines_from_project(project_path: str) -> int:
    python_file_paths_in_project = get_all_python_file_paths_from_directory(
        project_path
    )

    project_physical_lines_count = 0

    for file_path in python_file_paths_in_project:
        lines_with_visible_content = get_lines_with_visible_content_from_file(file_path)

        lines_without_comments = remove_all_comments_from_content_lines(
            lines_with_visible_content
        )

        physical_lines_count_in_file = len(lines_without_comments)

        project_physical_lines_count += physical_lines_count_in_file

    return project_physical_lines_count
