import pymysql
import functools
import threading

pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from util.logger import logger

from env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME


SessionLocalLazy = None
Base = declarative_base()
engine = None


def init_db():

    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s?charset=utf8mb4&autocommit=false" % (
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_NAME,
    )

    global engine
    engine = create_engine(
        SQLALCHEMY_DATABASE_URI,
        # encoding='utf-8',
        echo=False,
        pool_pre_ping=True,
        pool_size=50,
        max_overflow=50,
    )

    global SessionLocalLazy
    SessionLocalLazy = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    Base.query = SessionLocalLazy.query_property()


def SessionLocal():
    return SessionLocalLazy()


def getSessionLocalLazy():
    return SessionLocalLazy


def create_all():
    Base.metadata.create_all(engine)
    print("create all tables")


def transactional(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        session = SessionLocal()
        try:
            result = func(*args, **kwargs)
            session.commit()
            session.flush()
            return result
        except Exception as e:
            session.rollback()
            logger.exception(e)
            logger.info("transational error...")
        finally:
            session.close()

    return inner
