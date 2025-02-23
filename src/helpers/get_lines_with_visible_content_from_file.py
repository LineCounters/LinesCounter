def get_lines_with_visible_content_from_file(filepath: str) -> list[str]:
    lines_with_visible_content = []

    with open(filepath, encoding="utf-8") as file:
        for line in file:
            if line.strip() != "":
                lines_with_visible_content.append(line)

    return lines_with_visible_content
