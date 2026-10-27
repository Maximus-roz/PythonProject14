import pytest

from src.products import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасывает счётчики класса перед каждым тестом, чтобы тесты не влияли друг на друга."""
    Category.category_count = 0
    Category.product_count = 0
    yield


def test_product_init():
    """Корректность инициализации объектов класса Product."""
    product = Product("iPhone", "Смартфон Apple", 99999.99, 10)

    assert product.name == "iPhone"
    assert product.description == "Смартфон Apple"
    assert product.price == 99999.99
    assert product.quantity == 10


def test_category_init():
    """Корректность инициализации объектов класса Category."""
    products = [
        Product("iPhone", "Смартфон", 99999.99, 10),
        Product("Samsung", "Смартфон", 79999.99, 5),
    ]
    category = Category("Смартфоны", "Мобильные телефоны", products)

    assert category.name == "Смартфоны"
    assert category.description == "Мобильные телефоны"
    assert category.products == products
    assert len(category.products) == 2


def test_category_count():
    """Подсчёт количества категорий."""
    assert Category.category_count == 0

    Category("Смартфоны", "Мобильные телефоны", [])
    assert Category.category_count == 1

    Category("Ноутбуки", "Портативные компьютеры", [])
    assert Category.category_count == 2

    # Проверка доступа через экземпляр
    category = Category("Планшеты", "Планшетные ПК", [])
    assert category.category_count == 3


def test_product_count():
    """Подсчёт количества продуктов."""
    assert Category.product_count == 0

    products_1 = [
        Product("iPhone", "Смартфон", 99999.99, 10),
        Product("Samsung", "Смартфон", 79999.99, 5),
    ]
    Category("Смартфоны", "Мобильные телефоны", products_1)
    assert Category.product_count == 2

    products_2 = [
        Product("MacBook", "Ноутбук", 199999.99, 3),
        Product("Lenovo", "Ноутбук", 89999.99, 7),
        Product("Asus", "Ноутбук", 99999.99, 4),
    ]
    Category("Ноутбуки", "Портативные компьютеры", products_2)
    assert Category.product_count == 5

    # Пустая категория не меняет счётчик товаров
    Category("Пустая", "Без товаров", [])
    assert Category.product_count == 5


def test_counters_shared_between_instances():
    """Счётчики доступны через любой экземпляр класса."""
    cat_1 = Category("A", "Описание A", [Product("p1", "d", 1.0, 1)])
    cat_2 = Category(
        "B",
        "Описание B",
        [
            Product("p2", "d", 2.0, 1),
            Product("p3", "d", 3.0, 1),
        ],
    )

    assert cat_1.category_count == cat_2.category_count == 2
    assert cat_1.product_count == cat_2.product_count == 3
