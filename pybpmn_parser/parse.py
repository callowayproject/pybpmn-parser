"""Parse a BPMN file."""

from pathlib import Path

import lxml.etree as ET

from pybpmn_parser.bpmn.infrastructure.definitions import Definitions
from pybpmn_parser.validator import validate


def parse_file(xml_file: Path) -> Definitions:
    """
    Parse a BPMN XML file into internal representation.

    Args:
        xml_file: The path to a BPMN XML file

    Returns:
        Definitions object
    """
    xml = xml_file.read_text(encoding="utf-8")
    return parse(xml)


def parse(xml_str: str) -> Definitions:
    """
    Parse a BPMN XML string into internal representation.

    Args:
        xml_str: A BPMN XML string

    Returns:
        Dictionary containing parsed nodes and flows
    """
    # Validate XML first
    validation_result = validate(xml_str)
    for error in validation_result.errors:
        print(error)
    validation_result.raise_for_errors()

    # Parse root element
    root: ET.Element = ET.fromstring(xml_str.encode("utf-8"))
    return Definitions.parse(root)
