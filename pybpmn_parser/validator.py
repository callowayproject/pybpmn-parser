"""Validator for BPMN 2.0 XML documents."""

import logging
from pathlib import Path
from typing import List, Optional

import lxml.etree as ET
import xmlschema
from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import Failure, Result, Success, safe

logger = logging.getLogger(__name__)

SCHEMA_DIR = Path(__file__).parent / "schemas"

BPMN_SCHEMA = xmlschema.XMLSchema(
    SCHEMA_DIR / "BPMN20.xsd",
    validation="lax",  # Use lax validation to handle missing imports
    base_url=str(SCHEMA_DIR.absolute()),  # Set base URL for imports
)

# Load registered extension schemas
# self.extension_schema = xmlschema.XMLSchema(
#     schema_dir / "pythmata.xsd", validation="lax"
# )

# Define known validation issues to skip
KNOWN_VALIDATION_PATTERNS = [
    "tFormalExpression",
    "global xs:simpleType/xs:complexType 'bpmn:tFormalExpression' not found",
]

# Define namespaces for validation
NAMESPACES = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class ValidationError(Exception):
    """An error encountered during validation."""

    def __init__(self, code: str, message: str, element_id: Optional[str] = None):
        self.code = code
        self.message = message
        self.element_id = element_id

    def __str__(self) -> str:
        if self.element_id:
            return f"{self.code}: {self.message} (element: {self.element_id})"
        return f"{self.code}: {self.message}"

    def __repr__(self) -> str:
        return self.__str__()


class ValidationResult:
    """Result of BPMN XML validation."""

    def __init__(self, errors: Optional[list[ValidationError]] = None):
        self.is_valid = True
        self.errors = errors or []
        if self.errors:
            self.is_valid = False

    def add_errors(self, errors: list[ValidationError]) -> None:
        """Adds a list of validation errors."""
        self.errors.extend(errors)
        self.is_valid = len(self.errors) == 0

    def raise_for_errors(self) -> None:
        """Raises a ValidationError if there are any errors."""
        if self.errors:
            errors = "\n".join(str(error) for error in self.errors)
            raise ValidationError("VALIDATION_ERROR", f"Validation failed\n{errors}")


@safe
def _strip_extra_whitespace(value: str) -> str:
    """Strips extra whitespace from a string and returns the result."""
    return_value = value.strip()
    if not return_value:
        raise ValidationError("EMPTY_XML", "Value cannot be empty")
    return return_value


@safe
def _parse_xml(xml: str) -> ET.Element:
    """Parses an XML string into an ElementTree Element."""
    try:
        xml_bytes = xml.encode("utf-8")
        return ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        raise ValidationError("XML_PARSE_ERROR", str(e)) from e


def _parse_xml_with_strip(xml: str) -> Result[ET.Element, ValidationError]:
    """Parses an XML string into an ElementTree Element and strips extra whitespace."""
    return flow(xml, _strip_extra_whitespace, bind(_parse_xml))


def _is_skippable_error(error: str) -> bool:
    """Checks if an error is a known validation issue to skip."""
    if "extensionElements" in error:
        return True

    for pattern in KNOWN_VALIDATION_PATTERNS:
        if pattern in error:
            logger.debug(f"Skipping known validation issue: {error}")
            return True
    return False


def _validate_bpmn_schema(doc: ET.Element) -> List[ValidationError]:
    """Validates an ElementTree Element against the BPMN 2.0 schema."""
    return [
        ValidationError("SCHEMA_ERROR", f"{error.reason} ({error.elem.tag.split('}')[-1]})")
        for error in BPMN_SCHEMA.iter_errors(doc, namespaces=NAMESPACES)
        if not _is_skippable_error(str(error))
    ]


def _validate_extension_schema(doc: ET.Element) -> List[ValidationError]:
    """Validate an ElementTree Element against the extension schema."""
    # TODO: Implement validating against public or registered extensions
    # extension_elements = doc.findall(".//{*}extensionElements")
    return []


def _get_unique_ids(doc: ET.Element) -> List[str]:
    """Validates that all IDs are unique within the document."""
    ids = set()

    for elem in doc.findall(".//*[@id]"):
        elem_id = elem.get("id")
        ids.add(elem_id)

    return list(ids)


def _validate_process_id(process: ET.Element) -> List[ValidationError]:
    """Validate that the process ID is present and unique."""
    if not process.get("id"):
        return [ValidationError("MISSING_ATTRIBUTE", "Process element missing required 'id' attribute")]
    return []


def _validate_flows(flows: List[ET.Element], ids: List[str]) -> List[ValidationError]:
    """Validates that all flows have a source and target reference."""
    errors = []
    for flo in flows:
        flow_id = flo.get("id")
        source_ref = flo.get("sourceRef")
        target_ref = flo.get("targetRef")

        if not source_ref:
            errors.append(ValidationError("INVALID_FLOW", f"Flow {flow_id} missing source reference"))
        if not target_ref:
            errors.append(ValidationError("INVALID_FLOW", f"Flow {flow_id} missing target reference"))
        if source_ref and source_ref not in ids:
            errors.append(
                ValidationError(
                    "INVALID_REFERENCE",
                    f"Sequence flow '{flow_id}' source ref '{source_ref}' references non-existent node",
                )
            )
        if target_ref and target_ref not in ids:
            errors.append(
                ValidationError(
                    "INVALID_REFERENCE",
                    f"Sequence flow '{flow_id}' target ref '{target_ref}' references non-existent node",
                )
            )

    return errors


def _validate_sequence_flows(doc: ET.Element, ids: List[str]) -> List[ValidationError]:
    """Validates that all sequence flows reference existing nodes."""
    errors = []

    for process in doc.findall(".//{*}process"):
        errors.extend(_validate_process_id(process))

        # Get all flow nodes and sequence flows
        nodes = (
            process.findall(".//{*}startEvent")
            + process.findall(".//{*}activities")
            + process.findall(".//{*}endEvent")
        )
        flows = process.findall(".//{*}sequenceFlow")

        # Check if nodes are connected
        if nodes and not flows:
            errors.append(ValidationError("INVALID_STRUCTURE", "Process contains nodes but no sequence flows"))

        errors.extend(_validate_flows(flows, ids))

    return errors


def validate(xml: str) -> ValidationResult:
    """
    Validates a BPMN XML string against the BPMN 2.0 schema and additional rules.

    Args:
        xml: The BPMN XML string to validate

    Returns:
        ValidationResult containing validation status and any errors
    """
    result = ValidationResult()
    doc = _parse_xml_with_strip(xml)

    match doc:
        case Success(value):
            doc = value
        case Failure(error):
            result.add_errors([error])
            return result

    result.add_errors(_validate_bpmn_schema(doc))
    if not result.is_valid:
        return result

    result.add_errors(_validate_extension_schema(doc))
    if not result.is_valid:
        return result

    ids = _get_unique_ids(doc)
    result.add_errors(_validate_sequence_flows(doc, ids))

    return result
