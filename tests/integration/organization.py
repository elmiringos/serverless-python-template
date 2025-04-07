from time import sleep
import pytest
from testcontainers.mysql import MySqlContainer
from unittest.mock import patch

from src.application.handler.organization_handler import create_organization
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
            "user": "root",
            "password": "test",
            "name": "serverless_template",
        }


def test_create_organization_lambda(setup_test_db):
    test_db_config = setup_test_db

    with patch.object(settings, "db") as db:
        db.HOST = test_db_config["host"]
        db.PORT = test_db_config["port"]
        db.PASSWORD = test_db_config["password"]
        db.NAME = test_db_config["name"]
        db.DRIVER = "pymysql"

        event = {
            "body": '{"name": "test", "email": "test@email.com", "description": "test"}',
        }

        sleep(10)
        response = create_organization(event, None)
        assert response["statusCode"] == 201


def test_get_organization_lambda(setup_test_db):
    test_db_config = setup_test_db

    with patch.object(settings, "db") as db:
        db.HOST = test_db_config["host"]
        db.PORT = test_db_config["port"]
        db.PASSWORD = test_db_config["password"]
        db.NAME = test_db_config["name"]
        db.DRIVER = "pymysql"

        event = {
            "pathParameters": {"organization_id": "82daa9f8-445f-4f4c-918f-9a86707af38c"},
        }

        response = create_organization(event, None)
        assert response["statusCode"] == 200
