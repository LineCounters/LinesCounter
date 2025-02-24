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

        logical_lines_count_in_file = len(extract_logical_lines(lines_without_comments))
        print(f"File: {file_path} - Logical lines: {logical_lines_count_in_file}")
        project_logical_lines_count += logical_lines_count_in_file

    return project_logical_lines_count


def extract_logical_lines(code_lines: list[str]) -> list[str]:
    if not code_lines:
        return []

    # Join lines to process them together
    code_string = "\n".join(code_lines)

    logical_lines = []
    in_multiline = False
    parentheses_level = 0

    # Split by semicolons first to handle multiple statements per line
    # but preserve semicolons in strings
    in_string = False
    string_char = None
    semicolon_splits = []
    current_split = []

    for char in code_string:
        if char in "\"'":
            if not in_string:
                in_string = True
                string_char = char
            elif string_char == char:
                in_string = False
        elif char == ";" and not in_string:
            semicolon_splits.extend(["".join(current_split), ";"])
            current_split = []
        else:
            current_split.append(char)

    if current_split:
        semicolon_splits.append("".join(current_split))

    # Process each potential logical line
    current_line_parts = []

    for token in semicolon_splits:
        if token == ";":
            if current_line_parts:
                logical_lines.append("".join(current_line_parts).strip())
                current_line_parts = []
            continue

        lines = token.split("\n")

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Handle explicit line continuation
            if line.endswith("\\"):
                in_multiline = True
                current_line_parts.append(line[:-1].strip() + " ")
                continue

            # Count parentheses/brackets/braces
            parentheses_level += line.count("(") + line.count("[") + line.count("{")
            parentheses_level -= line.count(")") + line.count("]") + line.count("}")

            current_line_parts.append(line + " ")

            # If we're not in a multiline construct, add as a logical line
            if not in_multiline and parentheses_level == 0:
                if current_line_parts:
                    logical_lines.append("".join(current_line_parts).strip())
                    current_line_parts = []

            # Reset multiline flag if we're not in parentheses
            if parentheses_level == 0:
                in_multiline = False

    # Handle any remaining line
    if current_line_parts and not in_multiline and parentheses_level == 0:
        logical_lines.append("".join(current_line_parts).strip())

    return logical_lines
