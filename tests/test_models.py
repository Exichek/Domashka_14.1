import pytest

from src.models import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """Сбрасывает счетчики категорий и товаров перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization() -> None:
    """Проверяет корректную инициализацию товара."""
    product = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )

    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_category_initialization() -> None:
    """Проверяет корректную инициализацию категории."""
    product1 = Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
    )
    product2 = Product(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14,
    )

    category = Category(
        "Смартфоны",
        "Категория смартфонов",
        [product1, product2],
    )

    assert category.name == "Смартфоны"
    assert category.description == "Категория смартфонов"
    assert category.products == [product1, product2]


def test_product_count() -> None:
    """Проверяет подсчет количества товаров."""
    product1 = Product(
        "Product 1",
        "Description 1",
        100.0,
        1,
    )
    product2 = Product(
        "Product 2",
        "Description 2",
        200.0,
        2,
    )
    product3 = Product(
        "Product 3",
        "Description 3",
        300.0,
        3,
    )

    Category(
        "Category 1",
        "Description",
        [product1, product2],
    )

    Category(
        "Category 2",
        "Description",
        [product3],
    )

    assert Category.product_count == 3


def test_category_count() -> None:
    """Проверяет подсчет количества категорий."""
    product = Product(
        "Product",
        "Description",
        100.0,
        1,
    )

    Category(
        "Category 1",
        "Description",
        [product],
    )

    Category(
        "Category 2",
        "Description",
        [],
    )

    assert Category.category_count == 2
