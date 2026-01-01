"""Core parser functions and constants."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import Any, Callable, Dict, Optional


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
        return f"{{{self.uri}}}{self.local}" if self.uri else self.local

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
            if uri := nsmap.get(prefix, default_uri):
                return cls(local, uri)
            else:
                raise ValueError(f"Prefix {prefix} is not defined in the namespace map.")
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
        return _convert_sequence(value, empty_predicate=empty_predicate, enum_as=enum_as, skip_empty=skip_empty)

    # Objects with __dict__ (non-dataclass)
    if hasattr(value, "__dict__") and not isinstance(value, (str, bytes, bytearray)):
        with contextlib.suppress(TypeError):
            return _convert(vars(value), skip_empty=skip_empty, empty_predicate=empty_predicate, enum_as=enum_as)

    # Primitives
    return value


def _convert_sequence(
    value: list | tuple | set, *, empty_predicate: Callable[[Any], bool] | None, enum_as: str, skip_empty: bool
) -> list[Any]:
    """
    Converts a collection (list, tuple, or set) to a processed list with optional filtering and transformations.

    This function processes sequences by applying a conversion function to each element. It can also exclude
    elements that are considered "empty" based on a predicate function. The conversion ensures compatibility
    with JSON, producing a list regardless of the input type.

    Parameters:
        value: The input collection to be processed. Non-sequence types are not supported.
        empty_predicate: A callable that determines if an element is "empty."
            If None, the predicate is not used, and no filtering occurs.
        enum_as: A string that determines how enumerations are treated during conversion. The exact behavior
            depends on the implementation of the `_convert` function.
        skip_empty: A flag indicating whether "empty" elements, as defined by the empty_predicate,
            should be removed from the resulting list.

    Returns:
        A new list formed by processing the input collection and optionally filtering out empty elements.
    """
    seq = [_convert(v, skip_empty=skip_empty, empty_predicate=empty_predicate, enum_as=enum_as) for v in value]

    # Optionally drop empty items inside sequences
    if skip_empty:
        seq = [s for s in seq if not empty_predicate(s)]

    return seq


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
        empty_predicate: A function that returns True if a value should be considered empty.
            If None, the default considers:
            - None as empty
            - Empty strings/bytes as empty
            - Any object with len(x) == 0 as empty (lists, tuples, sets, dicts, etc.)
            Note: False and 0 are NOT considered empty by default.
        enum_as: How to represent Enum members: "value" (default) or "name".

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


def index_ids(obj: Any) -> dict[str, Any]:
    """
    Indexes all 'id' fields within a dataclass object or its nested attributes.

    The IDs are organized into a dictionary where the keys are the IDs and the values are the corresponding dataclass
    instances.

    Args:
        obj: The input object to process and extract IDs from.

    Returns:
        A dictionary mapping IDs to their corresponding dataclass instances.
    """
    result: dict[str, Any] = {}
    if not is_dataclass(obj):
        return result

    # Add IDs from child elements
    for fld in fields(obj):
        child_obj = getattr(obj, fld.name)
        if isinstance(child_obj, list):
            for item in child_obj:
                result.update(index_ids(item))
        elif fld.name == "id" and getattr(obj, fld.name) is None:
            continue
        elif fld.name == "id" and getattr(obj, fld.name):
            result[child_obj] = obj
        elif child_obj:
            result |= index_ids(child_obj)
    return result
