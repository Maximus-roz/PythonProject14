from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Сумма полной стоимости товаров на складе (цена × количество)."""
        if type(self) is type(other):
            return self.price * self.quantity + other.price * other.quantity
        raise TypeError("Нельзя складывать товары разных классов")

    @property
    @abstractmethod
    def price(self):
        """Цена товара — должна быть реализована в наследниках."""
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        pass
