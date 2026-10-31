class Product:
    """Класс, описывающий товар."""

    name: str
    description: str  # описание
    quantity: int  # количество
    price: float

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Сумма полной стоимости всех товаров на складе (цена × количество)."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_data: dict):
        """Создаёт объект Product из словаря с параметрами товара."""
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


class CategoryIterator:
    """Итератор по товарам одной категории."""

    def __init__(self, category):
        # получаем список товаров через публичное свойство категории
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
    """Класс, описывающий категорию товаров."""

    # Атрибуты класса — общие для всех объектов
    category_count = 0  # количество созданных категорий
    product_count = 0  # общее количество товаров во всех категориях

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = list(products)

        # Автоматическое обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product):
        """Добавляет товар в категорию."""
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products_list(self):
        """Возвращает сам список товаров (для итератора и внутреннего использования)."""
        return self.__products

    @property
    def products(self):
        """Возвращает строку со списком товаров категории."""
        return "".join(f"{product}\n" for product in self.__products)


if __name__ == "__main__":
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)
