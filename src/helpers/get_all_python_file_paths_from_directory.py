import os


def get_all_python_file_paths_from_directory(project_path: str) -> list[str]:
    python_files = []

    for dirpath, _, filenames in os.walk(project_path):
        for filename in filenames:
            if filename.endswith(".py"):
                full_path = os.path.join(dirpath, filename)
                python_files.append(full_path)

    return python_files
