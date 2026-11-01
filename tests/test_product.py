import pytest

from src.products import Product, Category, CategoryIterator

# ============================================================
#  ФИКСТУРЫ
# ============================================================


@pytest.fixture
def product1():
    return Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )


@pytest.fixture
def product2():
    return Product("Iphone 15", "512GB, Gray space", 210000.0, 8)


@pytest.fixture
def product3():
    return Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)


@pytest.fixture
def category1(product1, product2, product3):
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций",
        [product1, product2, product3],
    )


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасываем счётчики класса перед каждым тестом, чтобы тесты не влияли друг на друга."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


# ============================================================
#  ЗАДАНИЕ 1. __str__ для Product
# ============================================================


class TestProductStr:
    def test_product_str_format(self):
        p = Product("Товар", "Описание", 80.0, 15)
        assert str(p) == "Товар, 80.0 руб. Остаток: 15 шт."

    def test_product_str_int_price(self):
        p = Product("Товар", "Описание", 80, 15)
        assert str(p) == "Товар, 80 руб. Остаток: 15 шт."

    def test_product_str_zero_quantity(self):
        p = Product("Товар", "Описание", 100.0, 0)
        assert str(p) == "Товар, 100.0 руб. Остаток: 0 шт."

    def test_product_str_contains_rub_and_sht(self):
        p = Product("X", "d", 1.0, 1)
        text = str(p)
        assert "руб." in text
        assert "шт." in text
        assert "Остаток:" in text


# ============================================================
#  ЗАДАНИЕ 1. __str__ для Category
# ============================================================


class TestCategoryStr:
    def test_category_str_sums_quantity(self, category1):
        # 5 + 8 + 14 = 27
        assert str(category1) == "Смартфоны, количество продуктов: 27 шт."

    def test_category_str_empty(self):
        c = Category("Пустая", "Описание", [])
        assert str(c) == "Пустая, количество продуктов: 0 шт."

    def test_category_str_does_not_use_global_counter(self):
        """Строка категории должна зависеть от её собственных товаров,
        а не от общего счётчика класса."""
        Category("Другая", "d", [Product("A", "", 10.0, 100)])
        c = Category("Маленькая", "d", [Product("B", "", 10.0, 2)])
        assert str(c) == "Маленькая, количество продуктов: 2 шт."


# ============================================================
#  Геттер products у Category (оптимизирован через str(Product))
# ============================================================


class TestCategoryProductsProperty:
    def test_products_property_returns_string(self, category1):
        assert isinstance(category1.products, str)

    def test_products_property_contains_each_product_str(
        self, category1, product1, product2, product3
    ):
        text = category1.products
        assert str(product1) in text
        assert str(product2) in text
        assert str(product3) in text

    def test_products_property_empty(self):
        c = Category("Пустая", "d", [])
        assert c.products == ""


# ============================================================
#  ЗАДАНИЕ 2. __add__ для Product
# ============================================================


class TestProductAdd:
    def test_add_example_from_task(self):
        """Пример из ТЗ: a (100×10) + b (200×2) = 1400."""
        a = Product("A", "", 100.0, 10)
        b = Product("B", "", 200.0, 2)
        assert a + b == 1400

    def test_add_returns_number(self):
        a = Product("A", "", 100.0, 1)
        b = Product("B", "", 200.0, 1)
        result = a + b
        assert isinstance(result, (int, float))

    def test_add_fixtures(self, product1, product2, product3):
        assert product1 + product2 == 180000.0 * 5 + 210000.0 * 8
        assert product1 + product3 == 180000.0 * 5 + 31000.0 * 14
        assert product2 + product3 == 210000.0 * 8 + 31000.0 * 14

    def test_add_does_not_mutate_left_operand(self):
        a = Product("A", "", 100.0, 10)
        b = Product("B", "", 200.0, 2)
        _ = a + b
        assert a.price == 100.0
        assert a.quantity == 10
        assert a.name == "A"

    def test_add_does_not_mutate_right_operand(self):
        a = Product("A", "", 100.0, 10)
        b = Product("B", "", 200.0, 2)
        _ = a + b
        assert b.price == 200.0
        assert b.quantity == 2
        assert b.name == "B"

    def test_add_is_commutative_in_value(self):
        a = Product("A", "", 100.0, 10)
        b = Product("B", "", 200.0, 2)
        assert a + b == b + a

    def test_add_with_zero_quantity(self):
        a = Product("A", "", 100.0, 10)
        b = Product("B", "", 200.0, 0)
        assert a + b == 1000

    def test_add_with_non_product_raises_type_error(self):
        a = Product("A", "", 100.0, 10)
        with pytest.raises(TypeError):
            _ = a + 5

    def test_add_with_string_raises_type_error(self):
        a = Product("A", "", 100.0, 10)
        with pytest.raises(TypeError):
            _ = a + "текст"


# ============================================================
#  price setter
# ============================================================


class TestPriceSetter:
    def test_set_valid_price(self):
        p = Product("A", "", 100.0, 1)
        p.price = 150.0
        assert p.price == 150.0

    def test_set_zero_price_raises(self):
        p = Product("A", "", 100.0, 1)
        with pytest.raises(ValueError):
            p.price = 0
        assert p.price == 100.0

    def test_set_negative_price_raises(self):
        p = Product("A", "", 100.0, 1)
        with pytest.raises(ValueError):
            p.price = -50
        assert p.price == 100.0

    def test_create_with_zero_price_raises(self):
        with pytest.raises(ValueError):
            Product("A", "", 0, 1)

    def test_create_with_negative_price_raises(self):
        with pytest.raises(ValueError):
            Product("A", "", -10, 1)


# ============================================================
#  new_product (classmethod)
# ============================================================


class TestNewProduct:
    def test_new_product_from_dict(self):
        data = {"name": "A", "description": "d", "price": 50.0, "quantity": 3}
        p = Product.new_product(data)
        assert isinstance(p, Product)
        assert p.name == "A"
        assert p.description == "d"
        assert p.price == 50.0
        assert p.quantity == 3

    def test_new_product_invalid_price(self):
        data = {"name": "A", "description": "d", "price": 0, "quantity": 3}
        with pytest.raises(ValueError):
            Product.new_product(data)


# ============================================================
#  Category: счётчики и add_product
# ============================================================


class TestCategory:
    def test_category_count_increments(self):
        assert Category.category_count == 0
        Category("A", "d", [])
        assert Category.category_count == 1
        Category("B", "d", [])
        assert Category.category_count == 2

    def test_product_count_on_init(self, product1, product2, product3):
        Category("C", "d", [product1, product2, product3])
        assert Category.product_count == 3

    def test_product_count_accumulates(self, product1, product2):
        Category("C1", "d", [product1])
        Category("C2", "d", [product2])
        assert Category.product_count == 2

    def test_add_product_increments_count(self):
        c = Category("C", "d", [])
        assert Category.product_count == 0
        c.add_product(Product("A", "", 100.0, 1))
        assert Category.product_count == 1

    def test_add_product_appears_in_products(self, category1):
        new_p = Product("Новый", "d", 100.0, 1)
        category1.add_product(new_p)
        assert str(new_p) in category1.products

    def test_add_product_wrong_type_raises(self):
        c = Category("C", "d", [])
        with pytest.raises(TypeError):
            c.add_product("не товар")

    def test_init_does_not_mutate_source_list(self):
        items = []
        c = Category("C", "d", items)
        c.add_product(Product("A", "", 100.0, 1))
        assert items == []  # исходный список не изменился


# ============================================================
#  ДОП. ЗАДАНИЕ. CategoryIterator
# ============================================================


class TestCategoryIterator:
    def test_iter_returns_all_products(self, category1, product1, product2, product3):
        items = list(CategoryIterator(category1))
        assert items == [product1, product2, product3]

    def test_for_loop_iterates(self, category1):
        names = [p.name for p in CategoryIterator(category1)]
        assert names == [
            "Samsung Galaxy S23 Ultra",
            "Iphone 15",
            "Xiaomi Redmi Note 11",
        ]

    def test_empty_category(self):
        c = Category("Пустая", "d", [])
        assert list(CategoryIterator(c)) == []

    def test_iterator_returns_same_objects(self, category1):
        for p in CategoryIterator(category1):
            assert isinstance(p, Product)

    def test_iterator_can_be_created_twice_independently(self, category1):
        it1 = CategoryIterator(category1)
        it2 = CategoryIterator(category1)
        first1 = next(it1)
        first2 = next(it2)
        assert first1 is first2  # оба начинают с первого товара
        assert list(it1) == list(it2)  # и обходят одинаково

    def test_iterator_next_raises_stop_iteration(self, category1):
        it = CategoryIterator(category1)
        for _ in range(3):
            next(it)
        with pytest.raises(StopIteration):
            next(it)
