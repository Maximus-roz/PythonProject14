from src.products import Product


class LawnGrass(Product):
    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        super().__init__(name, description, price, quantity)
        self.germination_period = germination_period  # срок прорастания
        self.country = country  # страна-производитель
        self.color = color
