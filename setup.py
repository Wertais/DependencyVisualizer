from setuptools import setup, find_packages

setup(
    name="DependencyVisualizer",  # Имя вашего проекта
    version="1.0.0",  # Версия
    packages=find_packages(),  # Автоматически находить пакеты (включает подпапки с __init__.py)
    install_requires=[
        "graphviz",  # Основные зависимости
        "pytest",
    ],
    entry_points={
        'console_scripts': [
            'dependency-visualizer=dependency_visualizer.main:main',  # Указываем точку входа для консольной команды
        ],
    },
    description="Command-line tool for visualizing Python package dependencies",  # Краткое описание
    author="Ваше Имя",  # Ваше имя
    author_email="ваш_email@example.com",  # Ваш email (опционально)
    url="https://github.com/Wertais/DependencyVisualizer",  # Ссылка на репозиторий
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
