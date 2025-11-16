from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Address, User


engine = create_engine(
    DATABASE_URL,
    echo=True
)

session_factory = sessionmaker(bind=engine)

with session_factory() as session:
   
    user1 = User(username="john_doe", email="john.doe@example.com")
    session.add(user1)
    session.flush()
    address1_1 = Address(
        user_id=user1.id,
        street="123 Main Street",
        city="New York",
        state="NY",
        zip_code="10001",
        country="USA",
        is_primary=True
    )
    address1_2 = Address(
        user_id=user1.id,
        street="456 Park Avenue",
        city="New York",
        state="NY",
        zip_code="10022",
        country="USA",
        is_primary=False
    )
    session.add(address1_1)
    session.add(address1_2)
    
    user2 = User(username="jane_smith", email="jane.smith@example.com")
    session.add(user2)
    session.flush()
    
    address2_1 = Address(
        user_id=user2.id,
        street="789 Oak Boulevard",
        city="Los Angeles",
        state="CA",
        zip_code="90001",
        country="USA",
        is_primary=True
    )
    session.add(address2_1)
    
    user3 = User(username="bob_wilson", email="bob.wilson@example.com")
    session.add(user3)
    session.flush()
    
    address3_1 = Address(
        user_id=user3.id,
        street="321 Elm Street",
        city="Chicago",
        state="IL",
        zip_code="60601",
        country="USA",
        is_primary=True
    )
    address3_2 = Address(
        user_id=user3.id,
        street="654 Pine Road",
        city="Chicago",
        state="IL",
        zip_code="60602",
        country="USA",
        is_primary=False
    )
    session.add(address3_1)
    session.add(address3_2)
    
    user4 = User(username="alice_brown", email="alice.brown@example.com")
    session.add(user4)
    session.flush()
    
    address4_1 = Address(
        user_id=user4.id,
        street="987 Maple Drive",
        city="Houston",
        state="TX",
        zip_code="77001",
        country="USA",
        is_primary=True
    )
    session.add(address4_1)
    
    user5 = User(username="charlie_davis", email="charlie.davis@example.com")
    session.add(user5)
    session.flush()
    
    address5_1 = Address(
        user_id=user5.id,
        street="147 Cedar Lane",
        city="Phoenix",
        state="AZ",
        zip_code="85001",
        country="USA",
        is_primary=True
    )
    address5_2 = Address(
        user_id=user5.id,
        street="258 Birch Street",
        city="Phoenix",
        state="AZ",
        zip_code="85002",
        country="USA",
        is_primary=False
    )
    session.add(address5_1)
    session.add(address5_2)
    
    session.commit()
    print("База данных успешно наполнена 5 пользователями и их адресами!")

