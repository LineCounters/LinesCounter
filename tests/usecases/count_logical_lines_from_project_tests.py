from unittest import TestCase

from src.usecases.count_logical_lines_from_project import (
    count_logical_lines_from_project,
    _extract_logical_lines,
)


class ExtractLogicalLinesTests(TestCase):
    def test_that_empty_lines_should_return_empty_list_of_logical_lines(self):
        logical_lines = _extract_logical_lines([])

        self.assertEqual(logical_lines, [])

    def test_that_a_string_with_a_logical_line_inside_should_return_empty_list_of_logical_lines(
        self,
    ):
        logical_lines = _extract_logical_lines(
            ["'def function():'", "'    if x != 0:'", "        'return x'"]
        )

        self.assertEqual(logical_lines, [])

    def test_that_a_list_comprehension_should_return_empty_list_of_logical_lines(self):
        logical_lines = _extract_logical_lines(["[x for x in range(10) if x % 2 == 0]"])

        self.assertEqual(logical_lines, [])

    def test_that_a_single_logical_line_should_return_one_logical_line(self):
        logical_lines = _extract_logical_lines(["def function():"])

        self.assertEqual(logical_lines, ["def function():"])

    def test_that_match_case_expresion_should_return_one_logical_line(self):
        logical_lines = _extract_logical_lines(
            ["match number:", "    case 1:", "        print('one')"]
        )

        self.assertEqual(logical_lines, ["match number:"])


class CountLogicalLinesFromProjectTests(TestCase):
    def test_that_a_directory_without_python_files_should_return_zero(self):
        project_logical_lines_count = count_logical_lines_from_project(
            "tests/assets/empty_dir"
        )

        self.assertEqual(project_logical_lines_count, 0)

    def test_that_a_project_with_only_comments_should_return_zero(self):
        project_logical_lines_count = count_logical_lines_from_project(
            "tests/assets/empty_python_project"
        )

        self.assertEqual(project_logical_lines_count, 0)

    def test_that_a_project_with_only_code_should_count_the_logical_lines(self):
        project_logical_lines_count = count_logical_lines_from_project(
            "tests/assets/only_code_python_project"
        )

        self.assertEqual(project_logical_lines_count, 19)

    def test_that_a_project_with_code_and_comments_should_count_the_logical_lines(
        self,
    ):
        project_logical_lines_count = count_logical_lines_from_project(
            "tests/assets/documented_python_project"
        )

        self.assertEqual(project_logical_lines_count, 19)
