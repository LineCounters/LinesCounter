from CodeFile import CodeFile

# path to the file for which the logical and physical line counts will be calculated
file_path = "my_file.py"
file = CodeFile(file_path)

print(file.__str__())
