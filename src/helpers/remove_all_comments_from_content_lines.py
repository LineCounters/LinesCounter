from re import match as is_string_matching
from re import sub as replace_string_matching


def remove_all_comments_from_content_lines(
    content_lines: list[str],
) -> list[str]:
    lines_without_inline_comments = remove_inline_comments_from_content_lines(
        content_lines
    )
    lines_without_docstrings = remove_docstrings_from_content_lines(
        lines_without_inline_comments
    )

    return lines_without_docstrings


def remove_inline_comments_from_content_lines(content_lines: list[str]) -> list[str]:
    lines_of_code = []

    inline_comment_pattern = r"#.*$"

    for content_line in content_lines:
        content_line = replace_string_matching(inline_comment_pattern, "", content_line)

        if content_line.strip() != "":
            lines_of_code.append(content_line)

    return lines_of_code


def remove_docstrings_from_content_lines(content_lines: list[str]) -> list[str]:
    lines_of_code = []

    currently_in_docstring = False

    for content_line in content_lines:
        if currently_in_docstring:
            # This means that the current line is the last line of the docstring
            if contains_docstring_characters(content_line):
                currently_in_docstring = False
        else:
            if contains_docstring_characters(content_line):
                if is_inline_docstring(content_line):
                    continue

                currently_in_docstring = True
                continue

            lines_of_code.append(content_line)

    return lines_of_code


def is_inline_docstring(string: str) -> bool:
    return string.count('"""') == 2 or string.count("'''") == 2


def contains_docstring_characters(string: str) -> bool:
    docstring_pattern = r'^\s*(\'\'\'|""")'

    return is_string_matching(docstring_pattern, string) is not None
