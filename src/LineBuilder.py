import re
from typing import Tuple, List, Optional
from CodeLine import CodeLine

class LineBuilder:
    _raw_lines: List[str]
    _built_lines: List[CodeLine]
    _in_docstring: bool
    _doc_delim: Optional[str]

    def __init__(self, raw_lines: List[str]) -> None:
        self._raw_lines = raw_lines
        # Initialize internal docstring state BEFORE building lines
        self._in_docstring = False
        self._doc_delim = None
        self._built_lines = self._build_lines()

    def get_built_lines(self) -> List[CodeLine]:
        return self._built_lines

    def _build_lines(self) -> List[CodeLine]:
        built_lines: List[CodeLine] = []
        index = 0
        while index < len(self._raw_lines):
            block, index = self._collect_next_logical_block(index)
            if block:
                built_lines.append(self._create_code_line_from_block(block))
        return built_lines

    def _collect_next_logical_block(self, start_index: int) -> Tuple[List[str], int]:
        block: List[str] = []
        index = start_index

        while index < len(self._raw_lines):
            current_line = self._raw_lines[index]
            stripped_line = current_line.strip()

            if self._should_skip_line(stripped_line):
                index += 1
                continue

            if self._should_skip_due_to_docstring(stripped_line):
                index += 1
                continue

            block.append(current_line)
            if self._is_explicit_continuation(current_line) or not self._is_block_complete(block):
                index += 1
                continue

            index += 1
            break

        return block, index

    def _create_code_line_from_block(self, block_lines: List[str]) -> CodeLine:
        block_text = " ".join(block_lines)
        physical_count = len(block_lines)
        logical_count = block_text.count(";") + 1
        statement_type = self._determine_statement_type(block_text.strip())
        return CodeLine(statement_type, physical_count, logical_count)

    def _should_skip_line(self, stripped: str) -> bool:
        is_blank = not stripped
        is_comment = self._is_comment(stripped)
        is_annotation = stripped.startswith("@")
        return is_blank or is_comment or is_annotation

    def _should_skip_due_to_docstring(self, line: str) -> bool:
        # If not inside a docstring and the line signals a docstring start
        if not self._in_docstring and self._line_starts_docstring(line):
            if self._line_is_single_line_docstring(line):
                return True
            else:
                self._in_docstring = True
                self._doc_delim = line[:3]
                return True

        # If inside a docstring, always skip the line
        if self._in_docstring:
            if self._line_ends_docstring(line):
                self._in_docstring = False
                self._doc_delim = None
            return True

        return False

    def _line_starts_docstring(self, line: str) -> bool:
        return line.startswith('"""') or line.startswith("'''")

    def _line_is_single_line_docstring(self, line: str) -> bool:
        has_start_and_end = line.endswith('"""') or line.endswith("'''")
        contains_content = len(line) > 3
        return has_start_and_end and contains_content

    def _line_ends_docstring(self, line: str) -> bool:
        return self._doc_delim is not None and self._doc_delim in line

    def _is_explicit_continuation(self, line: str) -> bool:
        returns_backslash = line.rstrip().endswith("\\")
        return returns_backslash

    def _is_block_complete(self, block_lines: List[str]) -> bool:
        block_text = " ".join(block_lines)
        balance = 0
        for char in block_text:
            is_opening = char in "([{"
            is_closing = char in ")]}"
            if is_opening:
                balance += 1
            elif is_closing:
                balance -= 1
        return balance == 0

    def _determine_statement_type(self, line: str) -> str:
        if self._is_method_signature(line):
            return "method signature"
        elif self._is_conditional(line):
            return "Conditional"
        elif self._is_loop(line):
            return "Loop"
        elif self._is_try_except(line):
            return "try_except"
        elif self._is_import_line(line):
            return "import"
        elif self._is_with_statement(line):
            return "with"
        elif self._is_class(line):
            return "class"
        elif self._is_variable(line) or self._is_self_attribute(line):
            return "variable"
        elif self._is_control_statement(line):
            return "ControlStatement"
        else:
            return "SomethingElse"

    def _is_comment(self, line: str) -> bool:
        is_comment = line.startswith("#")
        return is_comment

    def _is_with_statement(self, line: str) -> bool:
        is_with = line.startswith("with")
        return is_with

    def _is_try_except(self, line: str) -> bool:
        is_try = line.startswith("try")
        is_except = line.startswith("except")
        is_finally = line.startswith("finally")
        is_raise = line.startswith("raise")
        return is_try or is_except or is_finally or is_raise

    def _is_loop(self, line: str) -> bool:
        is_for = line.startswith("for")
        is_while = line.startswith("while")
        return is_for or is_while

    def _is_conditional(self, line: str) -> bool:
        is_if = line.startswith("if")
        is_elif = line.startswith("elif")
        is_else = line.startswith("else")
        is_assert = line.startswith("assert")
        return is_if or is_elif or is_else or is_assert

    def _is_import_line(self, line: str) -> bool:
        is_import = line.startswith("import")
        is_from = line.startswith("from")
        return is_import or is_from

    def _is_class(self, line: str) -> bool:
        is_class = line.startswith("class")
        return is_class

    def _is_method_signature(self, line: str) -> bool:
        is_def = line.startswith("def ")
        return is_def

    def _is_control_statement(self, line: str) -> bool:
        is_return = line.startswith("return")
        is_break = line.startswith("break")
        is_continue = line.startswith("continue")
        return is_return or is_break or is_continue

    def _is_variable(self, line: str) -> bool:
        simple_variable_assignment_pattern = (
            r'^[a-zA-Z_]\w*\s*=\s*[^=][^;]*?(;[a-zA-Z_]\w*\s*=\s*[^=][^;]*?)*$'
        )
        compiled_pattern = re.compile(simple_variable_assignment_pattern)
        matches_pattern = bool(compiled_pattern.match(line))
        return matches_pattern

    def _is_self_attribute(self, line: str) -> bool:
        is_self_start = line.startswith("self.")
        if is_self_start:
            has_assignment = "=" in line
            no_function_call = "(" not in line.split("=")[0]
            if has_assignment and no_function_call:
                return True
            if not has_assignment and "(" not in line:
                return True
        return False
