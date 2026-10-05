from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session

from app.core.config import DATABASE_URL

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL must be configured")

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db:Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()

