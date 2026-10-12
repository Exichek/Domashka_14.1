from typing import Any


class Product:
    """Класс для представления товара."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        """Инициализирует товар."""
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Возвращает цену товара."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Изменяет цену товара, если новое значение положительное."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict[str, Any]) -> "Product":
        """Создает новый товар из словаря."""
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __str__(self) -> str:
        """Возвращает строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Возвращает суммарную стоимость товаров одного класса."""
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одинакового класса")

        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс для представления смартфона."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        """Инициализирует смартфон."""
        super().__init__(name, description, price, quantity)

        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для представления газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        """Инициализирует газонную траву."""
        super().__init__(name, description, price, quantity)

        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс для представления категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: list[Product],
    ) -> None:
        """Инициализирует категорию товаров."""
        self.name = name
        self.description = description
        self.__products = list(products)

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет в категорию товар или его наследника."""
        if not isinstance(product, Product):
            raise TypeError("Добавлять можно только объекты Product и его наследников")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строку со всеми товарами категории."""
        return "".join(f"{product}\n" for product in self.__products)

    def __str__(self) -> str:
        """Возвращает название категории и общий остаток товаров."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
