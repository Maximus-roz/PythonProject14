import pytest

from src.base_product import BaseProduct
from src.print_mixin import PrintMixin
from src.products import (
    Product,
    Category,
    Smartphone,
    LawnGrass,
    CategoryIterator,
)


# ---------------------------------------------------------------------------
# BaseProduct / иерархия наследования
# ---------------------------------------------------------------------------

def test_base_product_is_abstract():
    """BaseProduct нельзя инстанцировать напрямую (есть абстрактный price)."""
    with pytest.raises(TypeError):
        BaseProduct("name", "desc", 100, 1)


def test_product_is_subclass_of_base():
    assert issubclass(Product, BaseProduct)
    assert issubclass(Smartphone, Product)
    assert issubclass(LawnGrass, Product)
    assert issubclass(Product, PrintMixin)


# ---------------------------------------------------------------------------
# Product: инициализация и валидация
# ---------------------------------------------------------------------------

def test_product_init_and_attributes():
    p = Product("Тест", "Описание", 100.0, 5)
    assert p.name == "Тест"
    assert p.description == "Описание"
    assert p.price == 100.0
    assert p.quantity == 5


def test_product_price_validation():
    with pytest.raises(ValueError):
        Product("Тест", "Описание", 0, 5)
    with pytest.raises(ValueError):
        Product("Тест", "Описание", -10, 5)


def test_product_quantity_validation():
    """Нулевое/отрицательное количество должно приводить к ValueError."""
    with pytest.raises(ValueError):
        Product("Тест", "Описание", 100.0, 0)
    with pytest.raises(ValueError):
        Product("Тест", "Описание", 100.0, -1)


def test_product_price_setter():
    p = Product("A", "d", 100.0, 1)
    p.price = 200.0
    assert p.price == 200.0
    with pytest.raises(ValueError):
        p.price = 0
    with pytest.raises(ValueError):
        p.price = -5


def test_new_product_classmethod():
    data = {"name": "N", "description": "D", "price": 50.0, "quantity": 3}
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.name == "N"
    assert p.price == 50.0
    assert p.quantity == 3


# ---------------------------------------------------------------------------
# Product: __add__ (из BaseProduct)
# ---------------------------------------------------------------------------

def test_product_add_same_type():
    p1 = Product("A", "d", 100.0, 2)
    p2 = Product("B", "d", 200.0, 3)
    assert p1 + p2 == 100 * 2 + 200 * 3


def test_product_add_different_types_raises():
    p = Product("A", "d", 100.0, 2)
    s = Smartphone("S", "d", 100.0, 1, 3.5, "M", 128, "black")
    with pytest.raises(TypeError):
        _ = p + s


def test_smartphone_add_same_type():
    s1 = Smartphone("S1", "d", 100.0, 1, 3.5, "M", 128, "black")
    s2 = Smartphone("S2", "d", 200.0, 2, 4.0, "N", 256, "white")
    assert s1 + s2 == 100 * 1 + 200 * 2


# ---------------------------------------------------------------------------
# PrintMixin
# ---------------------------------------------------------------------------

def test_print_mixin_prints_repr(capsys):
    Product("Продукт1", "Описание продукта", 1200.0, 10)
    captured = capsys.readouterr()
    assert "Product(" in captured.out
    assert "Продукт1" in captured.out
    assert "1200.0" in captured.out


def test_print_mixin_repr_format():
    p = Product("X", "Y", 100.0, 1)
    assert repr(p) == "Product('X', 'Y', 100.0, 1)"


def test_smartphone_print_mixin(capsys):
    Smartphone("S", "d", 100.0, 1, 3.5, "M", 128, "black")
    captured = capsys.readouterr()
    assert "Smartphone(" in captured.out


def test_lawn_grass_print_mixin(capsys):
    LawnGrass("G", "d", 10.0, 1, "RU", "7d", "green")
    captured = capsys.readouterr()
    assert "LawnGrass(" in captured.out


# ---------------------------------------------------------------------------
# Smartphone / LawnGrass: атрибуты
# ---------------------------------------------------------------------------

def test_smartphone_attributes():
    s = Smartphone("S", "d", 100.0, 1, 3.5, "M", 128, "black")
    assert s.efficiency == 3.5
    assert s.model == "M"
    assert s.memory == 128
    assert s.color == "black"
    # унаследованные
    assert s.name == "S"
    assert s.price == 100.0


def test_lawn_grass_attributes():
    g = LawnGrass("G", "d", 10.0, 2, "RU", "7d", "green")
    assert g.country == "RU"
    assert g.germination_period == "7d"
    assert g.color == "green"


# ---------------------------------------------------------------------------
# Category: счётчики, str, add_product
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_category_counters():
    """Счётчики класса Category — глобальные, их надо сбрасывать между тестами."""
    Category.category_count = 0
    Category.product_count = 0
    yield


def test_category_counters():
    p1 = Product("A", "d", 100.0, 1)
    p2 = Product("B", "d", 100.0, 2)
    Category("C1", "d", [p1, p2])
    Category("C2", "d", [p1])
    assert Category.category_count == 2
    assert Category.product_count == 3


def test_category_str():
    p1 = Product("A", "d", 100.0, 3)
    p2 = Product("B", "d", 100.0, 7)
    c = Category("Кат", "d", [p1, p2])
    assert str(c) == "Кат, количество продуктов: 10 шт."


def test_add_product_type_check():
    c = Category("C", "d", [])
    with pytest.raises(TypeError):
        c.add_product("not a product")


def test_add_product_increments_counter():
    c = Category("C", "d", [])
    assert Category.product_count == 0
    c.add_product(Product("A", "d", 100.0, 1))
    assert Category.product_count == 1
    assert len(c.products_list) == 1


def test_category_products_property():
    p1 = Product("A", "d", 100.0, 1)
    p2 = Product("B", "d", 200.0, 2)
    c = Category("C", "d", [p1, p2])
    text = c.products
    assert "A" in text
    assert "B" in text
    # Каждый товар на отдельной строке
    assert text.count("\n") == 2


# ---------------------------------------------------------------------------
# Category: итерация
# ---------------------------------------------------------------------------

def test_iterator():
    p1 = Product("A", "d", 100.0, 1)
    p2 = Product("B", "d", 100.0, 2)
    c = Category("C", "d", [p1, p2])
    it = CategoryIterator(c)
    assert list(it) == [p1, p2]


def test_category_iterable():
    p1 = Product("A", "d", 100.0, 1)
    c = Category("C", "d", [p1])
    assert list(c) == [p1]


def test_iterator_on_empty_category():
    c = Category("C", "d", [])
    assert list(c) == []


# ---------------------------------------------------------------------------
# Category: middle_price
# ---------------------------------------------------------------------------

def test_middle_price():
    p1 = Product("A", "d", 100.0, 1)
    p2 = Product("B", "d", 200.0, 1)
    p3 = Product("C", "d", 300.0, 1)
    c = Category("C", "d", [p1, p2, p3])
    assert c.middle_price() == 200.0


def test_middle_price_empty_category():
    """Пустая категория — возвращается 0 через обработку ZeroDivisionError."""
    c = Category("C", "d", [])
    assert c.middle_price() == 0


def test_middle_price_single_product():
    p = Product("A", "d", 150.0, 1)
    c = Category("C", "d", [p])
    assert c.middle_price() == 150.0


def test_middle_price_uses_price_not_total():
    """Средняя цена — по цене за единицу, не по полной стоимости склада."""
    p1 = Product("A", "d", 100.0, 10)  # на складе 1000
    p2 = Product("B", "d", 300.0, 1)   # на складе 300
    c = Category("C", "d", [p1, p2])
    assert c.middle_price() == 200.0  # (100 + 300) / 2


def test_middle_price_returns_zero_on_empty_category_explicitly():
    """Явно проверяем, что именно ветка try/except отдаёт 0."""
    c = Category("C", "d", [])
    result = c.middle_price()
    assert result == 0
    assert isinstance(result, int)