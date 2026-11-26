"""Project configuration and filesystem conventions."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProjectPaths:
    """Immutable collection of project paths.

    Attributes:
        root: Repository root directory.
    """

    root: Path

    @property
    def data(self) -> Path:
        """Return the data directory."""
        return self.root / "data"

    @property
    def raw(self) -> Path:
        """Return the immutable raw-data directory."""
        return self.data / "raw"

    @property
    def interim(self) -> Path:
        """Return the intermediate-data directory."""
        return self.data / "interim"

    @property
    def processed(self) -> Path:
        """Return the curated-data directory."""
        return self.data / "processed"

    @property
    def analytical(self) -> Path:
        """Return the controlled analytical-output directory."""
        return self.data / "analytical"

    @property
    def database(self) -> Path:
        """Return the analytical-database directory."""
        return self.data / "database"

    @property
    def database_file(self) -> Path:
        """Return the persistent DuckDB database path."""
        return self.database / "nhs_ae.duckdb"

    @property
    def reference(self) -> Path:
        """Return the reference-data directory."""
        return self.data / "reference"

    @property
    def sql(self) -> Path:
        """Return the version-controlled SQL directory."""
        return self.root / "sql"

    @property
    def master_dataset(self) -> Path:
        """Return the validated 25-month provider dataset path."""
        return (
            self.processed
            / "nhs_ae_provider_2024_09_to_2026_09.csv"
        )

    @classmethod
    def from_file(cls, file_path: Path) -> "ProjectPaths":
        """Locate project root from the configuration module path.

        Args:
            file_path: Path to ``src/nhs_ae/config.py``.

        Returns:
            Configured project paths.
        """
        return cls(root=file_path.resolve().parents[2])


PROJECT_PATHS = ProjectPaths.from_file(Path(__file__))
