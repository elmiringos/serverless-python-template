import pathlib
from alembic.config import Config
from alembic import command


def run_alembic_migrations(db_url: str):
    base_dir = pathlib.Path(__file__).resolve().parent.parent

    alembic_ini_path = base_dir / "src" / "alembic.ini"
    script_location = base_dir / "src" / "alembic"

    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.set_main_option("script_location", str(script_location))
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)

    command.upgrade(alembic_cfg, "head")
