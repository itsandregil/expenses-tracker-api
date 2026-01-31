from sqlmodel import create_engine

from app.core.config import settings

engine = create_engine(str(settings.POSTGRES_DATABASE_URI))
