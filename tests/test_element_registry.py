"""Tests for the element_registry module."""

from dataclasses import dataclass, field
from types import NoneType
from typing import Dict, List, Optional, Union

import pytest
from typing_extensions import type_repr

from pybpmn_parser.core import QName
from pybpmn_parser.element_registry import (
    ElementDescriptor,
    ElementProperty,
    dataclass_fields,
    descriptor_from_class,
    get_base_type,
    type_hint_to_property,
)


class TestGetBaseType:
    """Unit tests for the get_base_type function."""

    def test_base_type_simple(self):
        """Test extracting the base type from a simple type."""
        result = get_base_type(str)
        assert result is str

    def test_base_type_optional(self):
        """Test extracting the base type from an Optional type."""
        result = get_base_type(Optional[str])
        assert result is str

    def test_base_type_list(self):
        """Test extracting the base type from a list type."""
        result = get_base_type(List[int])
        assert result is int

    def test_base_type_list_of_dict(self):
        """Test extracting the base type from a list of dictionaries."""
        result = get_base_type(List[Dict[str, int]])
        assert result is dict

    def test_base_type_union(self):
        """Test extracting the base type from a Union type."""
        with pytest.raises(ValueError, match="Cannot handle multiple types in Union:"):
            get_base_type(Union[int, float])

    def test_base_type_empty_union(self):
        """Test extracting the base type from a Union with no types."""
        result = get_base_type(Union[None])
        assert result is NoneType

    def test_base_type_complex_optional_union(self):
        """Test extracting base type from a complex Optional Union."""
        with pytest.raises(ValueError, match="Cannot handle multiple types in Union:"):
            get_base_type(Optional[Union[List[int], List[str]]])


class TestDataclassFields:
    """Unit tests for dataclass_fields function."""

    @dataclass
    class ExampleDataClass:
        """Example dataclass for testing."""

        field_one: int = field(metadata={"key1": "value1", "key2": "value2"})
        field_two: str = field(metadata={"key1": "value3"})
        field_three: bool = field(metadata={})

    def test_return_type(self):
        """Test that the function returns a dictionary."""
        result = dataclass_fields(self.ExampleDataClass)
        assert isinstance(result, dict)

    def test_field_metadata_extraction(self):
        """Test that metadata is extracted correctly for each field."""
        expected = {
            "field_one": {"key1": "value1", "key2": "value2"},
            "field_two": {"key1": "value3"},
            "field_three": {},
        }
        result = dataclass_fields(self.ExampleDataClass)
        assert expected == result

    def test_empty_dataclass(self):
        """Test with an empty dataclass."""

        @dataclass
        class EmptyDataClass:
            pass

        result = dataclass_fields(EmptyDataClass)
        assert result == {}

    def test_no_metadata(self):
        """Test with a dataclass that has no metadata."""

        @dataclass
        class NoMetadataDataClass:
            field_one: int
            field_two: str

        result = dataclass_fields(NoMetadataDataClass)
        expected = {"field_one": {}, "field_two": {}}
        assert expected == result


class TestTypeHintToProperty:
    """Unit tests for the type_hint_to_property function."""

    @dataclass
    class ExampleDataClass:
        """Example dataclass for testing."""

        class Meta:
            namespace = "http://example.com"
            name = "exampleDataClass"

        field_one: int = field(metadata={"name": "fieldOne", "key2": "value2"})
        field_two: Optional[str] = field(metadata={"name": "fieldTwo"})
        field_three: bool = field(metadata={})

    def test_create_element_property_with_simple_type(self):
        """Test creating an ElementProperty with a simple type."""
        name = "field_one"
        type_hint = int
        metadata = {"name": "fieldOne", "type": "Element", "namespace": "http://example.com"}
        result = type_hint_to_property(name, type_hint, metadata)

        assert isinstance(result, ElementProperty)
        assert result.property_name == "field_one"
        assert result.type == type_repr(int)
        assert result.type_qname is None
        assert result.is_attr is False
        assert result.is_optional is False
        assert result.is_many is False

    def test_create_element_property_with_optional(self):
        """Test creating an ElementProperty with an optional type."""
        type_hint = Optional[str]
        field_metadata = {"name": "fieldTwo", "type": "Element"}
        name = "field_two"

        result = type_hint_to_property(name, type_hint, field_metadata)

        assert isinstance(result, ElementProperty)
        assert result.property_name == "field_two"
        assert result.type == type_repr(str)
        assert result.is_optional is True

    def test_create_element_property_with_attribute_type(self):
        """Test creating an ElementProperty marked as an attribute."""
        type_hint = int
        field_metadata = {"type": "Attribute"}
        name = "attribute_field"

        result = type_hint_to_property(name, type_hint, field_metadata)

        assert isinstance(result, ElementProperty)
        assert result.property_name == "attribute_field"
        assert result.type == type_repr(int)
        assert result.is_attr is True
        assert result.is_optional is False

    def test_create_element_property_with_qname(self, mocker):
        """Test creating an ElementProperty with QName metadata."""
        type_hint = self.ExampleDataClass
        field_metadata = {"type": "Element"}
        name = "qname_field"

        result = type_hint_to_property(name, type_hint, field_metadata)

        assert isinstance(result, ElementProperty)
        assert result.property_name == "qname_field"
        assert result.type_qname == QName(uri="http://example.com", local="exampleDataClass")


class TestDescriptorFromClass:
    """Unit tests for descriptor_from_class function."""

    @dataclass
    class ExampleElement:
        """Example element class to test descriptor_from_class."""

        class Meta:
            name = "ExampleElement"
            namespace = "http://example.com"

        attr_one: int = field(metadata={"name": "attributeOne", "type": "Attribute"})
        element_one: str = field(metadata={"name": "elementOne", "type": "Element"})
        optional_attr: Optional[float] = field(metadata={"name": "optionalAttribute", "type": "Attribute"})

    def test_descriptor_type_and_name(self):
        """Test that the descriptor has the correct type and name."""
        descriptor = descriptor_from_class(self.ExampleElement)
        assert isinstance(descriptor, ElementDescriptor)
        assert descriptor.type is self.ExampleElement
        assert descriptor.name == "ExampleElement"

    def test_descriptor_qname(self):
        """Test that the QName is correctly set in the descriptor."""
        descriptor = descriptor_from_class(self.ExampleElement)
        expected_qname = QName(uri="http://example.com", local="ExampleElement")
        assert descriptor.q_name == expected_qname

    def test_descriptor_properties(self):
        """Test that properties are correctly set in the descriptor."""
        descriptor = descriptor_from_class(self.ExampleElement)
        expected_properties = {
            QName(uri="http://example.com", local="attributeOne"): {
                "property_name": "attr_one",
                "type": "int",
                "is_attr": True,
                "is_optional": False,
                "is_many": False,
            },
            QName(uri="http://example.com", local="elementOne"): {
                "property_name": "element_one",
                "type": "str",
                "is_attr": False,
                "is_optional": False,
                "is_many": False,
            },
            QName(uri="http://example.com", local="optionalAttribute"): {
                "property_name": "optional_attr",
                "type": "float",
                "is_attr": True,
                "is_optional": True,
                "is_many": False,
            },
        }
        for key, prop in expected_properties.items():
            assert key in descriptor.properties
            element_property = descriptor.properties[key]
            assert element_property.property_name == prop["property_name"]
            assert element_property.type == prop["type"]
            assert element_property.is_attr == prop["is_attr"]
            assert element_property.is_optional == prop["is_optional"]
            assert element_property.is_many == prop["is_many"]

    def test_descriptor_no_metadata(self):
        """Test descriptor creation for a class with no metadata."""

        @dataclass
        class NoMetadataElement:
            class Meta:
                name = "NoMetadata"
                namespace = "http://example.org"

            field_one: int

        descriptor = descriptor_from_class(NoMetadataElement)
        assert len(descriptor.properties) == 1
        assert QName(uri="http://example.org", local="field_one") in descriptor.properties
