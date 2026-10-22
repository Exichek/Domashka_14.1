import pytest

from src.models import (
    Category,
    LawnGrass,
    Order,
    Product,
    Smartphone,
    ZeroQuantityError,
)


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    Category.category_count = 0
    Category.product_count = 0


@pytest.mark.parametrize("product_class", [Product, Smartphone, LawnGrass])
def test_zero_quantity_product(product_class: type[Product]) -> None:
    extras: dict[type[Product], tuple[object, ...]] = {
        Product: (),
        Smartphone: (90.0, "X", 128, "Черный"),
        LawnGrass: ("Россия", "5 дней", "Зеленый"),
    }
    with pytest.raises(
        ValueError, match="^Товар с нулевым количеством не может быть добавлен$"
    ):
        product_class("Товар", "Описание", 100.0, 0, *extras[product_class])


def test_zero_quantity_classmethod() -> None:
    with pytest.raises(
        ValueError, match="Товар с нулевым количеством не может быть добавлен"
    ):
        Product.new_product(
            {"name": "Товар", "description": "Описание", "price": 100.0, "quantity": 0}
        )


def test_average_price_no_weighting() -> None:
    category = Category(
        "Разное",
        "Описание",
        [Product("A", "A", 100.0, 10), Product("B", "B", 300.0, 1)],
    )
    assert category.average_price() == 200.0
    assert category.middle_price() == 200.0


def test_average_price_empty() -> None:
    category = Category("Пусто", "Описание", [])
    assert category.average_price() == 0.0
    assert category.middle_price() == 0.0


def test_average_price_updates() -> None:
    category = Category("Категория", "Описание", [Product("A", "A", 100.0, 1)])
    category.add_product(Product("B", "B", 200.0, 10))
    assert category.average_price() == 150.0


def test_custom_exception() -> None:
    error = ZeroQuantityError()
    assert isinstance(error, ValueError)
    assert str(error) == "Товар с нулевым количеством не может быть добавлен"


def test_category_success_logs(capsys: pytest.CaptureFixture[str]) -> None:
    product = Product("A", "B", 100.0, 2)
    category = Category("Пусто", "Описание", [])
    capsys.readouterr()
    category.add_product(product)
    assert (
        capsys.readouterr().out
        == "Товар успешно добавлен\nОбработка добавления товара завершена\n"
    )
    assert Category.product_count == 1


def test_category_zero_stock_logs_and_rejects(
    capsys: pytest.CaptureFixture[str],
) -> None:
    product = Product("A", "B", 100.0, 2)
    product.quantity = 0
    category = Category("Категория", "Описание", [])
    capsys.readouterr()
    with pytest.raises(ZeroQuantityError):
        category.add_product(product)
    assert (
        capsys.readouterr().out
        == "Товар с нулевым количеством не может быть добавлен\nОбработка добавления товара завершена\n"
    )
    assert Category.product_count == 0
    assert category.products == ""


def test_category_init_zero_rolls_back_count(
    capsys: pytest.CaptureFixture[str],
) -> None:
    product = Product("A", "B", 100.0, 2)
    broken = Product("C", "D", 100.0, 1)
    broken.quantity = 0
    capsys.readouterr()
    with pytest.raises(ZeroQuantityError):
        Category("Категория", "Описание", [product, broken])
    assert Category.product_count == 0
    assert Category.category_count == 0
    assert capsys.readouterr().out.endswith(
        "Товар с нулевым количеством не может быть добавлен\nОбработка добавления товара завершена\n"
    )


def test_category_wrong_type_finally(capsys: pytest.CaptureFixture[str]) -> None:
    category = Category("Категория", "Описание", [])
    capsys.readouterr()
    with pytest.raises(TypeError):
        category.add_product("не товар")  # type: ignore[arg-type]
    assert capsys.readouterr().out == "Обработка добавления товара завершена\n"


def test_order_success_logs(capsys: pytest.CaptureFixture[str]) -> None:
    product = Product("A", "B", 100.0, 2)
    capsys.readouterr()
    order = Order(product, 1)
    assert order.total_price == 100.0
    assert (
        capsys.readouterr().out
        == "Товар успешно добавлен\nОбработка добавления товара завершена\n"
    )


def test_order_zero_product_finally(capsys: pytest.CaptureFixture[str]) -> None:
    product = Product("A", "B", 100.0, 2)
    product.quantity = 0
    capsys.readouterr()
    with pytest.raises(ZeroQuantityError):
        Order(product, 1)
    assert (
        capsys.readouterr().out
        == "Товар с нулевым количеством не может быть добавлен\nОбработка добавления товара завершена\n"
    )


def test_order_zero_requested_finally(capsys: pytest.CaptureFixture[str]) -> None:
    product = Product("A", "B", 100.0, 2)
    capsys.readouterr()
    with pytest.raises(ZeroQuantityError):
        Order(product, 0)
    assert capsys.readouterr().out == (
        "Товар с нулевым количеством не может быть добавлен\n"
        "Обработка добавления товара завершена\n"
    )


def test_order_wrong_type_finally(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(TypeError):
        Order("не товар", 1)  # type: ignore[arg-type]
    assert capsys.readouterr().out == "Обработка добавления товара завершена\n"
