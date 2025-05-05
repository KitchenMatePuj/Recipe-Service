# src/main/python/config/DatabaseConfig.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from src.main.python.ApplicationProperties import ApplicationProperties

DATABASE_URL = ApplicationProperties.DATABASE_URL

# --- connect_args ----------------------------------------------------
connect_args = (
    {"check_same_thread": False}                          # solo SQLite
    if DATABASE_URL.startswith("sqlite")
    else {
        "charset": "utf8mb4",
        "init_command": "SET NAMES utf8mb4"
    }
)

# --- engine ----------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    connect_args=connect_args
)

# red de seguridad (por si el driver ignora init_command)
@event.listens_for(engine, "connect")
def _force_utf8(dbapi_conn, _):
    cursor = dbapi_conn.cursor()
    cursor.execute("SET NAMES utf8mb4")
    cursor.close()

# --- ORM boilerplate -------------------------------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)
Base = declarative_base()

# --- ESTA FUNCIÓN ES IMPRESCINDIBLE ---------------------------------
def get_db():
    """Dependency que inyectan todos los controladores."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
