from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, selectinload
from config import DATABASE_URL
from models import User


engine = create_engine(
    DATABASE_URL,
    echo=True 
)

session_factory = sessionmaker(bind=engine)

with session_factory() as session:
    stmt = select(User).options(selectinload(User.addresses))
    users = session.execute(stmt).scalars().all()
    
    print("\n" + "="*60)
    print("ПОЛЬЗОВАТЕЛИ И ИХ АДРЕСА:")
    print("="*60)
    
    for user in users:
        print(f"\nПользователь: {user.username} ({user.email})")
        print(f"  Создан: {user.created_at}")
        print(f"  Адреса ({len(user.addresses)}):")
        for address in user.addresses:
            primary_mark = " [ОСНОВНОЙ]" if address.is_primary else ""
            print(f"    - {address.street}, {address.city}, {address.state} {address.zip_code}, {address.country}{primary_mark}")
    
    print("\n" + "="*60)



