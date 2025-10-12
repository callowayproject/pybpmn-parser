"""Core parser functions and constants."""

from dataclasses import fields, is_dataclass
from typing import Any


def strtobool(value: str) -> bool:
    """Convert a string representation of truth to true (1) or false (0)."""
    value = str(value).lower()
    return value in ("y", "yes", "on", "1", "true", "t")


def get_fields_by_metadata(data_class: Any, key: str, val: Any) -> dict[str, Any]:
    """Get fields from a data class based on metadata."""
    if not is_dataclass(data_class):
        return {}
    return {
        field.name: getattr(data_class, field.name) for field in fields(data_class) if field.metadata.get(key) == val
    }
