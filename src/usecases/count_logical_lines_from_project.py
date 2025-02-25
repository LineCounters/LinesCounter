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
    state = {
        "multiline_buffer": [],
        "parentheses_level": 0,
        "current_line_indentation": "",
        "is_multiline_active": False,
        "is_backslash_continuation": False,
    }

    logical_lines = []

    for code_line in code_lines:
        logical_lines.extend(_process_line(code_line, state))

    if state["multiline_buffer"]:
        logical_lines.append(
            state["current_line_indentation"]
            + _consolidate_multiline(
                state["multiline_buffer"],
            )
        )

    return logical_lines


def _get_line_indentation(line: str) -> str:
    return line[: len(line) - len(line.lstrip())]


def _calculate_nesting_level(line: str) -> int:
    return (line.count("(") + line.count("[") + line.count("{")) - (
        line.count(")") + line.count("]") + line.count("}")
    )


def _split_statements_by_semicolon(line: str) -> list[str]:
    return [statement.strip() for statement in line.split(";") if statement.strip()]


def _consolidate_multiline(multiline_parts: list[str]) -> str:
    merged_multiline_content = "".join(multiline_parts)
    trimmed_tokens_from_multiline = merged_multiline_content.split()

    return " ".join(trimmed_tokens_from_multiline)


def _handle_line_continuation_by_backslash(
    line: str, multiline_buffer: list[str], is_backslash_continuation: bool
) -> tuple[list[str], bool]:
    line_without_backslash = line[:-1].strip()

    if is_backslash_continuation:
        multiline_buffer.append(line_without_backslash)
        return multiline_buffer, True

    return [line_without_backslash], True


def _handle_multiline_statement(
    line: str, multiline_buffer: list[str], is_in_multiline_context: bool
) -> tuple[list[str], bool]:
    if is_in_multiline_context:
        multiline_buffer.append(line)
        return multiline_buffer, True

    return [line], True


def _process_line(line: str, current_state: dict) -> list[str]:
    line_stripped = line.strip()

    line_is_not_part_of_multiline = not (
        current_state["is_multiline_active"]
        or current_state["is_backslash_continuation"]
    )

    if line_is_not_part_of_multiline:
        current_state["current_line_indentation"] = _get_line_indentation(line)

    if ";" in line_stripped and line_is_not_part_of_multiline:
        return _split_statements_by_semicolon(line_stripped)

    if line_stripped.endswith("\\"):
        (
            current_state["multiline_buffer"],
            current_state["is_backslash_continuation"],
        ) = _handle_line_continuation_by_backslash(
            line_stripped,
            current_state["multiline_buffer"],
            current_state["is_backslash_continuation"],
        )

        return []

    logical_lines = []
    current_state["parentheses_level"] += _calculate_nesting_level(line_stripped)

    if current_state["is_backslash_continuation"]:
        logical_lines.append(
            " ".join(current_state["multiline_buffer"] + [line_stripped])
        )

        current_state["multiline_buffer"] = []
        current_state["is_backslash_continuation"] = False

        return logical_lines

    if current_state["parentheses_level"] > 0:
        current_state["multiline_buffer"], current_state["is_multiline_active"] = (
            _handle_multiline_statement(
                line_stripped,
                current_state["multiline_buffer"],
                current_state["is_multiline_active"],
            )
        )
    else:
        if current_state["is_multiline_active"]:
            logical_lines.append(
                current_state["current_line_indentation"]
                + _consolidate_multiline(
                    current_state["multiline_buffer"] + [line_stripped]
                )
            )
            current_state["multiline_buffer"] = []
            current_state["is_multiline_active"] = False
        else:
            logical_lines.append(line)

    return logical_lines
