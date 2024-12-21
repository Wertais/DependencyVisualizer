import argparse
import subprocess
import os

def get_dependencies(package_name):
    """
    Получает список зависимостей для указанного пакета.
    """
    result = subprocess.run(
        ['pip', 'show', package_name],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise ValueError(f"Пакет '{package_name}' не найден.")
    
    dependencies = []
    for line in result.stdout.splitlines():
        if line.startswith("Requires"):
            dependencies = line.split(":")[1].strip().split(", ")
            break
    return dependencies if dependencies[0] else []

def build_graph(package_name, output_path):
    """
    Создаёт граф зависимостей в формате .dot и преобразует его в .png.
    """
    dependencies = get_dependencies(package_name)

    # Создаём граф в формате .dot
    graph_lines = ["digraph G {"]
    for dep in dependencies:
        graph_lines.append(f'    "{package_name}" -> "{dep}";')
    graph_lines.append("}")

    # Сохраняем граф
    dot_file = output_path.replace(".png", ".dot")
    print(f"Путь для сохранения .dot файла: {dot_file}")
    print(f"Путь для сохранения .png файла: {output_path}")
    print("Содержимое .dot файла:")
    print("\n".join(graph_lines))

    try:
        with open(dot_file, "w") as f:
            f.write("\n".join(graph_lines))
        print(f".dot файл успешно создан: {dot_file}")
    except Exception as e:
        print(f"Ошибка при создании .dot файла: {e}")
        return

    # Конвертируем .dot в .png с помощью Graphviz
    command = f"dot -Tpng {dot_file} -o {output_path}"
    print(f"Выполнение команды Graphviz: {command}")
    result = os.system(command)
    if result != 0:
        print("Ошибка при выполнении команды Graphviz.")
    else:
        print(f"Граф зависимостей сохранён в {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Визуализация графа зависимостей.")
    parser.add_argument("--package", required=True, help="Имя Python-пакета.")
    parser.add_argument("--output", required=True, help="Путь к выходному .png файлу.")
    args = parser.parse_args()

    try:
        build_graph(args.package, args.output)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
