from unittest import TestCase

from src.helpers.get_lines_with_visible_content_from_file import (
    get_lines_with_visible_content_from_file,
)


class GetLinesWithVisibleContentFromFileTests(TestCase):
    def test_that_an_empty_file_should_return_zero_lines(self):
        file_content = get_lines_with_visible_content_from_file(
            "tests/assets/only_code_python_project/main.py"
        )

        self.assertEqual(file_content, [])

    def test_that_a_file_with_only_empty_lines_should_return_zero_lines(self):
        file_content = get_lines_with_visible_content_from_file(
            "tests/assets/only_code_python_project/docs.py"
        )

        self.assertEqual(file_content, [])

    def test_that_a_file_has_more_than_one_line(self):
        file_content = get_lines_with_visible_content_from_file(
            "tests/assets/only_code_python_project/models/fruit.py"
        )

        self.assertGreaterEqual(len(file_content), 6)
