import re
from CodeLine import CodeLine

class LineBuilder:

    _raw_lines : list[str]
    _built_lines: list[CodeLine]

    def __init__(self, raw_lines: list[str]):
        self._raw_lines:list[str] = raw_lines
        self._built_lines:list[CodeLine] = self._build_lines()

    def _build_lines(self) -> list[CodeLine]:
        result: list[CodeLine] = []
        i: int = 0
        while i < len(self._raw_lines):
            line: str = self._raw_lines[i]
            stripped: str = line.strip()

            if self._is_nothing(stripped) or self._is_single_comment(stripped):
                pass
            elif self._is_multiline_comment(stripped):
                i = self._skip_comment(i)
            elif self._is_method_signature(stripped):
                result.append(CodeLine("method signature",1, 1))
            elif self._is_conditional(stripped):
                result.append(CodeLine("Conditional",1, 1))
            elif self._is_loop(stripped):
                result.append(CodeLine("Loop",1, 1))
            elif self._is_try_except(stripped):
                result.append(CodeLine("try_except",1, 1))
            elif self._is_import_line(stripped):
                result.append(CodeLine("import",1, 1))
            elif self._is_with_statement(stripped):
                result.append(CodeLine("with",1, 1))
            elif self._is_class(stripped):
                result.append(CodeLine("class", 1, 1))
            elif self._is_variable(stripped) or self._is_self_attribute(stripped):
                    logical_count = stripped.count(";") + 1 
                    result.append(CodeLine("variable", 1, logical_count))
            elif self._is_control_statement(stripped):
                result.append(CodeLine("ControlStatement", 1, 1))
            else:
                result.append(CodeLine("SomethingElse", 1, 0))
            i += 1
        return result
    

    def _is_with_statement(self,stripped:str)->bool:
        return stripped.startswith("with")


    def _is_try_except(self,stripped:str):
        return stripped.startswith("try") or stripped.startswith("except") or stripped.startswith("finally") or stripped.startswith("raise") 

    def _is_loop(self,stripped:str) -> bool:
        return stripped.startswith("for") or stripped.startswith("while")
    
    def _is_conditional(self,stripped : str) -> bool:
        return stripped.startswith("if") or stripped.startswith("elif") or stripped.startswith("else") or stripped.startswith("assert") 

    def _is_import_line(self, stripped: str) -> bool:
        starts_with_import: bool = stripped.startswith("import")
        starts_with_from: bool = stripped.startswith("from")
        return starts_with_import or starts_with_from

    def _is_class(self, stripped: str) -> bool:
        return stripped.startswith("class")

    def _is_method_signature(self, stripped: str) -> bool:
        return stripped.startswith("def ")
    
    def _is_control_statement(self, stripped: str) -> bool:
        return stripped.startswith("return") or stripped.startswith("break") or stripped.startswith("continue")

    def _is_variable(self, stripped: str) -> bool:
        pattern: re.Pattern = r'^[a-zA-Z_]\w*\s*=\s*[^=][^;]*?(;[a-zA-Z_]\w*\s*=\s*[^=][^;]*?)*$'
        return bool(re.match(pattern, stripped))
        
    def _is_self_attribute(self, stripped: str) -> bool:
        if stripped.startswith("self."):
            if "=" in stripped:
                if "(" not in stripped.split("=")[0]: 
                    return True
            elif "(" not in stripped:
                return True
        return False


    def _is_nothing(self,stripped:str):
        return stripped == ""

    def _is_single_comment(self, stripped : str):
        return  stripped.startswith("#")
    
    def _is_multiline_comment(self,stripped:str):
        return stripped.startswith('"""')

    def is_indented(self,line: str) -> bool:
        return bool(re.match(r'^\s+', line))
    
    def _get_indentation(self, line: str) -> int:
        return len(line) - len(line.lstrip())


    def _skip_comment(self,i):
        return self._count_physical_lines('"""',i) - 1 + i
    
    def _skip_method(self,startIndex : int):
        j = startIndex
        while j < len(self._raw_lines):
            _line: str = self._raw_lines[j].strip()
            if (self._is_class(_line) or self._is_method_signature()):
                break
            j += 1
        return j - startIndex + 1
    
    def _count_physical_lines(self,endChar : str, startIndex : int = 0):
        j = startIndex
        open_par = 0
        while j < len(self._raw_lines):
            _line: str = self._raw_lines[j].strip()
            if(endChar == ")"):
                open_par += _line.count("(")
                open_par -= _line.count(")")
            elif(endChar == '"""'):
                open_par += _line.count('"""')

            if (open_par % 2 == 0 and _line.endswith(endChar)):
                break
            j += 1
        return j - startIndex + 1
    
    def get_built_lines(self) -> list[CodeLine]:
        return self._built_lines
