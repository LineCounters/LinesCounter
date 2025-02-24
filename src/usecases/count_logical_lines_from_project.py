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

        project_logical_lines_count += logical_lines_count_in_file

    return project_logical_lines_count


def extract_logical_lines(code_lines: list[str]) -> list[str]:
    logical_lines = []
    current_parts = []
    multiline_active = False
    parentheses_level = 0
    current_indentation = ""
    backslash_continuation = False

    i = 0
    while i < len(code_lines):
        line = code_lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        # Get indentation of the current line
        current_line_indent = line[: len(line) - len(line.lstrip())]

        # Store initial indentation when starting a new statement
        if not multiline_active and not backslash_continuation and stripped:
            current_indentation = current_line_indent

        # Handle semicolons when not in a multiline context
        if ";" in stripped and not multiline_active and not backslash_continuation:
            parts = [part.strip() for part in stripped.split(";") if part.strip()]
            logical_lines.extend(parts)
            i += 1
            continue

        # Handle backslash continuation
        if stripped.endswith("\\"):
            if not backslash_continuation:
                current_parts = [stripped[:-1].strip()]
                backslash_continuation = True
            else:
                current_parts.append(stripped[:-1].strip())
            i += 1
            continue

        # Track parentheses
        parentheses_level += (
            stripped.count("(") + stripped.count("[") + stripped.count("{")
        )
        parentheses_level -= (
            stripped.count(")") + stripped.count("]") + stripped.count("}")
        )

        # Handle backslash continuation end
        if backslash_continuation:
            current_parts.append(stripped)
            logical_lines.append(" ".join(current_parts))
            current_parts = []
            backslash_continuation = False
            i += 1
            continue

        # Start or continue parentheses multiline
        if parentheses_level > 0:
            if not multiline_active:  # Starting new multiline
                multiline_active = True
                current_parts = [stripped]
            else:
                current_parts.append(stripped)
        else:
            if multiline_active:
                # Complete multiline statement
                current_parts.append(stripped)
                # Join and clean up
                joined = "".join(current_parts)
                cleaned = ""
                prev_char = ""
                for char in joined:
                    if char.isspace():
                        if (
                            prev_char
                            and not prev_char.isspace()
                            and prev_char not in "({["
                        ):
                            if not (cleaned and cleaned[-1].isspace()) and not (
                                cleaned and cleaned[-1].isspace()
                            ):
                                cleaned += " "
                    else:
                        cleaned += char
                    prev_char = char
                logical_lines.append(current_indentation + cleaned.strip())
                current_parts = []
                multiline_active = False
            else:
                # Regular single line - keep original indentation
                logical_lines.append(line)

        i += 1

    # Handle any remaining multiline
    if current_parts:
        joined = "".join(current_parts)
        cleaned = ""
        prev_char = ""
        for char in joined:
            if char.isspace():
                if prev_char and not prev_char.isspace() and prev_char not in "({[":
                    if not (cleaned and cleaned[-1].isspace()):
                        cleaned += " "
            else:
                cleaned += char
            prev_char = char
        logical_lines.append(current_indentation + cleaned.strip())

    return logical_lines
