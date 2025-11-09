"""Core parser functions and constants."""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import Any, Callable, Dict, Optional


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


@dataclass(frozen=True, slots=True)
class QName:
    """QName represents a qualified name in the form {uri}local."""

    local: str
    uri: Optional[str] = None

    def __str__(self) -> str:
        if self.uri:
            return f"{{{self.uri}}}{self.local}"
        return self.local

    @classmethod
    def from_str(
        cls,
        qname: str,
        nsmap: Optional[dict[str, str]] = None,
        default_prefix: Optional[str] = None,
        default_uri: Optional[str] = None,
    ) -> QName:
        """Parse a QName from a string."""
        nsmap = nsmap or {}
        default_uri = default_uri or nsmap.get(default_prefix, None)

        if qname.startswith("{"):
            uri, local = qname[1:].split("}")
            return cls(local, uri)

        if ":" in qname:
            prefix, local = qname.split(":")
            uri = nsmap.get(prefix, default_uri)
            if not uri:
                raise ValueError(f"Prefix {prefix} is not defined in the namespace map.")
            return cls(local, uri)

        return cls(qname, default_uri)


def default_empty_predicate(x: Any) -> bool:
    """Default predicate for determining if a value is considered empty."""
    if x is None:
        return True
    if isinstance(x, (str, bytes, bytearray)):
        return len(x) == 0
    try:
        return len(x) == 0  # lists, tuples, sets, dicts, etc.
    except Exception:  # noqa: BLE001
        return False


def _enum_to_primitive(e: Enum, enum_as: str) -> Any:
    """Convert an Enum to its value or name."""
    return e.value if enum_as == "value" else e.name


def _convert(
    value: Any,
    *,
    skip_empty: bool = False,
    empty_predicate: Callable[[Any], bool] | None = None,
    enum_as: str = "value",
) -> Any:
    empty_predicate = empty_predicate or default_empty_predicate

    # Enums
    if isinstance(value, Enum):
        return _enum_to_primitive(value, enum_as=enum_as)

    # Dataclasses
    if is_dataclass(value):
        return convert_dataclass(value, skip_empty=skip_empty, empty_predicate=empty_predicate, enum_as=enum_as)

    # Dicts
    if isinstance(value, dict):
        return convert_dict(value, empty_predicate=empty_predicate, enum_as=enum_as, skip_empty=skip_empty)

    # Iterables (sequence-like) — normalize to list for JSON-friendliness
    if isinstance(value, (list, tuple, set)):
        seq = [_convert(v, skip_empty=skip_empty, empty_predicate=empty_predicate, enum_as=enum_as) for v in value]
        # Optionally drop empty items inside sequences
        if skip_empty:
            seq = [s for s in seq if not empty_predicate(s)]
        # Preserve tuple if you prefer; here we choose list for JSON-friendliness
        return seq

    # Objects with __dict__ (non-dataclass)
    if hasattr(value, "__dict__") and not isinstance(value, (str, bytes, bytearray)):
        try:
            return _convert(vars(value), skip_empty=skip_empty, empty_predicate=empty_predicate, enum_as=enum_as)
        except TypeError:
            # vars may fail (e.g., for some extension types); fall through to return as-is
            pass

    # Primitives
    return value


def convert_dict(
    value: dict, *, empty_predicate: Callable[[Any], bool] | None, enum_as: str, skip_empty: bool
) -> dict[Any, Any]:
    """
    Converts a dictionary by transforming its keys and values and omitting entries depending on a given predicate.

    Summary:
    - Keys that are Enum instances are processed based on the provided `enum_as` behavior.
    - Remaining keys are left unaltered.
    - Values are always recursively converted using internal conversion logic.
    - Entries can be skipped if `skip_empty` is set to True and the predicate function indicates
      that the value is considered empty.

    Args:
        value: The dictionary to be converted.
        empty_predicate: A predicate function that determines whether a value is considered empty.
            If None, no predicate is applied.
        enum_as: Specifies the behavior for converting Enum instances. Accepted values depend on
            internal Enum conversion logic.
        skip_empty: A flag indicating whether to skip entries where the predicate function identifies
            the value as empty.

    Returns:
        A newly converted dictionary with potentially altered keys and values and with entries optionally
        removed based on the given predicate.
    """
    out: Dict[Any, Any] = {}
    for k, v in value.items():
        ck = _enum_to_primitive(k, enum_as=enum_as) if isinstance(k, Enum) else k
        cv = _convert(v)
        if skip_empty and empty_predicate(cv):
            continue
        out[ck] = cv
    return out


def convert_dataclass(
    value: Any,
    *,
    skip_empty: bool = False,
    empty_predicate: Callable[[Any], bool] | None = None,
    enum_as: str = "value",
) -> dict[str, Any]:
    """
    Converts a dataclass object into a dictionary representation.

    The function processes each field of a dataclass, transforming its value if needed. It can optionally
    omit fields based on specific conditions, such as empty values. Additionally, it incorporates any extra
    key-value pairs provided by the dataclass's `__extra_kwargs__` attribute.

    Args:
        value: The dataclass instance to be converted.
        skip_empty: Whether to skip empty fields. Defaults to False.
        empty_predicate: A function to determine if a value is empty. Defaults to None.
        enum_as: How to represent Enum members: "value" (default) or "name".

    Returns:
        A dictionary representation of the dataclass instance, possibly excluding empty fields.
    """
    out: Dict[str, Any] = {}

    for f in fields(value):
        v = getattr(value, f.name)
        cv = _convert(v, skip_empty=skip_empty, empty_predicate=empty_predicate, enum_as=enum_as)
        if skip_empty and empty_predicate(cv):
            continue
        out[f.name] = cv
    for key, val in getattr(value, "__extra_kwargs__", {}).items():
        cv = _convert(val, skip_empty=skip_empty, empty_predicate=empty_predicate, enum_as=enum_as)
        if skip_empty and empty_predicate(cv):
            continue
        out[key] = cv
    return out


def dataclass_to_dict(
    obj: Any,
    *,
    skip_empty: bool = False,
    empty_predicate: Callable[[Any], bool] | None = None,
    enum_as: str = "value",  # "value" | "name"
) -> Any:
    """
    Recursively convert a dataclass instance to a plain Python structure (dicts/lists/etc.).

    - Handles nested dataclasses, dicts, lists/tuples/sets, and basic types.
    - Optionally skips fields whose converted value is considered "empty".
    - Basic handling for Enum values (choose name or value via `enum_as`).

    Args:
        obj: The object to convert (typically a dataclass instance, but dicts/lists/etc. are accepted).
        skip_empty: If True, fields/items with empty values are omitted from the result.
        enum_as : How to represent Enum members: "value" (default) or "name".
        empty_predicate: A function that returns True if a value should be considered empty.
            If None, the default considers:
            - None as empty
            - Empty strings/bytes as empty
            - Any object with len(x) == 0 as empty (lists, tuples, sets, dicts, etc.)
            Note: False and 0 are NOT considered empty by default.

    Returns:
        A structure of plain dicts/lists/tuples with primitive values (and optionally Enums mapped to name/value).

    Notes:
        - Cyclic references are not handled; they will cause recursion errors.
        - Non-dataclass arbitrary objects are converted via `vars(obj)` when possible.
    """
    empty_predicate = empty_predicate or default_empty_predicate

    result = _convert(obj, skip_empty=skip_empty, empty_predicate=empty_predicate, enum_as=enum_as)

    # If the root itself is empty and skip_empty=True, return an empty dict instead of dropping everything
    if skip_empty and empty_predicate(result):
        return {} if isinstance(result, dict) else result

    return result
