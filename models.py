"""
ORM модели для пользователей, адресов, продуктов и заказов
"""
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Table, Column, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column()  # Дополнительное строковое поле
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    
    # Связь один-ко-многим с адресами
    addresses = relationship("Address", back_populates="user")
    # Связь один-ко-многим с заказами
    orders = relationship("Order", back_populates="user")


class Address(Base):
    """Модель адреса"""
    __tablename__ = 'addresses'
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column(nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    
    # Связь многие-к-одному с пользователем
    user = relationship("User", back_populates="addresses")
    # Связь один-ко-многим с заказами (адрес доставки)
    orders = relationship("Order", back_populates="delivery_address")


# Промежуточная таблица для связи многие-ко-многим между Order и Product
order_product_association = Table(
    'order_product',
    Base.metadata,
    Column('order_id', ForeignKey('orders.id'), primary_key=True),
    Column('product_id', ForeignKey('products.id'), primary_key=True),
    Column('quantity', Integer, default=1)  # Количество продукта в заказе
)


class Product(Base):
    """Модель продукта"""
    __tablename__ = 'products'
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    
    # Связь многие-ко-многим с заказами
    orders = relationship("Order", secondary=order_product_association, back_populates="products")


class Order(Base):
    """Модель заказа"""
    __tablename__ = 'orders'
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    delivery_address_id: Mapped[UUID] = mapped_column(ForeignKey('addresses.id'), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default="pending")  # pending, processing, shipped, delivered
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    
    # Связь многие-к-одному с пользователем
    user = relationship("User", back_populates="orders")
    # Связь многие-к-одному с адресом доставки
    delivery_address = relationship("Address", back_populates="orders")
    # Связь многие-ко-многим с продуктами
    products = relationship("Product", secondary=order_product_association, back_populates="orders")

