"""Tests for the core module."""

from dataclasses import dataclass, field

from pybpmn_parser.core import get_fields_by_metadata


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
