from abc import ABC, abstractmethod
from inspect import signature
from typing import Any


class ZeroQuantityError(ValueError):
    """Исключение для попытки добавить товар с нулевым остатком."""

    def __init__(self) -> None:
        super().__init__("Товар с нулевым количеством не может быть добавлен")


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __str__(self) -> str:
        """Возвращает строковое представление продукта."""

    @abstractmethod
    def __add__(self, other: "Product") -> float:
        """Возвращает общую стоимость двух продуктов."""


class CreationLogMixin:
    """Миксин для вывода информации о созданном объекте."""

    def __init__(self) -> None:
        """Выводит информацию после инициализации атрибутов."""
        super().__init__()
        print(repr(self))

    def __repr__(self) -> str:
        """Возвращает класс и параметры создания объекта."""
        parameters = signature(type(self).__init__).parameters

        arguments = ", ".join(
            repr(getattr(self, name)) for name in parameters if name != "self"
        )

        return f"{type(self).__name__}({arguments})"


class Product(CreationLogMixin, BaseProduct):
    """Класс для представления товара."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        """Инициализирует товар с ненулевым остатком."""
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

        super().__init__()

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
        """Создает товар из словаря."""
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
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

        super().__init__(name, description, price, quantity)


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
        self.country = country
        self.germination_period = germination_period
        self.color = color

        super().__init__(name, description, price, quantity)


class BaseCatalogEntity(ABC):
    """Абстрактный класс для категорий и заказов."""

    def __init__(self, name: str, description: str) -> None:
        """Инициализирует общие атрибуты."""
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""


class Category(BaseCatalogEntity):
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
        super().__init__(name, description)
        self.__products: list[Product] = []
        try:
            for product in products:
                self.add_product(product)
        except (TypeError, ZeroQuantityError):
            Category.product_count -= len(self.__products)
            raise
        else:
            Category.category_count += 1

    def add_product(self, product: Product) -> None:
        """Добавляет в категорию товар или его наследника."""
        try:
            if not isinstance(product, Product):
                raise TypeError(
                    "Добавлять можно только объекты Product и его наследников"
                )
            if product.quantity == 0:
                raise ZeroQuantityError()

            self.__products.append(product)
            Category.product_count += 1
        except ZeroQuantityError as error:
            print(error)
            raise
        else:
            print("Товар успешно добавлен")
        finally:
            print("Обработка добавления товара завершена")

    def average_price(self) -> float:
        """Возвращает среднюю цену позиции без учета остатков."""
        try:
            return sum(product.price for product in self.__products) / len(
                self.__products
            )
        except ZeroDivisionError:
            return 0.0

    def middle_price(self) -> float:
        """Совместимое название метода средней цены."""
        return self.average_price()

    @property
    def products(self) -> str:
        """Возвращает строку со всеми товарами категории."""
        return "".join(f"{product}\n" for product in self.__products)

    def __str__(self) -> str:
        """Возвращает название категории и общий остаток товаров."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


class Order(BaseCatalogEntity):
    """Класс для представления заказа на один товар."""

    def __init__(self, product: Product, quantity: int) -> None:
        """Инициализирует заказ и рассчитывает его стоимость."""
        try:
            if not isinstance(product, Product):
                raise TypeError("В заказе должен быть объект Product")
            if product.quantity == 0:
                raise ZeroQuantityError()
            if quantity == 0:
                raise ZeroQuantityError()
            if quantity < 0:
                raise ValueError("Количество товара должно быть положительным")

            super().__init__(product.name, product.description)
            self.product = product
            self.quantity = quantity
            self.total_price = product.price * quantity
        except ZeroQuantityError as error:
            print(error)
            raise
        else:
            print("Товар успешно добавлен")
        finally:
            print("Обработка добавления товара завершена")

    def __str__(self) -> str:
        """Возвращает информацию о заказе."""
        return (
            f"Заказ: {self.product.name}, "
            f"количество: {self.quantity} шт., "
            f"стоимость: {self.total_price} руб."
        )
