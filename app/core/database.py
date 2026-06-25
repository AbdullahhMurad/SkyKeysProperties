from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.engine.url import make_url

SQLALCHEMY_DATABASE_URL = "postgresql://avnadmin:YOUR_PASSWORD@pg-1f53fee4-theclassicdope1-f1fe.h.aivencloud.com:28191/defaultdb?sslmode=require"

print("=" * 60)
print("DATABASE.PY LOADED")

url = make_url(SQLALCHEMY_DATABASE_URL)

print("HOST =", url.host)
print("PORT =", url.port)
print("DATABASE =", url.database)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

print("ENGINE CREATED")
print("=" * 60)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, DeclarativeBase

# from app.core.config import settings


# SQLALCHEMY_DATABASE_URL = "postgresql://avnadmin:REMOVED_AIVEN_PASSWORD@pg-1f53fee4-theclassicdope1-f1fe.h.aivencloud.com:28191/defaultdb?sslmode=require"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # engine = create_engine(settings.DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# class Base(DeclarativeBase):
#     pass


# ---------------------------------------------------------------------------
# Dependency – yields a DB session and closes it after the request finishes
# ---------------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
