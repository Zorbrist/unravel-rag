from dataclasses import dataclass


def log_calls(func):
    return func


@dataclass
class Product:
    name: str
    price: float


class ProductService:
    def __init__(self):
        self.products = []

    def add_product(self, name, price):
        product = Product(name, price)
        self.products.append(product)
        return product