"""Unit tests for the validator module."""

import lxml.etree as ET  # noqa: N812

from pybpmn_parser.validator import (
    ValidationError,
    _get_unique_ids,
    _is_skippable_error,
    _parse_xml,
    _strip_extra_whitespace,
    _validate_flows,
    validate,
)


class TestStripExtraWhitespace:
    """Unit tests for _strip_extra_whitespace function."""

    def test_strip_valid_whitespace(self):
        """Test that excess whitespace is stripped correctly."""
        result = _strip_extra_whitespace("  example text  ").unwrap()
        assert result == "example text"

    def test_strip_empty_string(self):
        """Test that an empty string raises the correct ValidationError."""
        result = _strip_extra_whitespace("").failure()
        assert isinstance(result, ValidationError)
        assert result.code == "EMPTY_XML"
        assert result.message == "Value cannot be empty"

    def test_strip_whitespace_only(self):
        """Test that a string with only spaces raises the correct ValidationError."""
        result = _strip_extra_whitespace("      ").failure()
        assert isinstance(result, ValidationError)
        assert result.code == "EMPTY_XML"
        assert result.message == "Value cannot be empty"

    def test_strip_no_change(self):
        """Test that a string with no extra whitespace is returned unchanged."""
        result = _strip_extra_whitespace("test").unwrap()
        assert result == "test"


class TestParseXML:
    """Unit tests for _parse_xml function."""

    def test_parse_valid_xml(self):
        """Test that a valid XML string is parsed correctly."""
        valid_xml = "<root><child>Content</child></root>"
        result = _parse_xml(valid_xml).unwrap()
        assert result.tag == "root"
        assert len(result) == 1
        assert result[0].tag == "child"
        assert result[0].text == "Content"

    def test_parse_malformed_xml(self):
        """Test that a malformed XML string raises ValidationError."""
        malformed_xml = "<root><child>Content</child>"
        result = _parse_xml(malformed_xml).failure()
        assert isinstance(result, ValidationError)
        assert result.code == "XML_PARSE_ERROR"

    def test_parse_empty_string(self):
        """Test that an empty XML string raises ValidationError."""
        empty_xml = ""
        result = _parse_xml(empty_xml).failure()
        assert isinstance(result, ValidationError)
        assert result.code == "XML_PARSE_ERROR"

    def test_parses_with_utf_8_header(self):
        """Test that an XML string with UTF-8 header is parsed correctly."""
        utf_8_header_xml = "<?xml version='1.0' encoding='UTF-8'?>\n<root><child>Content</child></root>"
        result = _parse_xml(utf_8_header_xml).unwrap()
        assert result.tag == "root"
        assert len(result) == 1
        assert result[0].tag == "child"
        assert result[0].text == "Content"


class TestValidateUniqueIds:
    """Unit tests for _validate_unique_ids function."""

    def test_unique_ids_passes(self):
        """Test that a document with unique IDs passes the validation."""
        xml = """<root>
                    <element id="id1"/>
                    <element id="id2"/>
                </root>"""
        doc = ET.fromstring(xml)
        result = _get_unique_ids(doc)
        assert set(result) == {"id1", "id2"}

    def test_duplicate_ids_are_deduplicated(self):
        """Test that a document with duplicate IDs returns only one ID per element."""
        xml = """<root>
                    <element id="id1"/>
                    <element id="id1"/>
                </root>"""
        doc = ET.fromstring(xml)
        result = _get_unique_ids(doc)
        assert result == ["id1"]

    def test_no_ids_passes_with_empty_list(self):
        """Test that a document with no IDs passes the validation."""
        xml = """<root>
                    <element/>
                    <element/>
                </root>"""
        doc = ET.fromstring(xml)
        result = _get_unique_ids(doc)
        assert result == []


class TestIsSkippableError:
    """Unit tests for _is_skippable_error function."""

    def test_is_skippable_error_extension_elements(self):
        """
        Test that errors containing 'extensionElements' are recognized as skippable.
        """
        error_message = "Something about extensionElements"
        result = _is_skippable_error(error_message)
        assert result is True

    def test_is_skippable_error_known_pattern(self, mocker):
        """
        Test that errors matching a known pattern are recognized as skippable.
        """
        mocker.patch("pybpmn_parser.validator.KNOWN_VALIDATION_PATTERNS", ["KnownPattern"])
        error_message = "This contains KnownPattern"
        result = _is_skippable_error(error_message)
        assert result is True

    def test_is_skippable_error_unknown_pattern(self, mocker):
        """
        Test that errors not matching a known pattern or 'extensionElements' are not skippable.
        """
        mocker.patch("pybpmn_parser.validator.KNOWN_VALIDATION_PATTERNS", ["KnownPattern"])
        error_message = "This is not skippable"
        result = _is_skippable_error(error_message)
        assert result is False


class TestValidateFlows:
    """Unit tests for validate_flows function."""

    def test_valid_references(self):
        """
        Test that _validate_flows passes when all flows have valid source and target references.
        """
        flows_xml = """<root>
            <flow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_1" />
            <flow id="Flow_2" sourceRef="Task_1" targetRef="EndEvent_1" />
        </root>"""
        elements_xml = """<root>
            <node id="StartEvent_1" />
            <node id="Task_1" />
            <node id="EndEvent_1" />
        </root>"""

        flows = ET.fromstring(flows_xml).findall("flow")
        elements = ET.fromstring(elements_xml).findall("node")
        ids = [el.get("id") for el in elements]

        errors = _validate_flows(flows, ids)

        assert len(errors) == 0, f"Unexpected errors: {errors}"

    def test_raises_error_when_missing_source_reference(self):
        """
        Test that _validate_flows detects missing source reference in a flow.
        """
        flows_xml = """<root>
            <flow id="Flow_1" targetRef="Task_1" />
        </root>"""
        elements_xml = """<root>
            <node id="Task_1" />
        </root>"""

        flows = ET.fromstring(flows_xml).findall("flow")
        elements = ET.fromstring(elements_xml).findall("node")
        ids = [el.get("id") for el in elements]

        errors = _validate_flows(flows, ids)

        assert len(errors) == 1
        assert errors[0].code == "INVALID_FLOW"
        assert errors[0].message == "Flow Flow_1 missing source reference"

    def test_raises_error_with_invalid_target_reference(self):
        """
        Test that _validate_flows detects invalid target reference in a flow.
        """
        flows_xml = """<root>
            <flow id="Flow_1" sourceRef="StartEvent_1" targetRef="InvalidNode_1" />
        </root>"""
        elements_xml = """<root>
            <node id="StartEvent_1" />
        </root>"""

        flows = ET.fromstring(flows_xml).findall("flow")
        elements = ET.fromstring(elements_xml).findall("node")
        ids = [el.get("id") for el in elements]

        errors = _validate_flows(flows, ids)

        assert len(errors) == 1
        assert errors[0].code == "INVALID_REFERENCE"
        assert errors[0].message == "Sequence flow 'Flow_1' target ref 'InvalidNode_1' references non-existent node"

    def test_raises_error_when_missing_flow_id(self):
        """
        Test that _validate_flows gracefully handles flows without an ID.
        """
        flows_xml = """<root>
            <flow sourceRef="StartEvent_1" targetRef="Task_1" />
        </root>"""
        elements_xml = """<root>
            <node id="StartEvent_1" />
            <node id="Task_1" />
        </root>"""

        flows = ET.fromstring(flows_xml).findall("flow")
        elements = ET.fromstring(elements_xml).findall("node")
        ids = [el.get("id") for el in elements]

        errors = _validate_flows(flows, ids)

        assert len(errors) == 0, "Flows without an ID should not cause errors"

    def test_captures_multiple_errors(self):
        """
        Test that _validate_flows captures multiple errors in the same flow.
        """
        flows_xml = """<root>
            <flow id="Flow_1" sourceRef="NonExistent_1" />
        </root>"""
        elements_xml = """<root>
            <node id="Task_1" />
        </root>"""

        flows = ET.fromstring(flows_xml).findall("flow")
        elements = ET.fromstring(elements_xml).findall("node")
        ids = [el.get("id") for el in elements]

        errors = _validate_flows(flows, ids)

        assert len(errors) == 2
        import pprint

        pprint.pprint(errors)
        assert errors[0].code == "INVALID_FLOW"
        assert errors[0].message == "Flow Flow_1 missing target reference"
        assert errors[1].code == "INVALID_REFERENCE"
        assert "source ref 'NonExistent_1'" in errors[1].message


class TestValidate:
    """Unit tests for validate function."""

    def test_validates_valid_xml(self):
        """
        Test validation of a basic BPMN process with start event, activities, and end event.
        """
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <bpmn:definitions
            xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
            xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
            xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
            xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
            targetNamespace="http://example.org/bpmn">
            <bpmn:process id="Process_1">
                <bpmn:startEvent id="Start_1"/>
                <bpmn:task id="Task_1"/>
                <bpmn:endEvent id="End_1"/>
                <bpmn:sequenceFlow id="Flow_1" sourceRef="Start_1" targetRef="Task_1"/>
                <bpmn:sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="End_1"/>
            </bpmn:process>
        </bpmn:definitions>
        """
        result = validate(xml)

        if not result.is_valid:
            print(result.errors)
        assert result.is_valid
        assert len(result.errors) == 0

    def test_raises_error_on_duplicate_ids(self):
        """
        The validator should raise an error if the XML contains duplicate IDs.
        """
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <bpmn:definitions
            xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
            xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
            xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
            xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
            targetNamespace="http://example.org/bpmn">
            <bpmn:process id="Process_1">
                <bpmn:startEvent id="id1234"/>
                <bpmn:task id="id1234"/>
                <bpmn:endEvent id="id12345"/>
                <bpmn:sequenceFlow id="Flow_1" sourceRef="id1234" targetRef="id1234"/>
                <bpmn:sequenceFlow id="Flow_2" sourceRef="id1234" targetRef="id12345"/>
            </bpmn:process>
        </bpmn:definitions>
        """
        result = validate(xml)

        assert not result.is_valid
        assert len(result.errors) == 1
        assert result.errors[0].code == "SCHEMA_ERROR"
        assert "attribute id='id1234': duplicated xs:ID value 'id1234'" in result.errors[0].message

    def test_raises_error_on_invalid_structure(self):
        """
        Test validation of a BPMN process with an invalid structure (missing sequence flow).
        """
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <bpmn:definitions
            xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
            xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
            xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
            xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
            targetNamespace="http://example.org/bpmn">
            <bpmn:process id="Process_1">
                <bpmn:startEvent id="Start_1"/>
                <bpmn:task id="Task_1"/>
                <!-- Missing sequence flow -->
            </bpmn:process>
        </bpmn:definitions>
        """
        result = validate(xml)

        assert not result.is_valid
        assert len(result.errors) == 1
        assert result.errors[0].code == "INVALID_STRUCTURE"
        assert result.errors[0].message == "Process contains nodes but no sequence flows"

    def test_raises_error_on_invalid_schema(self):
        """
        Test validation of a BPMN process with an invalid schema (missing sequence flow).
        """
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <bpmn:definitions
            xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
            xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
            xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
            xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
            targetNamespace="http://example.org/bpmn">
            <bpmn:startEvent id="Start_1"/>
            <bpmn:process id="Process_1">
                <bpmn:startEvent id="Start_1"/>
                <bpmn:activities id="Task_1"/>
                <!-- Missing sequence flow -->
            </bpmn:process>
        </bpmn:definitions>
        """
        result = validate(xml)

        assert not result.is_valid
        assert len(result.errors) == 4
        assert result.errors[0].code == "SCHEMA_ERROR"
        assert "XsdComplexType(name='tRootElement') is abstract" in result.errors[0].message
        assert result.errors[1].code == "SCHEMA_ERROR"
        assert "Unexpected child with tag 'bpmn:startEvent' at position 1." in result.errors[1].message
        assert result.errors[2].code == "SCHEMA_ERROR"
        assert "Unexpected child with tag 'bpmn:activities' at position 2" in result.errors[2].message
        assert result.errors[3].code == "SCHEMA_ERROR"
        assert "Unexpected child with tag 'bpmn:startEvent' at position 1." in result.errors[3].message

    def test_raises_error_on_missing_attributes(self):
        """
        Test validation of BPMN elements with missing required attributes.
        """
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <bpmn:definitions
            xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
            xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
            xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
            xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
            targetNamespace="http://example.org/bpmn">
            <bpmn:process>  <!-- Missing required id attribute -->
                <bpmn:startEvent id="Start_1"/>
                <bpmn:endEvent id="End_1"/>
                <bpmn:sequenceFlow id="SequenceFlow_1" sourceRef="Start_1" targetRef="End_1" />
            </bpmn:process>
        </bpmn:definitions>
        """
        result = validate(xml)

        assert not result.is_valid
        assert len(result.errors) == 1
        assert result.errors[0].code == "MISSING_ATTRIBUTE"
        assert result.errors[0].message == "Process element missing required 'id' attribute"

    def test_raises_error_with_bad_xml(self):
        """The validator should raise an error if the XML is invalid."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <bpmn:definitions
            xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
            xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
            xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
            xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
            targetNamespace="http://example.org/bpmn">"""

        result = validate(xml)
        assert not result.is_valid
        assert len(result.errors) == 1
        assert result.errors[0].code == "XML_PARSE_ERROR"
        assert "Premature end of data in tag definitions" in result.errors[0].message
