from functools import wraps

from src.settings import settings
from common.logger import get_logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

logger = get_logger(__name__)


class BaseRepository:
    def __init__(self):
        db = settings.db
        db_url = f"mysql+pymysql://{db.USER}:{db.PASSWORD}@{db.HOST}:{db.PORT}/{db.NAME}"
        engine = create_engine(db_url, echo=True)
        SessionLocal = sessionmaker(bind=engine)
        self.session = SessionLocal()

    def __del__(self):
        self.session.close()

    @staticmethod
    def write_ops(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                return method(self, *args, **kwargs)
            except SQLAlchemyError as e:
                logger.exception("Database error on write operations", exc_info=True)
                self.session.rollback()
                raise e
            except Exception as e:
                self.session.rollback()
                raise e

        return wrapper
