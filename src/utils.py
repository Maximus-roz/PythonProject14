import json
from pathlib import Path

from src.products import Category, Product


def load_categories_from_json(file_path: str) -> list[Category]:
    """
    Читает JSON-файл и создаёт объекты классов Product и Category.

    :param file_path: путь к JSON-файлу
    :return: список объектов Category
    """
    path = Path(file_path)

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []

    for category_data in data:
        # Создаём объекты Product для каждой категории
        products = [
            Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            for product_data in category_data.get("products", [])
        ]

        # Создаём объект Category (счётчики класса обновятся автоматически)
        category = Category(
            name=category_data["name"],
            description=category_data["description"],
            products=products,
        )
        categories.append(category)

    return categories


if __name__ == "__main__":

    categories = load_categories_from_json(r"..\data\products.json")

    for category in categories:
        print(f"Категория: {category.name} — товаров: {len(category.products)}")

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")
