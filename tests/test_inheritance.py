import pytest

from src.models import Category, LawnGrass, Product, Smartphone


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """Сбрасывает счетчики категорий перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def smartphone() -> Smartphone:
    """Создает смартфон для тестирования."""
    return Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )


@pytest.fixture
def grass() -> LawnGrass:
    """Создает газонную траву для тестирования."""
    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )


def test_smartphone_initialization(smartphone: Smartphone) -> None:
    """Проверяет инициализацию смартфона."""
    assert smartphone.name == "Samsung Galaxy S23 Ultra"
    assert smartphone.description == "256GB, Серый цвет"
    assert smartphone.price == 180000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23 Ultra"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_lawn_grass_initialization(grass: LawnGrass) -> None:
    """Проверяет инициализацию газонной травы."""
    assert grass.name == "Газонная трава"
    assert grass.description == "Элитная трава для газона"
    assert grass.price == 500.0
    assert grass.quantity == 20
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


def test_inheritance(
    smartphone: Smartphone,
    grass: LawnGrass,
) -> None:
    """Проверяет наследование от Product."""
    assert isinstance(smartphone, Product)
    assert isinstance(grass, Product)

    assert issubclass(Smartphone, Product)
    assert issubclass(LawnGrass, Product)


def test_smartphone_str(smartphone: Smartphone) -> None:
    """Проверяет унаследованное строковое представление смартфона."""
    assert str(smartphone) == ("Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.")


def test_lawn_grass_str(grass: LawnGrass) -> None:
    """Проверяет унаследованное строковое представление травы."""
    assert str(grass) == ("Газонная трава, 500.0 руб. Остаток: 20 шт.")


def test_smartphone_price(smartphone: Smartphone) -> None:
    """Проверяет наследование геттера и сеттера цены."""
    assert smartphone.price == 180000.0

    smartphone.price = 190000.0
    assert smartphone.price == 190000.0


def test_lawn_grass_price(grass: LawnGrass) -> None:
    """Проверяет изменение цены газонной травы."""
    assert grass.price == 500.0

    grass.price = 600.0
    assert grass.price == 600.0


def test_smartphone_add(smartphone: Smartphone) -> None:
    """Проверяет сложение двух смартфонов."""
    smartphone2 = Smartphone(
        "Iphone 15",
        "512GB",
        210000.0,
        8,
        98.2,
        "15",
        512,
        "Серый",
    )

    assert smartphone + smartphone2 == 2580000.0


def test_lawn_grass_add(grass: LawnGrass) -> None:
    """Проверяет сложение двух видов газонной травы."""
    grass2 = LawnGrass(
        "Газонная трава 2",
        "Выносливая трава",
        450.0,
        15,
        "США",
        "5 дней",
        "Темно-зеленый",
    )

    assert grass + grass2 == 16750.0


def test_different_subclasses_add(
    smartphone: Smartphone,
    grass: LawnGrass,
) -> None:
    """Проверяет запрет сложения разных классов товаров."""
    with pytest.raises(TypeError):
        smartphone + grass

    with pytest.raises(TypeError):
        grass + smartphone


def test_product_and_subclass_add(
    smartphone: Smartphone,
) -> None:
    """Проверяет запрет сложения Product и его наследника."""
    product = Product("Телефон", "Описание", 1000.0, 5)

    with pytest.raises(TypeError):
        product + smartphone

    with pytest.raises(TypeError):
        smartphone + product


def test_category_accepts_subclasses(
    smartphone: Smartphone,
    grass: LawnGrass,
) -> None:
    """Проверяет добавление наследников Product в категорию."""
    category = Category("Товары", "Разные товары", [])

    category.add_product(smartphone)
    category.add_product(grass)

    assert Category.product_count == 2
    assert str(category) == "Товары, количество продуктов: 25 шт."
    assert str(smartphone) in category.products
    assert str(grass) in category.products


def test_category_accepts_product() -> None:
    """Проверяет добавление обычного Product в категорию."""
    category = Category("Товары", "Описание", [])
    product = Product("Телефон", "Описание", 1000.0, 5)

    category.add_product(product)

    assert Category.product_count == 1
    assert str(product) in category.products


def test_category_rejects_invalid_objects() -> None:
    """Проверяет запрет добавления объектов других типов."""
    category = Category("Товары", "Описание", [])

    invalid_objects = ["Not a product", 123, None, object()]

    for invalid_object in invalid_objects:
        with pytest.raises(TypeError):
            category.add_product(invalid_object)  # type: ignore[arg-type]

    assert Category.product_count == 0
    assert category.products == ""
