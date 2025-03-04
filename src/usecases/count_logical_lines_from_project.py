from re import match

from ..helpers.get_all_python_file_paths_from_directory import (
    get_all_python_file_paths_from_directory,
)
from ..helpers.get_lines_with_visible_content_from_file import (
    get_lines_with_visible_content_from_file,
)
from ..helpers.remove_all_comments_from_content_lines import (
    remove_all_comments_from_content_lines,
)


def count_logical_lines_from_project(project_path: str) -> int:
    python_file_paths_in_project = get_all_python_file_paths_from_directory(
        project_path
    )

    project_logical_lines_count = 0

    for file_path in python_file_paths_in_project:
        lines_with_visible_content = get_lines_with_visible_content_from_file(file_path)

        lines_without_comments = remove_all_comments_from_content_lines(
            lines_with_visible_content
        )

        logical_lines_count_in_file = len(
            _extract_logical_lines(lines_without_comments)
        )

        project_logical_lines_count += logical_lines_count_in_file

    return project_logical_lines_count


def _extract_logical_lines(content_lines: list[str]) -> list[str]:
    logical_lines = []

    for content_line in content_lines:
        if _is_logical_line(content_line):
            logical_lines.append(content_line)

    return logical_lines


def _is_logical_line(line: str) -> bool:
    BLOCK_DEFINERS_PATTERNS = [
        r"^\s*class\s+\w+",
        r"^\s*def\s+\w+",
        r"^\s*if\s+",
        r"^\s*while\s+",
        r"^\s*for\s+",
        r"^\s*try\s*:",
        r"^\s*with\s+",
        r"^\s*match\s+",
    ]

    for block_definer_pattern in BLOCK_DEFINERS_PATTERNS:
        if match(block_definer_pattern, line):
            return True

    return False
