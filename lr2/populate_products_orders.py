"""
Скрипт для наполнения базы данных продуктами и заказами
"""
from decimal import Decimal

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, selectinload

from config import DATABASE_URL
from models import Order, Product, User

# Создаем фабрику подключений
engine = create_engine(
    DATABASE_URL,
    echo=True  # Логирование SQL-запросов
)

# Создание фабрики сессий
session_factory = sessionmaker(bind=engine)

# Наполняем БД данными: 5 продуктов и 5 заказов
with session_factory() as session:
    # Создаем 5 продуктов
    products = [
        Product(
            name="Ноутбук Dell XPS 15",
            description="Мощный ноутбук для работы и творчества",
            price=Decimal("1299.99")
        ),
        Product(
            name="Смартфон iPhone 15 Pro",
            description="Флагманский смартфон с продвинутой камерой",
            price=Decimal("999.99")
        ),
        Product(
            name="Наушники Sony WH-1000XM5",
            description="Беспроводные наушники с активным шумоподавлением",
            price=Decimal("399.99")
        ),
        Product(
            name="Планшет iPad Pro 12.9",
            description="Профессиональный планшет для дизайна и работы",
            price=Decimal("1099.99")
        ),
        Product(
            name="Умные часы Apple Watch Series 9",
            description="Фитнес-трекер и умные часы премиум класса",
            price=Decimal("399.99")
        )
    ]
    
    for product in products:
        session.add(product)
    
    session.flush()  # Получаем ID продуктов
    
    # Получаем пользователей и их адреса
    stmt = select(User).options(selectinload(User.addresses))
    users = session.execute(stmt).scalars().all()
    
    # Создаем 5 заказов
    # Заказ 1: Пользователь 1, адрес 1, продукты 1 и 2
    order1 = Order(
        user_id=users[0].id,
        delivery_address_id=users[0].addresses[0].id,
        total_amount=Decimal("2299.98"),  # Ноутбук + Смартфон
        status="processing"
    )
    order1.products = [products[0], products[1]]
    session.add(order1)
    
    # Заказ 2: Пользователь 2, адрес 1, продукт 3
    order2 = Order(
        user_id=users[1].id,
        delivery_address_id=users[1].addresses[0].id,
        total_amount=Decimal("399.99"),  # Наушники
        status="shipped"
    )
    order2.products = [products[2]]
    session.add(order2)
    
    # Заказ 3: Пользователь 3, адрес 1, продукты 3 и 5
    order3 = Order(
        user_id=users[2].id,
        delivery_address_id=users[2].addresses[0].id,
        total_amount=Decimal("799.98"),  # Наушники + Часы
        status="pending"
    )
    order3.products = [products[2], products[4]]
    session.add(order3)
    
    # Заказ 4: Пользователь 4, адрес 1, продукт 4
    order4 = Order(
        user_id=users[3].id,
        delivery_address_id=users[3].addresses[0].id,
        total_amount=Decimal("1099.99"),  # Планшет
        status="delivered"
    )
    order4.products = [products[3]]
    session.add(order4)
    
    # Заказ 5: Пользователь 5, адрес 1, продукты 1, 3 и 4
    order5 = Order(
        user_id=users[4].id,
        delivery_address_id=users[4].addresses[0].id,
        total_amount=Decimal("2799.97"),  # Ноутбук + Наушники + Планшет
        status="processing"
    )
    order5.products = [products[0], products[2], products[3]]
    session.add(order5)
    
    # Сохраняем все изменения
    session.commit()
    print("База данных успешно наполнена 5 продуктами и 5 заказами!")

