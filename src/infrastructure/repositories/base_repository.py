from functools import wraps

from src.config import DB_CONFIG
from common.logger import get_logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DB_URL = (
    f"{DB_CONFIG['DRIVER']}://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}"
    f"@{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['NAME']}"
)
engine = create_engine(DB_URL, echo=False)
logger = get_logger(__name__)
Session = sessionmaker(bind=engine)


class BaseRepository:
    def __init__(self):
        self.session = Session()

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
