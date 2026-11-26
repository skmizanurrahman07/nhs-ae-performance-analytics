"""DuckDB connection management for the NHS A&E analytical database."""

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import duckdb

from nhs_ae.config import PROJECT_PATHS

DEFAULT_DATABASE_PATH = PROJECT_PATHS.database_file


def connect_database(
    database_path: Path = DEFAULT_DATABASE_PATH,
    *,
    read_only: bool = False,
) -> duckdb.DuckDBPyConnection:
    """Open a connection to the persistent analytical database."""
    if not read_only:
        database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    return duckdb.connect(
        database=str(database_path),
        read_only=read_only,
    )


@contextmanager
def database_connection(
    database_path: Path = DEFAULT_DATABASE_PATH,
    *,
    read_only: bool = False,
) -> Generator[duckdb.DuckDBPyConnection, None, None]:
    """Provide a managed DuckDB connection."""
    connection = connect_database(
        database_path,
        read_only=read_only,
    )

    try:
        yield connection
    finally:
        connection.close()
