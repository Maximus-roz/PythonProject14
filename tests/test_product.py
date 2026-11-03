import pytest

from src.base_product import BaseProduct
from src.products import Product, Category, Smartphone, LawnGrass, CategoryIterator


def test_base_product_is_abstract():
    with pytest.raises(TypeError):
        BaseProduct("name", "desc", 100, 1)


def test_product_is_subclass_of_base():
    assert issubclass(Product, BaseProduct)
    assert issubclass(Smartphone, Product)
    assert issubclass(LawnGrass, Product)


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


def test_product_add_same_type():
    p1 = Product("A", "d", 100.0, 2)
    p2 = Product("B", "d", 200.0, 3)
    assert p1 + p2 == 100 * 2 + 200 * 3


def test_product_add_different_types_raises():
    p = Product("A", "d", 100.0, 2)
    s = Smartphone("S", "d", 100.0, 1, 3.5, "M", 128, "black")
    with pytest.raises(TypeError):
        _ = p + s


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


def test_category_counters():
    Category.category_count = 0
    Category.product_count = 0
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