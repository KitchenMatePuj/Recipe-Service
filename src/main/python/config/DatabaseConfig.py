# src/main/python/config/DatabaseConfig.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from src.main.python.ApplicationProperties import ApplicationProperties

DATABASE_URL = ApplicationProperties.DATABASE_URL  # «mysql+pymysql://…»

# --- CONNECT_ARGS ----------------------------------------------------
connect_args = (
    {"check_same_thread": False}                     # ← solo si es SQLite
    if "sqlite" in DATABASE_URL
    else {
        "charset": "utf8mb4",
        "init_command": "SET NAMES utf8mb4"
    }
)

# --- ENGINE ----------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    encoding="utf8mb4",          # ← refuerzo extra
    connect_args=connect_args
)

# --- fallback absoluto (por si el driver ignora init_command) --------
@event.listens_for(engine, "connect")
def _set_utf8(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET NAMES utf8mb4")
    cursor.close()

# --- ORM boilerplate -------------------------------------------------
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()
