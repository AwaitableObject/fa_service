import os


def get_postgres_uri() -> str:
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", 5432)
    password = os.environ.get("DB_PASSWORD", "postgres")
    user = os.environ.get("DB_USER", "postgres")
    name = os.environ.get("DB_NAME", "postgres")

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"
