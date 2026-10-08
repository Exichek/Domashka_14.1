import pytest

from src.models import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """Сбрасывает счетчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def products() -> list[Product]:
    """Создает товары для тестирования."""
    return [
        Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5),
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
    ]


def test_product_initialization() -> None:
    """Проверяет инициализацию товара."""
    product = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет",
        180000.0,
        5,
    )

    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_category_initialization(products: list[Product]) -> None:
    """Проверяет инициализацию категории."""
    category = Category(
        "Смартфоны",
        "Категория смартфонов",
        products,
    )

    assert category.name == "Смартфоны"
    assert category.description == "Категория смартфонов"
    assert category.products == (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
    )


def test_category_count(products: list[Product]) -> None:
    """Проверяет количество созданных категорий."""
    Category("Смартфоны", "Описание", products)
    assert Category.category_count == 1

    Category("Телевизоры", "Описание", [])
    assert Category.category_count == 2


def test_product_count(products: list[Product]) -> None:
    """Проверяет общий счетчик товаров."""
    category1 = Category("Смартфоны", "Описание", products)
    assert Category.product_count == 2

    product3 = Product("Телевизор", "QLED 4K", 123000.0, 7)
    Category("Телевизоры", "Описание", [product3])
    assert Category.product_count == 3

    product4 = Product("Планшет", "128GB", 50000.0, 4)
    category1.add_product(product4)
    assert Category.product_count == 4


def test_add_product() -> None:
    """Проверяет добавление товара в категорию."""
    category = Category("Смартфоны", "Описание", [])
    product = Product("Iphone 15", "512GB", 210000.0, 8)

    result = category.add_product(product)

    assert result is None
    assert category.products == "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
    assert Category.product_count == 1


def test_empty_category_products() -> None:
    """Проверяет вывод товаров пустой категории."""
    category = Category("Пустая категория", "Описание", [])

    assert category.products == ""


def test_products_are_private(products: list[Product]) -> None:
    """Проверяет приватность списка товаров."""
    category = Category("Смартфоны", "Описание", products)

    with pytest.raises(AttributeError):
        getattr(category, "__products")


def test_new_product() -> None:
    """Проверяет создание товара из словаря."""
    product_data = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет",
        "price": 180000.0,
        "quantity": 5,
    }

    product = Product.new_product(product_data)

    assert isinstance(product, Product)
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_price_getter() -> None:
    """Проверяет получение цены через геттер."""
    product = Product("Телефон", "Описание", 1000.0, 5)

    assert product.price == 1000.0


def test_price_setter_positive() -> None:
    """Проверяет изменение цены на положительную."""
    product = Product("Телефон", "Описание", 1000.0, 5)

    product.price = 1500.0

    assert product.price == 1500.0


@pytest.mark.parametrize("invalid_price", [0.0, -100.0])
def test_price_setter_invalid(
    invalid_price: float,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет запрет нулевой и отрицательной цены."""
    product = Product("Телефон", "Описание", 1000.0, 5)

    product.price = invalid_price

    assert product.price == 1000.0
    assert capsys.readouterr().out == (
        "Цена не должна быть " "нулевая или отрицательная\n"
    )


def test_price_is_private() -> None:
    """Проверяет приватность атрибута цены."""
    product = Product("Телефон", "Описание", 1000.0, 5)

    with pytest.raises(AttributeError):
        getattr(product, "__price")
