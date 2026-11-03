class PrintMixin:
    """Миксин: при создании объекта печатает его repr в консоль."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.description!r}, {self.price!r}, {self.quantity!r})"
        )