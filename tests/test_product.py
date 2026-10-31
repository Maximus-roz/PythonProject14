import pytest

from src.products import Product, Category





# ---------------------------------------------------------------------------
# Product: инициализация
# ---------------------------------------------------------------------------

class TestProductInit:
    def test_attributes_are_set(self):
        p = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
        assert p.name == "Iphone 15"
        assert p.description == "512GB, Gray space"
        assert p.price == 210000.0
        assert p.quantity == 8

    def test_price_is_private(self):
        p = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
        # напрямую по имени __price извне не достать
        with pytest.raises(AttributeError):
            _ = p.__price


# ---------------------------------------------------------------------------
# Product: класс-метод new_product
# ---------------------------------------------------------------------------

class TestProductNewProduct:
    def test_returns_product_instance(self):
        p = Product.new_product(
            {"name": "Samsung Galaxy S23 Ultra",
             "description": "256GB, Серый цвет, 200MP камера",
             "price": 180000.0,
             "quantity": 5}
        )
        assert isinstance(p, Product)

    def test_fields_from_dict(self):
        p = Product.new_product(
            {"name": "Xiaomi", "description": "1024GB, Синий",
             "price": 31000.0, "quantity": 14}
        )
        assert p.name == "Xiaomi"
        assert p.description == "1024GB, Синий"
        assert p.price == 31000.0
        assert p.quantity == 14

    def test_new_product_goes_through_price_setter(self, capsys):
        # некорректная цена в словаре -> сеттер печатает сообщение и не присваивает
        p = Product.new_product(
            {"name": "Bad", "description": "x", "price": -5, "quantity": 1}
        )
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out


# ---------------------------------------------------------------------------
# Product: сеттер цены
# ---------------------------------------------------------------------------

class TestProductPriceSetter:
    def test_positive_price_is_set(self):
        p = Product("A", "B", 100.0, 1)
        p.price = 800
        assert p.price == 800

    def test_zero_price_prints_and_keeps_old(self, capsys):
        p = Product("A", "B", 100.0, 1)
        p.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 100.0

    def test_negative_price_prints_and_keeps_old(self, capsys):
        p = Product("A", "B", 100.0, 1)
        p.price = -100
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 100.0


# ---------------------------------------------------------------------------
# Category: инициализация и счётчики
# ---------------------------------------------------------------------------

@pytest.fixture
def products():
    return [
        Product("Samsung Galaxy S23 Ultra", "256GB", 180000.0, 5),
        Product("Iphone 15", "512GB", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB", 31000.0, 14),
    ]


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасываем счётчики класса перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


class TestCategoryInit:
    def test_attributes(self, products):
        c = Category("Смартфоны", "Описание", products)
        assert c.name == "Смартфоны"
        assert c.description == "Описание"

    def test_products_is_private(self, products):
        c = Category("Смартфоны", "Описание", products)
        with pytest.raises(AttributeError):
            _ = c.__products

    def test_category_count_increments(self, products):
        assert Category.category_count == 0
        Category("A", "d", products)
        Category("B", "d", products)
        assert Category.category_count == 2

    def test_product_count_from_initial_products(self, products):
        Category("A", "d", products)
        assert Category.product_count == 3


# ---------------------------------------------------------------------------
# Category: add_product
# ---------------------------------------------------------------------------

class TestCategoryAddProduct:
    def test_add_product_appends(self, products):
        c = Category("Смартфоны", "Описание", products)
        new_p = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
        c.add_product(new_p)

        # проверяем через публичный геттер
        assert "55\" QLED 4K" in c.products

    def test_add_product_increments_product_count(self, products):
        c = Category("Смартфоны", "Описание", products)
        new_p = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
        c.add_product(new_p)
        assert Category.product_count == 4

    def test_add_product_to_empty_category(self):
        c = Category("Пустая", "Описание", [])
        p = Product("A", "B", 10.0, 1)
        c.add_product(p)
        assert Category.product_count == 1
        assert "A, 10.0 руб. Остаток: 1 шт." in c.products


# ---------------------------------------------------------------------------
# Category: геттер products
# ---------------------------------------------------------------------------

class TestCategoryProductsGetter:
    def test_format(self):
        p = Product("Товар", "Описание", 80.0, 15)
        c = Category("Кат", "Описание", [p])
        assert c.products == "Товар, 80.0 руб. Остаток: 15 шт.\n"

    def test_multiple_products_each_on_own_line(self, products):
        c = Category("Смартфоны", "Описание", products)
        lines = [line for line in c.products.splitlines() if line]
        assert len(lines) == 3
        assert lines[0] == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
        assert lines[1] == "Iphone 15, 210000.0 руб. Остаток: 8 шт."
        assert lines[2] == "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт."

    def test_empty_category_returns_empty_string(self):
        c = Category("Пустая", "Описание", [])
        assert c.products == ""

    def test_products_does_not_expose_list(self, products):
        c = Category("Смартфоны", "Описание", products)
        # геттер возвращает строку, а не список
        assert isinstance(c.products, str)