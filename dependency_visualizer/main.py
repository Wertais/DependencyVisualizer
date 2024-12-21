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

def build_mermaid_graph(package_name, output_path):
    """
    Создаёт граф зависимостей в формате Mermaid и сохраняет его как PNG.
    """
    dependencies = get_dependencies(package_name)

    # Создаём граф в формате Mermaid
    graph_lines = ["graph TD"]
    for dep in dependencies:
        graph_lines.append(f'    {package_name} --> {dep}')

    # Сохраняем Mermaid диаграмму
    mmd_file = output_path.replace(".png", ".mmd")
    print(f"Путь для сохранения .mmd файла: {mmd_file}")
    print(f"Путь для сохранения .png файла: {output_path}")
    print("Содержимое .mmd файла:")
    print("\n".join(graph_lines))

    try:
        with open(mmd_file, "w") as f:
            f.write("\n".join(graph_lines))
        print(f".mmd файл успешно создан: {mmd_file}")
    except Exception as e:
        print(f"Ошибка при создании .mmd файла: {e}")
        return

    # Конвертируем .mmd в .png с помощью Mermaid CLI
    command = f"mmdc -i {mmd_file} -o {output_path}"
    print(f"Выполнение команды Mermaid CLI: {command}")
    result = os.system(command)
    if result != 0:
        print("Ошибка при выполнении команды Mermaid CLI.")
    else:
        print(f"Граф зависимостей сохранён в {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Визуализация графа зависимостей с помощью Mermaid.")
    parser.add_argument("--package", required=True, help="Имя Python-пакета.")
    parser.add_argument("--output", required=True, help="Путь к выходному .png файлу.")
    args = parser.parse_args()

    try:
        build_mermaid_graph(args.package, args.output)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
