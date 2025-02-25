from unittest import TestCase

from src.usecases.count_logical_lines_from_project import (
    count_logical_lines_from_project,
    extract_logical_lines,
)


class ExtractLogicalLinesTests(TestCase):
    def test_that_empty_lines_should_return_empty_list(self):
        logical_lines = extract_logical_lines([])

        self.assertEqual(logical_lines, [])

    def test_that_a_single_logical_line_should_return_single_line(self):
        logical_lines = extract_logical_lines(["def function():"])

        self.assertEqual(logical_lines, ["def function():"])

    def test_that_a_single_multiline_logical_line_should_return_single_line(self):
        logical_lines = extract_logical_lines(["def test(", "    arg):"])

        self.assertEqual(logical_lines, ["def test(arg):"])

    def test_that_multiple_logical_lines_should_return_multiple_lines(self):
        logical_lines = extract_logical_lines(["def test():", "    return 'Test'"])

        self.assertEqual(logical_lines, ["def test():", "    return 'Test'"])

    def test_that_multiple_multiline_logical_lines_should_return_multiple_lines(self):
        logical_lines = extract_logical_lines(["def test(", "    arg):", "    pass"])

        self.assertEqual(logical_lines, ["def test(arg):", "    pass"])

    def test_that_multiple_logical_lines_with_semicolons_and_backslashes_should_return_multiple_lines(
        self,
    ):
        logical_lines = extract_logical_lines(
            [
                "x = 5; y = 10; z = 15;",
                "long_string = 'This is a very long string that' \\",
                "              'continues on the next line'",
                "def complex_function(a,",
                "                    b,",
                "                    c):",
                "    return (a+",
                "            b+",
                "            c)",
                "tricky_string = 'This is a tricky string with a backslash \\'",
            ]
        )

        logical_lines_expected = [
            "x = 5",
            "y = 10",
            "z = 15",
            "long_string = 'This is a very long string that continues on the next line'",
            "def complex_function(a,b,c):",
            "    return (a+b+c)",
            "tricky_string = 'This is a tricky string with a backslash \\'",
        ]

        self.assertEqual(len(logical_lines), len(logical_lines_expected))


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

        self.assertEqual(project_logical_lines_count, 18)

    def test_that_a_project_with_code_and_comments_should_count_the_logical_lines(
        self,
    ):
        project_logical_lines_count = count_logical_lines_from_project(
            "tests/assets/documented_python_project"
        )

        self.assertEqual(project_logical_lines_count, 18)
