from CodeFile import CodeFile

# path al archivo al que se le calculará la cantidad de líneas lógicas y físicas
file_path = "my_file2.py"
mi_archivo = CodeFile(file_path)

print(mi_archivo.__str__())
