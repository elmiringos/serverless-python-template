import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.mysql import MySqlContainer
from unittest.mock import patch

from src.infrastructure.models import Organization
from src.application.handler.organization_handler import create_organization, get_organization
from src.settings import settings
from tests.utils import run_alembic_migrations


@pytest.fixture(scope="module")
def mysql_container():
    container = MySqlContainer("mysql:8.0")
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope="module")
def setup_test_db():
    """Sets up a MySQL container for testing."""
    with MySqlContainer("mysql:8.0") as mysql:
        # Override the settings to use the container
        settings.db.HOST = mysql.get_container_host_ip()
        settings.db.PORT = mysql.get_exposed_port(3306)
        settings.db.USER = mysql.username
        settings.db.PASSWORD = mysql.password
        settings.db.NAME = mysql.dbname

        test_db_url = (
            f"mysql+pymysql://{mysql.username}:"
            f"{mysql.password}@{mysql.get_container_host_ip()}:"
            f"{mysql.get_exposed_port(3306)}/"
            f"{mysql.dbname}"
        )

        run_alembic_migrations(test_db_url)

        yield {
            "host": mysql.get_container_host_ip(),
            "port": mysql.get_exposed_port(3306),
            "user": mysql.username,
            "password": mysql.password,
            "name": mysql.dbname,
        }


@pytest.fixture
def seed_organization_data(setup_test_db):
    """Seeds the test organization table."""
    db_url = (
        f"mysql+pymysql://{setup_test_db['user']}:"
        f"{setup_test_db['password']}@{setup_test_db['host']}:"
        f"{setup_test_db['port']}/"
        f"{setup_test_db['name']}"
    )

    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    test_org = Organization(
        id=str(uuid.uuid4()),
        name="Test Org",
        email="seed@test.com",
        description="Seeded test organization",
    )
    session.add(test_org)
    session.commit()
    yield test_org
    session.close()


def test_create_organization_lambda(setup_test_db):
    test_db_config = setup_test_db

    with patch.object(settings, "db") as db:
        db.HOST = test_db_config["host"]
        db.PORT = test_db_config["port"]
        db.PASSWORD = test_db_config["password"]
        db.NAME = test_db_config["name"]
        db.USER = test_db_config["user"]
        db.DRIVER = "pymysql"

        event = {
            "body": '{"name": "test", "email": "test@email.com", "description": "test"}',
        }

        response = create_organization(event, None)
        assert response["statusCode"] == 201


def test_get_organization_lambda(setup_test_db, seed_organization_data):
    test_db_config = setup_test_db
    test_organization_data = seed_organization_data

    if not test_organization_data:
        raise ValueError("Failed to seed organization data")

    with patch.object(settings, "db") as db:
        db.HOST = test_db_config["host"]
        db.PORT = test_db_config["port"]
        db.PASSWORD = test_db_config["password"]
        db.NAME = test_db_config["name"]
        db.USER = test_db_config["user"]
        db.DRIVER = "pymysql"

        event = {
            "pathParameters": {"organization_id": test_organization_data.id},
        }

        response = get_organization(event, None)
        assert response["statusCode"] == 200
