"""Tests for the core module."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import pytest

from pybpmn_parser.core import (
    QName,
    _convert,
    _enum_to_primitive,
    convert_dataclass,
    convert_dict,
    dataclass_to_dict,
    default_empty_predicate,
    get_fields_by_metadata,
    index_ids,
)


@dataclass
class ExampleDataClass:
    """Example dataclass for testing."""

    field_one: str = field(metadata={"key": "value1"})
    field_two: int = field(metadata={"key": "value2"})
    field_three: bool = field(metadata={"key": "value1"})
    field_four: float = field(metadata={})


class TestGetFieldsByMetadata:
    """Tests for the get_fields_by_metadata function."""

    def test_empty_dataclass(self):
        """Test function with an empty dataclass."""

        @dataclass
        class EmptyDataClass:
            pass

        result = get_fields_by_metadata(EmptyDataClass(), "key", "value1")
        assert result == {}

    def test_matching_fields(self):
        """Test function when fields match the metadata key-value pair."""
        result = get_fields_by_metadata(ExampleDataClass("one", 2, True, 1.0), "key", "value1")
        assert result == {"field_one": "one", "field_three": True}

    def test_no_matching_fields(self):
        """Test when no fields match the metadata key-value pair."""
        result = get_fields_by_metadata(ExampleDataClass("one", 2, True, 1.0), "key", "nonexistent_value")
        assert result == {}

    def test_no_metadata_key(self):
        """Test when the metadata key does not exist."""
        result = get_fields_by_metadata(ExampleDataClass("one", 2, True, 1.0), "nonexistent_key", "value1")
        assert result == {}

    def test_dataclass_without_metadata(self):
        """Test function for a dataclass with no metadata in its fields."""

        @dataclass
        class NoMetadataDataClass:
            field_one: str
            field_two: int

        result = get_fields_by_metadata(NoMetadataDataClass("one", 2), "key", "value1")
        assert result == {}

    def test_non_dataclass_input(self):
        """Test function when input is not a dataclass."""
        result = get_fields_by_metadata(object, "key", "value1")
        assert result == {}

    def test_partial_metadata_match(self):
        """Test function where some fields have unrelated metadata."""
        result = get_fields_by_metadata(ExampleDataClass("one", 2, True, 1.0), "key", "value2")
        assert result == {"field_two": 2}


class TestQName:
    """Unit tests for QName class."""

    def test_local_with_uri(self):
        """Test string representation of QName with URI."""
        qname = QName(local="name", uri="http://example.com")
        assert str(qname) == "{http://example.com}name"

    def test_local_without_uri(self):
        """Test string representation of QName without URI."""
        qname = QName(local="name")
        assert str(qname) == "name"

    def test_from_str_with_braces(self):
        """Test QName parsing a string with URI braces."""
        qname = QName.from_str("{http://example.com}name")
        expected = QName(local="name", uri="http://example.com")
        assert qname == expected

    def test_from_str_with_prefix(self):
        """Test QName parsing from string with prefix."""
        nsmap = {"ex": "http://example.com"}
        qname = QName.from_str("ex:name", nsmap=nsmap)
        expected = QName(local="name", uri="http://example.com")
        assert qname == expected

    def test_from_str_without_prefix_or_uri(self):
        """Test QName parsing without URI or prefix using a default URI."""
        qname = QName.from_str("name", default_uri="http://example.com")
        expected = QName(local="name", uri="http://example.com")
        assert qname == expected

    def test_from_str_with_undefined_prefix_raises_error(self):
        """Test QName parsing with an undefined prefix raises ValueError."""
        nsmap = {"ex": "http://example.com"}
        with pytest.raises(ValueError, match="Prefix unknown is not defined in the namespace map."):
            QName.from_str("unknown:name", nsmap=nsmap)

    def test_from_str_no_nsmap_or_defaults(self):
        """Test QName parsing without nsmap or defaults and only a local name."""
        qname = QName.from_str("local")
        expected = QName(local="local", uri=None)
        assert qname == expected


class TestDefaultEmptyPredicate:
    """Unit tests for the default_empty_predicate function."""

    def test_none_is_empty(self):
        """Test that None is considered empty."""
        assert default_empty_predicate(None) is True

    def test_empty_string_is_empty(self):
        """Test that an empty string is considered empty."""
        assert default_empty_predicate("") is True

    def test_empty_bytes_is_empty(self):
        """Test that empty bytes are considered empty."""
        assert default_empty_predicate(b"") is True

    def test_empty_list_is_empty(self):
        """Test that an empty list is considered empty."""
        assert default_empty_predicate([]) is True

    def test_empty_dict_is_empty(self):
        """Test that an empty dictionary is considered empty."""
        assert default_empty_predicate({}) is True

    def test_non_empty_string_is_not_empty(self):
        """Test that a non-empty string is not considered empty."""
        assert default_empty_predicate("content") is False

    def test_non_empty_bytes_is_not_empty(self):
        """Test that non-empty bytes are not considered empty."""
        assert default_empty_predicate(b"data") is False

    def test_non_empty_list_is_not_empty(self):
        """Test that a non-empty list is not considered empty."""
        assert default_empty_predicate([1, 2, 3]) is False

    def test_non_empty_dict_is_not_empty(self):
        """Test that a non-empty dictionary is not considered empty."""
        assert default_empty_predicate({"key": "value"}) is False

    def test_zero_not_empty(self):
        """Test that a zero (integer) is not considered empty."""
        assert default_empty_predicate(0) is False

    def test_false_not_empty(self):
        """Test that False is not considered empty."""
        assert default_empty_predicate(False) is False

    def test_empty_custom_object(self):
        """Test that an object with len() == 0 is considered empty."""

        class EmptyObject:
            def __len__(self):
                return 0

        empty_obj = EmptyObject()
        assert default_empty_predicate(empty_obj) is True

    def test_non_empty_custom_object(self):
        """Test that an object with len() > 0 is not considered empty."""

        class NonEmptyObject:
            def __len__(self):
                return 3

        non_empty_obj = NonEmptyObject()
        assert default_empty_predicate(non_empty_obj) is False


class ExampleEnum(Enum):
    """Example Enum for testing."""

    VALUE_ONE = 1
    VALUE_TWO = 2


class TestEnumToPrimitive:
    """Unit tests for the _enum_to_primitive function."""

    def test_enum_to_value(self):
        """Test conversion of Enum to its value."""
        result = _enum_to_primitive(ExampleEnum.VALUE_ONE, "value")
        assert result == 1

    def test_enum_to_name(self):
        """Test conversion of Enum to its name."""
        result = _enum_to_primitive(ExampleEnum.VALUE_ONE, "name")
        assert result == "VALUE_ONE"

    def test_invalid_enum_as_parameter_uses_name(self):
        """Test invalid enum_as parameter uses the name."""
        result = _enum_to_primitive(ExampleEnum.VALUE_ONE, "invalid")
        assert result == "VALUE_ONE"


class TestConvert:
    """Unit tests for the _convert function."""

    def test_convert_enum_value(self):
        """Test converting an Enum to its value."""

        class TestEnum(Enum):
            OPTION_A = 1
            OPTION_B = 2

        assert _convert(TestEnum.OPTION_A, enum_as="value") == 1

    def test_convert_enum_name(self):
        """Test converting an Enum to its name."""

        class TestEnum(Enum):
            OPTION_A = 1
            OPTION_B = 2

        assert _convert(TestEnum.OPTION_A, enum_as="name") == "OPTION_A"

    def test_convert_dataclass(self):
        """Test converting a dataclass to a dictionary."""

        @dataclass
        class TestDataclass:
            field_a: int
            field_b: str

        instance = TestDataclass(field_a=42, field_b="value")
        expected = {"field_a": 42, "field_b": "value"}
        assert _convert(instance) == expected

    def test_convert_dict(self):
        """Test converting a dictionary."""
        data = {
            "key_1": "value_1",
            "key_2": None,
        }
        expected = {
            "key_1": "value_1",
            "key_2": None,
        }
        assert _convert(data) == expected

    def test_convert_dict_skip_empty(self):
        """Test converting a dictionary with skip_empty=True."""
        data = {
            "key_1": "value_1",
            "key_2": "",
            "key_3": None,
        }
        expected = {
            "key_1": "value_1",
        }
        assert _convert(data, skip_empty=True) == expected

    def test_convert_list(self):
        """Test converting a list."""
        data = [1, 2, 3]
        assert _convert(data) == [1, 2, 3]

    def test_convert_list_with_empty_elements(self):
        """Test converting a list with empty elements and skip_empty=True."""
        data = [1, None, "", 3]
        expected = [1, 3]
        assert _convert(data, skip_empty=True) == expected

    def test_convert_object_with_dict(self):
        """Test converting an object with a __dict__ attribute."""

        class TestObject:
            def __init__(self):
                self.attr_1 = "value_1"
                self.attr_2 = "value_2"

        obj = TestObject()
        expected = {"attr_1": "value_1", "attr_2": "value_2"}
        assert _convert(obj) == expected

    def test_convert_with_custom_empty_predicate(self):
        """Test converting with a custom empty predicate."""

        def custom_predicate(value):
            return value == 0  # Treat 0 as empty

        data = {"key": 0}
        expected: dict[str, Any] = {}
        assert _convert(data, skip_empty=True, empty_predicate=custom_predicate) == expected


class TestConvertDict:
    """Unit tests for the convert_dict function."""

    def test_convert_dict_basic(self):
        """Test converting a simple dictionary without skipping empty entries."""
        data = {"key1": "value1", "key2": None}
        expected = {"key1": "value1", "key2": None}
        result = convert_dict(data, empty_predicate=None, enum_as="value", skip_empty=False)
        assert result == expected

    def test_convert_dict_skip_empty(self):
        """Test converting a dictionary with skipping empty entries."""
        data = {"key1": "value1", "key2": None, "key3": ""}
        expected = {"key1": "value1"}
        result = convert_dict(data, empty_predicate=lambda v: v in (None, ""), enum_as="value", skip_empty=True)
        assert result == expected

    def test_convert_dict_with_enum(self):
        """Test converting a dictionary with Enum keys."""

        class Color(Enum):
            RED = 1
            BLUE = 2

        data = {Color.RED: "Red Color", Color.BLUE: "Blue Color"}
        expected = {"RED": "Red Color", "BLUE": "Blue Color"}
        result = convert_dict(data, empty_predicate=None, enum_as="name", skip_empty=False)
        assert result == expected

    def test_convert_dict_nested(self):
        """Test converting a dictionary with nested dictionaries."""
        data = {"key1": {"nested_key": "nested_value"}}
        expected = {"key1": {"nested_key": "nested_value"}}
        result = convert_dict(data, empty_predicate=None, enum_as="value", skip_empty=False)
        assert result == expected

    def test_convert_dict_with_custom_empty_predicate(self):
        """Test converting a dictionary with a custom empty predicate."""
        data = {"key1": 0, "key2": "value2"}
        expected = {"key1": 0, "key2": "value2"}
        result = convert_dict(data, empty_predicate=lambda x: x == "", enum_as="value", skip_empty=True)
        assert result == expected


class TestConvertDataclass:
    """Unit tests for the convert_dataclass function."""

    @dataclass
    class ExampleDataclass:
        """Example dataclass for testing."""

        string_field: str
        int_field: int
        optional_field: str | None = None
        enum_field: Enum | None = None

    class ExampleEnum(Enum):
        """Example Enum for testing."""

        OPTION_ONE = 1
        OPTION_TWO = 2

    def test_basic_conversion(self):
        """Test that a basic dataclass is converted to a dictionary."""
        instance = self.ExampleDataclass(string_field="test", int_field=123)
        expected = {"string_field": "test", "int_field": 123, "optional_field": None, "enum_field": None}
        assert convert_dataclass(instance) == expected

    def test_optional_field_none(self):
        """Test conversion when optional fields are None."""
        instance = self.ExampleDataclass(string_field="value", int_field=42, optional_field=None)
        expected = {"string_field": "value", "int_field": 42, "optional_field": None, "enum_field": None}
        assert convert_dataclass(instance) == expected

    def test_with_enum_field(self):
        """Test conversion of a dataclass with an Enum field."""
        instance = self.ExampleDataclass(
            string_field="enum_test", int_field=100, enum_field=self.ExampleEnum.OPTION_ONE
        )
        expected = {"string_field": "enum_test", "int_field": 100, "optional_field": None, "enum_field": 1}
        assert convert_dataclass(instance) == expected

    def test_enum_as_name(self):
        """Test conversion of a dataclass with enum_as="name"."""
        instance = self.ExampleDataclass(
            string_field="enum_test", int_field=100, enum_field=self.ExampleEnum.OPTION_TWO
        )
        expected = {"string_field": "enum_test", "int_field": 100, "optional_field": None, "enum_field": "OPTION_TWO"}
        assert convert_dataclass(instance, enum_as="name") == expected

    def test_skip_empty_fields(self):
        """Test conversion with skip_empty=True."""
        instance = self.ExampleDataclass(string_field="filled", int_field=456)
        expected = {"string_field": "filled", "int_field": 456}
        assert convert_dataclass(instance, skip_empty=True, empty_predicate=lambda x: x is None) == expected

    def test_with_extra_kwargs(self):
        """Test conversion when the dataclass has extra key-value pairs."""

        @dataclass
        class DataclassWithExtra:
            __extra_kwargs__ = {"extra_key": "extra_value"}
            field_one: str

        instance = DataclassWithExtra(field_one="value")
        expected = {"field_one": "value", "extra_key": "extra_value"}
        assert convert_dataclass(instance) == expected


class TestDataclassToDict:
    """Unit tests for dataclass_to_dict function."""

    @dataclass
    class ExampleDataclass:
        """Example dataclass for testing dataclass_to_dict."""

        name: str
        value: int = 0
        optional_field: str | None = None

    class ExampleEnum(Enum):
        """Example Enum for testing."""

        FIRST = "first"
        SECOND = "second"

    def test_basic_conversion(self, mocker):
        """Test conversion of a simple dataclass."""
        expected = {"name": "Test", "value": 42, "optional_field": None}
        mock_convert = mocker.patch("pybpmn_parser.core._convert", return_value=expected)
        instance = self.ExampleDataclass(name="Test", value=42)

        assert dataclass_to_dict(instance) == expected
        assert mock_convert.call_count == 1

    def test_skip_empty_fields(self, mocker):
        """Test conversion with skip_empty=True."""
        expected = {"name": "SkipTest", "value": 0}
        mock_convert = mocker.patch("pybpmn_parser.core._convert", return_value=expected)
        instance = self.ExampleDataclass(name="SkipTest", optional_field=None)

        assert dataclass_to_dict(instance, skip_empty=True) == expected
        assert mock_convert.call_count == 1
        assert mock_convert.call_args[1]["skip_empty"] is True

    def test_with_enum_value(self, mocker):
        """Test conversion of an Enum field with enum_as='value'."""
        expected = {"enum_field": "first"}
        mock_convert = mocker.patch("pybpmn_parser.core._convert", return_value=expected)
        instance = {"enum_field": self.ExampleEnum.FIRST}

        assert dataclass_to_dict(instance, enum_as="value") == expected
        assert mock_convert.call_count == 1
        assert mock_convert.call_args[1]["enum_as"] == "value"

    def test_with_enum_name(self, mocker):
        """Test conversion of an Enum field with enum_as='name'."""
        expected = {"enum_field": "FIRST"}
        mock_convert = mocker.patch("pybpmn_parser.core._convert", return_value=expected)
        instance = {"enum_field": self.ExampleEnum.FIRST}
        assert dataclass_to_dict(instance, enum_as="name") == expected
        assert mock_convert.call_count == 1
        assert mock_convert.call_args[1]["enum_as"] == "name"

    def test_custom_empty_predicate(self, mocker):
        """Test conversion with a custom empty predicate."""

        def custom_predicate(value):
            return value == ""

        expected = {"name": "CustomTest", "value": 42}
        mock_convert = mocker.patch("pybpmn_parser.core._convert", return_value=expected)
        instance = self.ExampleDataclass(name="CustomTest", value=42, optional_field="")

        assert dataclass_to_dict(instance, skip_empty=True, empty_predicate=custom_predicate) == expected

        assert mock_convert.call_count == 1
        assert mock_convert.call_args[1]["skip_empty"] is True
        assert mock_convert.call_args[1]["empty_predicate"] == custom_predicate


@dataclass
class ExampleElement:
    id: str
    value: Any


@dataclass
class ExampleContainer:
    elements: list[ExampleElement] = field(default_factory=list)


class TestIndexIds:
    """Unit tests for the index_ids function."""

    def test_non_dataclass_returns_empty_dict(self):
        """Test that an object not being a dataclass returns an empty dictionary."""
        result = index_ids({"id": "123", "value": "test"})
        assert result == {}

    def test_missing_id_returns_empty_dict(self):
        """Test that an empty dataclass returns an empty dictionary."""

        @dataclass
        class EmptyDataclass:
            pass

        empty_instance = EmptyDataclass()
        result = index_ids(empty_instance)
        assert result == {}

    def test_single_element(self):
        """Test that a dataclass with a single element maps correctly."""
        element = ExampleElement(id="123", value="test")
        result = index_ids(element)
        assert result == {"123": element}

    def test_list_of_elements(self):
        """Test indexing with a list of elements within a container dataclass."""
        elements = [ExampleElement(id="1", value="A"), ExampleElement(id="2", value="B")]
        container = ExampleContainer(elements=elements)
        result = index_ids(container)
        assert result == {"1": elements[0], "2": elements[1]}

    def test_nested_elements(self):
        """Test indexing with nested dataclasses."""
        nested_element = ExampleElement(id="nested", value="nested_value")
        parent_element = ExampleContainer(elements=[nested_element])
        result = index_ids(parent_element)
        assert result == {"nested": nested_element}

    def test_element_without_id(self):
        """Test indexing ignores objects without an ID attribute."""

        @dataclass
        class ElementWithoutId:
            value: str

        obj = ElementWithoutId(value="no_id")
        result = index_ids(obj)
        assert result == {}

    def test_mixed_container(self):
        """Test indexing with a mix of elements (with and without IDs)."""

        @dataclass
        class MixedDataclass:
            list_with_id: list[ExampleElement] = field(default_factory=list)
            list_without_id: list[Any] = field(default_factory=list)

        obj = MixedDataclass(list_with_id=[ExampleElement(id="abc", value="has_id")], list_without_id=["no_id"])
        result = index_ids(obj)
        assert result == {"abc": obj.list_with_id[0]}

    def test_update_behavior(self):
        """Test that indexing works correctly when called recursively."""
        nested_1 = ExampleElement(id="nested1", value="value1")
        nested_2 = ExampleElement(id="nested2", value="value2")
        container = ExampleContainer(elements=[nested_1, nested_2])
        result = index_ids(container)
        assert result == {"nested1": nested_1, "nested2": nested_2}
