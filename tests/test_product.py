import pytest

from src.products import Product, Category
from src.smartphone_product import Smartphone
from src.lawngrass_product import LawnGrass

# ---------- Фикстуры ----------


@pytest.fixture
def smartphone1():
    return Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )


@pytest.fixture
def smartphone2():
    return Smartphone(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
        98.2,
        "15",
        512,
        "Gray space",
    )


@pytest.fixture
def grass1():
    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )


@pytest.fixture
def grass2():
    return LawnGrass(
        "Газонная трава 2",
        "Выносливая трава",
        450.0,
        15,
        "США",
        "5 дней",
        "Темно-зеленый",
    )


@pytest.fixture
def category_smartphones(smartphone1, smartphone2):
    return Category(
        "Смартфоны",
        "Высокотехнологичные смартфоны",
        [smartphone1, smartphone2],
    )


@pytest.fixture
def category_grass(grass1, grass2):
    return Category(
        "Газонная трава",
        "Различные виды газонной травы",
        [grass1, grass2],
    )


# ---------- Задание 1: наследование ----------


class TestInheritance:
    def test_smartphone_is_product(self, smartphone1):
        assert isinstance(smartphone1, Product)
        assert issubclass(Smartphone, Product)

    def test_lawn_grass_is_product(self, grass1):
        assert isinstance(grass1, Product)
        assert issubclass(LawnGrass, Product)

    def test_smartphone_extra_attributes(self, smartphone1):
        assert smartphone1.efficiency == 95.5
        assert smartphone1.model == "S23 Ultra"
        assert smartphone1.memory == 256
        assert smartphone1.color == "Серый"

    def test_lawn_grass_extra_attributes(self, grass1):
        assert grass1.country == "Россия"
        assert grass1.germination_period == "7 дней"
        assert grass1.color == "Зеленый"

    def test_product_base_attributes_still_work(self, smartphone1, grass1):
        assert smartphone1.name == "Samsung Galaxy S23 Ultra"
        assert smartphone1.price == 180000.0
        assert smartphone1.quantity == 5
        assert grass1.name == "Газонная трава"
        assert grass1.price == 500.0
        assert grass1.quantity == 20


# ---------- Задание 2: сложение ----------


class TestAddition:
    def test_add_same_class_smartphones(self, smartphone1, smartphone2):
        # 180000*5 + 210000*8 = 900000 + 1680000 = 2580000
        assert smartphone1 + smartphone2 == 2580000.0

    def test_add_same_class_grass(self, grass1, grass2):
        # 500*20 + 450*15 = 10000 + 6750 = 16750
        assert grass1 + grass2 == 16750.0

    def test_add_different_classes_raises(self, smartphone1, grass1):
        with pytest.raises(TypeError):
            smartphone1 + grass1

    def test_add_different_classes_raises_reverse(self, grass1, smartphone1):
        with pytest.raises(TypeError):
            grass1 + smartphone1

    def test_add_product_with_itself(self, smartphone1):
        assert smartphone1 + smartphone1 == 180000.0 * 5 * 2

    def test_add_with_non_product_raises(self, smartphone1):
        with pytest.raises(TypeError):
            smartphone1 + 5


# ---------- Задание 3: защита add_product ----------


class TestAddProduct:
    def test_add_smartphone(self, category_smartphones, smartphone1):
        new_phone = Smartphone(
            "Xiaomi Redmi Note 11",
            "1024GB, Синий",
            31000.0,
            14,
            90.3,
            "Note 11",
            1024,
            "Синий",
        )
        category_smartphones.add_product(new_phone)
        assert new_phone in category_smartphones.products_list

    def test_add_lawn_grass_to_category(self, category_grass, grass1):
        new_grass = LawnGrass(
            "Газонная трава 3",
            "Ещё одна трава",
            400.0,
            10,
            "Германия",
            "6 дней",
            "Салатовый",
        )
        category_grass.add_product(new_grass)
        assert new_grass in category_grass.products_list

    def test_add_base_product(self, category_smartphones):
        base = Product("Обычный товар", "Просто товар", 100.0, 1)
        category_smartphones.add_product(base)
        assert base in category_smartphones.products_list

    @pytest.mark.parametrize(
        "bad_value",
        [
            "Not a product",
            42,
            3.14,
            None,
            [],
            {},
            ("кортеж",),
            object(),
        ],
    )
    def test_add_non_product_raises(self, category_smartphones, bad_value):
        with pytest.raises(TypeError):
            category_smartphones.add_product(bad_value)

    def test_add_non_product_does_not_change_products(self, category_smartphones):
        before = list(category_smartphones.products_list)
        with pytest.raises(TypeError):
            category_smartphones.add_product("Not a product")
        assert category_smartphones.products_list == before

    def test_add_non_product_does_not_change_product_count(self, category_smartphones):
        count_before = Category.product_count
        with pytest.raises(TypeError):
            category_smartphones.add_product("Not a product")
        assert Category.product_count == count_before

    def test_add_non_product_does_not_change_category_count(self, category_smartphones):
        count_before = Category.category_count
        with pytest.raises(TypeError):
            category_smartphones.add_product("Not a product")
        assert Category.category_count == count_before

    def test_add_product_increments_product_count(
        self, category_smartphones, smartphone1
    ):
        new_phone = Smartphone(
            "Телефон",
            "Описание",
            1000.0,
            1,
            90.0,
            "M",
            64,
            "Черный",
        )
        count_before = Category.product_count
        category_smartphones.add_product(new_phone)
        assert Category.product_count == count_before + 1

    def test_add_product_subclass_works(self, category_smartphones):
        """Наследники Product должны добавляться без ошибок."""
        new_phone = Smartphone(
            "Телефон",
            "Описание",
            1000.0,
            1,
            90.0,
            "M",
            64,
            "Черный",
        )
        new_grass = LawnGrass(
            "Трава",
            "Описание",
            100.0,
            5,
            "Россия",
            "5 дней",
            "Зеленый",
        )
        category_smartphones.add_product(new_phone)
        category_smartphones.add_product(new_grass)
        assert new_phone in category_smartphones.products_list
        assert new_grass in category_smartphones.products_list


# ---------- Проверка isinstance / issubclass напрямую ----------


class TestIsinstanceIssubclass:
    def test_isinstance_on_products(self, smartphone1, grass1):
        assert isinstance(smartphone1, Product)
        assert isinstance(grass1, Product)

    def test_isinstance_on_non_products(self):
        assert not isinstance("строка", Product)
        assert not isinstance(42, Product)
        assert not isinstance(None, Product)

    def test_issubclass_on_subclasses(self):
        assert issubclass(Smartphone, Product)
        assert issubclass(LawnGrass, Product)
        assert issubclass(Product, Product)

    def test_issubclass_on_non_subclasses(self):
        assert not issubclass(str, Product)
        assert not issubclass(int, Product)
        assert not issubclass(Smartphone, LawnGrass)
