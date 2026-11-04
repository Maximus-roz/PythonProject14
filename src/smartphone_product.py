from src.products import Product


class Smartphone(Product):
    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency  # производительность
        self.model = model
        self.memory = memory
        self.color = color
