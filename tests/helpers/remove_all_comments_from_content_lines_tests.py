# noqa

from unittest import TestCase

from src.helpers.remove_all_comments_from_content_lines import (
    remove_all_comments_from_content_lines,
)


class RemoveAllCommentsFromContentLinesTests(TestCase):
    def test_that_an_empty_list_of_lines_should_return_an_empty_list(self):
        content_lines = []

        lines_of_code = remove_all_comments_from_content_lines(content_lines)

        self.assertEqual(lines_of_code, [])

    def test_that_a_list_of_lines_with_only_comments_should_return_an_empty_list(self):
        content_lines = ["# This is a comment", "# This is another comment"]

        lines_of_code = remove_all_comments_from_content_lines(content_lines)

        self.assertEqual(lines_of_code, [])

    def test_that_a_list_of_lines_with_only_docstrings_should_return_an_empty_list(
        self,
    ):
        content_lines = [
            "'''This is a docstring'''",
            "'''",
            "Inside of a docstring",
            "Also inside of a docstring",
            "'''",
            '"""This is a docstring"""',
            '"""',
            "This is inside of a docstring",
            "This is also inside of a docstring",
            '"""',
        ]

        lines_of_code = remove_all_comments_from_content_lines(content_lines)

        self.assertEqual(lines_of_code, [])

    def test_that_a_list_of_lines_with_comments_and_docstrings_should_return_only_the_lines_of_code(
        self,
    ):
        content_lines = [
            "# This is a inline comment",
            "def get_number_one():",
            "    '''This is a inline docstring'''",
            "    '''",
            "       This is inside of a docstring",
            "       This is also inside of a docstring",
            "    '''",
            "    # This is a comment",
            "    return 1",
            '"""This is a docstring"""',
            '"""',
            "   This is inside of a docstring",
            "   This is also inside of a docstring",
            '"""',
        ]

        lines_of_code = remove_all_comments_from_content_lines(content_lines)

        self.assertEqual(
            lines_of_code,
            [
                "def get_number_one():",
                "    return 1",
            ],
        )
