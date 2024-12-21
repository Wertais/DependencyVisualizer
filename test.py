from main import get_dependencies

def test_get_dependencies():
    deps = get_dependencies("pytest")
    assert "pluggy" in deps  # Проверка зависимости pytest
