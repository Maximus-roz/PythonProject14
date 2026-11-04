import json

import pytest

from src.products import Category
from src.utils import load_categories_from_json


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сброс счётчиков класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def json_file(tmp_path):
    """Создаёт временный JSON-файл с тестовыми данными."""
    data = [
        {
            "name": "Смартфоны",
            "description": "Мобильные телефоны",
            "products": [
                {
                    "name": "iPhone 15",
                    "description": "Смартфон Apple",
                    "price": 99999.99,
                    "quantity": 10,
                },
                {
                    "name": "Samsung Galaxy S24",
                    "description": "Смартфон Samsung",
                    "price": 79999.99,
                    "quantity": 5,
                },
            ],
        },
        {
            "name": "Ноутбуки",
            "description": "Портативные компьютеры",
            "products": [
                {
                    "name": "MacBook Pro",
                    "description": "Ноутбук Apple",
                    "price": 199999.99,
                    "quantity": 3,
                }
            ],
        },
    ]

    file_path = tmp_path / "products.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    return str(file_path)


def test_load_categories_returns_list(json_file):
    """Функция возвращает список объектов Category."""
    categories = load_categories_from_json(json_file)

    assert isinstance(categories, list)
    assert len(categories) == 2
    assert all(isinstance(c, Category) for c in categories)


def test_load_categories_content(json_file):
    """Проверяет корректность загруженных данных."""
    categories = load_categories_from_json(json_file)

    smartphones = categories[0]
    assert smartphones.name == "Смартфоны"
    assert smartphones.description == "Мобильные телефоны"
    # products_list — это список товаров, поэтому len() даёт количество товаров
    assert len(smartphones.products_list) == 2

    iphone = smartphones.products_list[0]
    assert iphone.name == "iPhone 15"
    assert iphone.description == "Смартфон Apple"
    assert iphone.price == 99999.99
    assert iphone.quantity == 10

    samsung = smartphones.products_list[1]
    assert samsung.name == "Samsung Galaxy S24"
    assert samsung.price == 79999.99
    assert samsung.quantity == 5

    laptops = categories[1]
    assert laptops.name == "Ноутбуки"
    assert laptops.description == "Портативные компьютеры"
    assert len(laptops.products_list) == 1

    macbook = laptops.products_list[0]
    assert macbook.name == "MacBook Pro"
    assert macbook.price == 199999.99
    assert macbook.quantity == 3


def test_load_categories_products_is_string(json_file):
    """Свойство products возвращает строку со списком товаров."""
    categories = load_categories_from_json(json_file)

    smartphones = categories[0]
    assert isinstance(smartphones.products, str)
    assert "iPhone 15" in smartphones.products
    assert "Samsung Galaxy S24" in smartphones.products
    # две строки товаров + завершающие \n
    assert smartphones.products.count("\n") == 2


def test_load_categories_updates_counters(json_file):
    """Счётчики класса обновляются при загрузке."""
    load_categories_from_json(json_file)

    assert Category.category_count == 2
    assert Category.product_count == 3


def test_load_categories_empty_products(tmp_path):
    """Категория без товаров загружается корректно."""
    data = [{"name": "Пустая", "description": "Без товаров", "products": []}]
    file_path = tmp_path / "empty.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    categories = load_categories_from_json(str(file_path))

    assert len(categories) == 1
    assert categories[0].name == "Пустая"
    assert categories[0].products_list == []
    assert categories[0].products == ""
    assert Category.product_count == 0
    assert Category.category_count == 1


def test_load_categories_file_not_found():
    """Для несуществующего файла возникает FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_categories_from_json("nonexistent.json")
