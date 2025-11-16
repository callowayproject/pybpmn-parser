"""Unit tests for the parse function in the parse module."""

from pathlib import Path

import pytest

from pybpmn_parser.parse import Parser
from pybpmn_parser.validator import ValidationError


class TestParser:
    """Unit tests for the Parser class in the parse module."""

    def test_instantiate_with_nsmap(self):
        """The Parser class can be instantiated with a custom namespace map."""
        ns_map = {"test": "http://example.com"}
        parser = Parser(ns_map=ns_map)
        assert parser.ns_map["test"] == ns_map["test"]

    def test_instantiate_with_moddle_extension(self, mocker):
        """The Parser class can be instantiated with a custom Moddle extension."""
        moddle_extension = Path("moddle_extension.json")
        mock_load_moddle_file = mocker.patch("pybpmn_parser.parse.load_moddle_file", return_value=None)

        Parser(moddle_extensions=[moddle_extension])

        assert mock_load_moddle_file.call_count == 1

    def test_valid_bpmn_returns_definitions(self):
        """The parse function with a valid BPMN XML string returns a Definitions object."""
        xml_str = """<?xml version="1.0" encoding="UTF-8"?>
        <bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" targetNamespace="http://bpmn.io/schema/bpmn">
            <bpmn:process id="Process_1" />
        </bpmn:definitions>
        """
        parser = Parser()
        result = parser.parse_string(xml_str)
        assert result.__class__.__name__ == "Definitions"
        assert len(result.processes) == 1
        assert result.processes[0].id == "Process_1"

    def test_invalid_bpmn_raises_validation_error(self):
        """Test parse function with an invalid BPMN XML string."""
        invalid_xml = """<?xml version="1.0"?>
        <bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" targetNamespace="http://bpmn.io/schema/bpmn">
            <bpmn:invalidTag />
        </bpmn:definitions>
        """
        expected_error_message = (
            "VALIDATION_ERROR: Validation failed\n"
            "SCHEMA_ERROR: Unexpected child with tag 'bpmn:invalidTag' at position 1."
        )
        parser = Parser()

        with pytest.raises(ValidationError, match=expected_error_message):
            parser.parse_string(invalid_xml)

    def test_empty_string_raises_validation_error(self):
        """Parsing an empty string raises a ValidationError."""
        parser = Parser()

        with pytest.raises(ValidationError, match="EMPTY_XML: Value cannot be empty"):
            parser.parse_string("")

    def test_parse_non_bpmn_xml_raises_validation_error(self):
        """Parsing valid XML not conforming to BPMN raises a ValidationError."""
        xml_str = """<?xml version="1.0"?>
        <root>
            <child>Some content</child>
        </root>
        """
        expected_error_message = (
            "VALIDATION_ERROR: Validation failed\nSCHEMA_ERROR: 'root' is not an element of the schema"
        )
        parser = Parser()
        with pytest.raises(ValidationError, match=expected_error_message):
            parser.parse_string(xml_str)


class TestParseFile:
    """Unit tests for the parse_file function in the parse module."""

    def test_can_parse_existing_valid_file(self, fixture_dir: Path):
        """Parsing a valid BPMN file should return a Definitions object."""
        parser = Parser()
        result = parser.parse_file(fixture_dir / "kitchen-sink.bpmn")
        assert result.__class__.__name__ == "Definitions"

    def test_missing_file_raises_file_not_found_error(self, fixture_dir: Path):
        """Parsing a non-existent file should raise a FileNotFoundError."""
        parser = Parser()
        non_existent_file = fixture_dir / "non_existent.bpmn"
        with pytest.raises(FileNotFoundError):
            parser.parse_file(non_existent_file)
