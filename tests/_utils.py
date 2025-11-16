"""Helpful utilities for testing."""

from dataclasses import is_dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import lxml.etree as ET  # NOQA: N812
from pytest import param
from yaml import safe_load

from pybpmn_parser.bpmn.types import NAMESPACES

TAG_FILE = Path(__file__).parent / "example_tags.yaml"
TAGS = None


def example_tags() -> dict[str, list]:
    """Load example tags from the YAML file."""
    global TAGS

    if TAGS is None:
        with open(TAG_FILE, encoding="utf-8") as f:
            TAGS = safe_load(f)

    return TAGS


@runtime_checkable
class Parseable(Protocol):
    """An object with a parse method."""

    @classmethod
    def parse(cls, obj: ET.Element) -> Any:
        """Parse an XML element into this class."""
        ...


def xml_test(xml_str: str, expected: dict, xml_tag: str, klass: Parseable) -> Any:
    """Test parsing an XML element from a string."""
    # Assemble
    xml_obj = ET.fromstring(xml_str)

    # Act
    result = klass.parse(xml_obj.find(f"./{xml_tag}", NAMESPACES))

    # Assert
    assert isinstance(result, klass)
    for key, value in expected.items():
        assert getattr(result, key) == value, f"Expected {key} to be {value}, got {getattr(result, key)}"

    return result


def wrap_xml(xml_str: str) -> str:
    """Wrap an XML string in a BPMN XML root element."""
    return f"""<root xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">{xml_str}</root>"""


def get_params(params: list[dict[str, Any]]) -> list[Any]:
    """Convert the test cases into parameters for pytest.mark.parametrize."""
    return [param(wrap_xml(item["xml"]), item["attributes"], id=item["name"]) for item in params]


def assert_attributes(obj: Any, attributes: dict[str, Any], parent_path: str = "") -> None:
    """
    Assert that the given object has the given attributes.

    Args:
        obj: The object to check.
        attributes: The expected attributes and their values.
        parent_path: The path to the parent object, used for error messages.
    """
    list_attributes = set()
    nested_attributes = set()

    if attributes is None:
        return

    if isinstance(obj, dict):
        assert_equal(obj, attributes, parent_path)
        return
    print(f"{parent_path}")

    for key, val in attributes.items():
        obj_val = getattr(obj, key, None)
        if isinstance(obj_val, list):
            list_attributes.add(key)
            continue
        elif isinstance(obj_val, dict):
            nested_attributes.add(key)
            continue
        elif is_dataclass(obj_val):
            assert_attributes(obj_val, val, f"{parent_path}.{key}")
            continue
        assert obj_val == val, f"Expected {parent_path}.{key} to be {val}, got {obj_val}"

    for key in list_attributes:
        attr_val = getattr(obj, key)
        for i, item in enumerate(attr_val):
            if len(attributes[key]) <= i:
                print(list_attributes)
                assert False, f"Expected {parent_path}.{key} to have at least {i} items, got {len(attr_val)}"
            assert_attributes(item, attributes[key][i], f"{parent_path}.{key}[{i}]")

    for key in nested_attributes:
        attr_val = getattr(obj, key)
        if isinstance(attr_val, dict):
            assert_equal(attr_val, attributes[key], f"{parent_path}.{key}")
        else:
            assert_attributes(attr_val, attributes[key], f"{parent_path}.{key}")


def assert_equal(actual: Any, expected: Any, path: str = "$") -> None:
    """Recursively assert that two values are equal.

    This helper compares common Python container types and dataclasses, producing
    clear, path-based error messages to pinpoint mismatches.

    Rules:
    - Primitives (None, bool, int, float, str) are compared with ==.
    - Dicts: keys must match exactly; values compared recursively.
    - Lists/Tuples: compared in order; lengths must match.
    - Sets/Frozensets: compared by equality (order-insensitive).
    - Dataclasses: compared field-by-field; supports comparing to dicts
      representing fields.
    """
    from dataclasses import fields, is_dataclass as _is_dataclass

    # Helper to render a path child
    def child(p: str, key: Any) -> str:
        if isinstance(key, int):
            return f"{p}[{key}]"
        # ensure dot separation but avoid double dots at root "$"
        if p == "$":
            return f"{p}.{key}"
        return f"{p}.{key}"

    # Dataclass normalization: compare as mapping of fields
    if _is_dataclass(actual) and _is_dataclass(expected):
        actual = {f.name: getattr(actual, f.name) for f in fields(actual)}
        expected = {f.name: getattr(expected, f.name) for f in fields(expected)}
    elif _is_dataclass(actual) and isinstance(expected, dict):
        actual = {f.name: getattr(actual, f.name) for f in fields(actual)}
    elif _is_dataclass(expected) and isinstance(actual, dict):
        expected = {f.name: getattr(expected, f.name) for f in fields(expected)}

    # Dicts
    if isinstance(actual, dict) and isinstance(expected, dict):
        act_keys = set(actual.keys())
        exp_keys = set(expected.keys())
        assert act_keys == exp_keys, (
            f"Key mismatch at {path}:\n"
            f"  in actual, not in expected: {sorted(act_keys - exp_keys)}\n"
            f"  in expected, not in actual: {sorted(exp_keys - act_keys)}"
        )
        for k in expected:
            assert_equal(actual[k], expected[k], child(path, k))
        return

    # Lists / Tuples (sequence, order-sensitive)
    if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
        assert len(actual) == len(expected), f"Length mismatch at {path}: {len(actual)} != {len(expected)}"
        for i, (a_i, e_i) in enumerate(zip(actual, expected)):
            assert_equal(a_i, e_i, child(path, i))
        return

    # Sets
    if isinstance(actual, (set, frozenset)) and isinstance(expected, (set, frozenset)):
        assert actual == expected, (
            f"Set mismatch at {path}:\n"
            f"  only-in-actual: {sorted(actual - expected)}\n"
            f"  only-in-expected: {sorted(expected - actual)}"
        )
        return

    # Fallback: direct equality
    assert actual == expected, f"Value mismatch at {path}: {actual!r} != {expected!r}"
