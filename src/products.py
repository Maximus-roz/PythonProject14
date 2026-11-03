from src.base_product import BaseProduct
from src.print_mixin import PrintMixin


class Product(PrintMixin, BaseProduct):
    """Класс, описывающий товар."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.__price = None  # до вызова super, чтобы setter работал
        super().__init__(name=name, description=description, price=price, quantity=quantity)

    @classmethod
    def new_product(cls, product_data: dict):
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        self.__price = value


class Smartphone(Product):
    """Смартфон — наследник Product."""

    def __init__(self, name, description, price, quantity,
                 efficiency: float, model: str, memory: int, color: str):
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)


class LawnGrass(Product):
    """Трава газонная — наследник Product."""

    def __init__(self, name, description, price, quantity,
                 country: str, germination_period: str, color: str):
        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)


class CategoryIterator:
    def __init__(self, category):
        self._products = category.products_list
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = list(products)
        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        return CategoryIterator(self)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products_list(self):
        return self.__products

    @property
    def products(self):
        return "".join(f"{product}\n" for product in self.__products)