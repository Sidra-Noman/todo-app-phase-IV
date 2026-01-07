from sqlmodel import create_engine, Session, SQLModel
from .config import settings
from ..models import user, todo

engine = create_engine(settings.DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
