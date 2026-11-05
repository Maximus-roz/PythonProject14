from src.base_product import BaseProduct
from src.print_mixin import PrintMixin


class Product(PrintMixin, BaseProduct):
    """Класс, описывающий товар.

    Наследует функциональность печати (PrintMixin) и базовую логику продукта
    (BaseProduct). Хранит название, описание, цену и количество товара.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Инициализирует товар.

        Args:
            name (str): Название товара.
            description (str): Описание товара.
            price (float): Цена товара. Должна быть положительной.
            quantity (int): Количество товара. Должно быть больше нуля.

        Raises:
            ValueError: Если количество товара меньше или равно нулю.
        """
        self.__price = None  # до вызова super, чтобы setter работал
        if quantity > 0:
            self.quantity = quantity
        else:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(
            name=name, description=description, price=price, quantity=quantity
        )

    @classmethod
    def new_product(cls, product_data: dict):
        """Создаёт новый товар из словаря с данными.

        Args:
            product_data (dict): Словарь с ключами "name", "description",
                "price", "quantity".

        Returns:
            Product: Новый экземпляр класса Product.
        """
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def price(self):
        """float: Цена товара."""
        return self.__price

    @price.setter
    def price(self, value):
        """Устанавливает цену товара.

        Args:
            value (float): Новая цена товара.

        Raises:
            ValueError: Если цена меньше или равна нулю.
        """
        if value <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        self.__price = value


class Smartphone(Product):
    """Смартфон — наследник Product.

    Дополнительно хранит характеристики: эффективность, модель, объём памяти
    и цвет.
    """

    def __init__(
        self,
        name,
        description,
        price,
        quantity,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        """Инициализирует смартфон.

        Args:
            name (str): Название смартфона.
            description (str): Описание смартфона.
            price (float): Цена смартфона.
            quantity (int): Количество смартфонов.
            efficiency (float): Эффективность смартфона.
            model (str): Модель смартфона.
            memory (int): Объём памяти смартфона.
            color (str): Цвет смартфона.
        """
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)


class LawnGrass(Product):
    """Трава газонная — наследник Product.

    Дополнительно хранит страну происхождения, срок всхожести и цвет.
    """

    def __init__(
        self,
        name,
        description,
        price,
        quantity,
        country: str,
        germination_period: str,
        color: str,
    ):
        """Инициализирует газонную траву.

        Args:
            name (str): Название травы.
            description (str): Описание травы.
            price (float): Цена травы.
            quantity (int): Количество травы.
            country (str): Страна происхождения.
            germination_period (str): Срок всхожести.
            color (str): Цвет травы.
        """
        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)


class CategoryIterator:
    """Итератор для перебора товаров категории."""

    def __init__(self, category):
        """Инициализирует итератор.

        Args:
            category (Category): Категория, товары которой нужно перебрать.
        """
        self._products = category.products_list
        self._index = 0

    def __iter__(self):
        """Возвращает сам итератор."""
        return self

    def __next__(self):
        """Возвращает следующий товар категории.

        Returns:
            Product: Следующий товар.

        Raises:
            StopIteration: Если товары закончились.
        """
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product


class Category:
    """Класс, описывающий категорию товаров.

    Хранит название, описание и список товаров. Поддерживает итерацию
    по товарам и подсчёт общей статистики по категориям и товарам.
    """

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        """Инициализирует категорию.

        Args:
            name (str): Название категории.
            description (str): Описание категории.
            products (list[Product]): Список товаров категории.
        """
        self.name = name
        self.description = description
        self.__products = list(products)
        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        """Возвращает строковое представление категории.

        Returns:
            str: Название категории и суммарное количество товаров.
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """Возвращает итератор по товарам категории.

        Returns:
            CategoryIterator: Итератор товаров.
        """
        return CategoryIterator(self)

    def add_product(self, product):
        """Добавляет товар в категорию.

        Args:
            product (Product): Товар для добавления.

        Raises:
            TypeError: Если передан объект, не являющийся Product.
        """
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product")
        self.__products.append(product)
        Category.product_count += 1

    def middle_price(self):
        """Вычисляет среднюю цену товаров в категории.

        Returns:
            float: Средняя цена товаров или 0, если категория пуста.
        """
        try:
            total = sum(product.price for product in self.__products)
            return total / len(self.__products)
        except ZeroDivisionError:
            return 0

    @property
    def products_list(self):
        """list[Product]: Список товаров категории."""
        return self.__products

    @property
    def products(self):
        """str: Строковое представление всех товаров категории."""
        return "".join(f"{product}\n" for product in self.__products)