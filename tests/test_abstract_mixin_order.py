import inspect

import pytest

from src.models import (
    BaseCatalogEntity,
    BaseProduct,
    Category,
    CreationLogMixin,
    LawnGrass,
    Order,
    Product,
    Smartphone,
)


def test_abstract_product() -> None:
    """Проверяет абстрактность BaseProduct."""
    assert inspect.isabstract(BaseProduct)

    with pytest.raises(TypeError):
        BaseProduct()  # type: ignore[abstract]


def test_product_inherits_base_and_mixin() -> None:
    """Проверяет цепочку наследования продуктов."""
    assert issubclass(Product, BaseProduct)
    assert issubclass(Product, CreationLogMixin)

    assert Smartphone.__bases__ == (Product,)
    assert LawnGrass.__bases__ == (Product,)


def test_mixin_logs_product_creation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет логирование создания обычного товара."""
    product = Product("Телефон", "Описание", 1000.0, 5)

    expected = "Product('Телефон', 'Описание', 1000.0, 5)"

    assert repr(product) == expected
    assert capsys.readouterr().out == expected + "\n"


def test_mixin_logs_smartphone_creation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет логирование создания смартфона."""
    phone = Smartphone(
        "Телефон",
        "Описание",
        1000.0,
        5,
        95.5,
        "X",
        256,
        "Чёрный",
    )

    expected = (
        "Smartphone('Телефон', 'Описание', 1000.0, 5, " "95.5, 'X', 256, 'Чёрный')"
    )

    assert repr(phone) == expected
    assert capsys.readouterr().out == expected + "\n"


def test_mixin_logs_lawn_grass_creation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет логирование создания газонной травы."""
    grass = LawnGrass(
        "Газон",
        "Трава",
        500.0,
        10,
        "Россия",
        "7 дней",
        "Зелёный",
    )

    expected = (
        "LawnGrass('Газон', 'Трава', 500.0, 10, " "'Россия', '7 дней', 'Зелёный')"
    )

    assert repr(grass) == expected
    assert capsys.readouterr().out == expected + "\n"


def test_mixin_logs_classmethod_creation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет логирование товара, созданного через new_product."""
    product = Product.new_product(
        {
            "name": "Товар",
            "description": "Описание",
            "price": 50.0,
            "quantity": 3,
        }
    )

    assert isinstance(product, Product)
    assert capsys.readouterr().out == ("Product('Товар', 'Описание', 50.0, 3)\n")


def test_abstract_catalog_entity() -> None:
    """Проверяет абстрактность общего класса категорий и заказов."""
    assert inspect.isabstract(BaseCatalogEntity)

    with pytest.raises(TypeError):
        BaseCatalogEntity("Название", "Описание")  # type: ignore[abstract]


def test_category_and_order_share_abstract_parent() -> None:
    """Проверяет общего родителя для Category и Order."""
    assert issubclass(Category, BaseCatalogEntity)
    assert issubclass(Order, BaseCatalogEntity)

    assert Category.__bases__ == (BaseCatalogEntity,)
    assert Order.__bases__ == (BaseCatalogEntity,)


def test_order_initialization_and_string() -> None:
    """Проверяет создание заказа и вычисление стоимости."""
    product = Product("Телефон", "Описание", 1000.0, 5)

    order = Order(product, 2)

    assert order.product is product
    assert order.name == "Телефон"
    assert order.description == "Описание"
    assert order.quantity == 2
    assert order.total_price == 2000.0

    assert str(order) == (
        "Заказ: Телефон, количество: 2 шт., " "стоимость: 2000.0 руб."
    )

    assert product.quantity == 5


def test_order_accepts_smartphone() -> None:
    """Проверяет заказ смартфона."""
    phone = Smartphone(
        "Телефон",
        "Описание",
        1500.0,
        3,
        93.2,
        "X",
        128,
        "Серый",
    )

    order = Order(phone, 2)

    assert order.product is phone
    assert order.total_price == 3000.0


def test_order_accepts_lawn_grass() -> None:
    """Проверяет заказ газонной травы."""
    grass = LawnGrass(
        "Газон",
        "Описание",
        500.0,
        10,
        "Россия",
        "7 дней",
        "Зелёный",
    )

    order = Order(grass, 4)

    assert order.product is grass
    assert order.total_price == 2000.0


@pytest.mark.parametrize(
    "invalid_product",
    ["Товар", 123, None, object()],
)
def test_order_rejects_invalid_product(
    invalid_product: object,
) -> None:
    """Проверяет запрет заказа объекта, не являющегося товаром."""
    with pytest.raises(TypeError):
        Order(invalid_product, 1)  # type: ignore[arg-type]


@pytest.mark.parametrize("quantity", [0, -1, -5])
def test_order_rejects_invalid_quantity(quantity: int) -> None:
    """Проверяет запрет нулевого и отрицательного количества."""
    product = Product("Товар", "Описание", 50.0, 10)

    with pytest.raises(ValueError):
        Order(product, quantity)


def test_category_still_works_with_shared_parent() -> None:
    """Проверяет работу категории после введения общего родителя."""
    product = Product("Товар", "Описание", 50.0, 10)
    category = Category(
        "Категория",
        "Описание категории",
        [product],
    )

    assert category.name == "Категория"
    assert category.description == "Описание категории"
    assert str(category) == "Категория, количество продуктов: 10 шт."
