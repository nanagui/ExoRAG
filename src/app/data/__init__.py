"""Data access and ingestion utilities."""

from .earthaccess_client import EarthAccessClient, EarthAccessCredentials  # noqa: F401
from .ingestion import IngestionRequest, LightCurveIngestionService  # noqa: F401
from .paths import get_data_dir, get_raw_data_dir, get_processed_data_dir  # noqa: F401

__all__ = [
    "EarthAccessClient",
    "EarthAccessCredentials",
    "IngestionRequest",
    "LightCurveIngestionService",
    "get_data_dir",
    "get_raw_data_dir",
    "get_processed_data_dir",
]
