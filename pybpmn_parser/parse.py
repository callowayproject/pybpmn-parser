"""Parse a BPMN file."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import xmltodict

from pybpmn_parser.bpmn.infrastructure.definitions import Definitions
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import ElementDescriptor
from pybpmn_parser.plugins import load_default_plugins
from pybpmn_parser.plugins.moddle import convert_moddle_registry, load_moddle_file
from pybpmn_parser.validator import validate


class ParseResult:
    """Result for parsing a BPMN file."""

    def __init__(self, definitions: Definitions, context: "ParseContext") -> None:
        self.definition = definitions
        self.elements_by_id: dict[str, ElementDescriptor] = context.elements_by_id
        self.references: list[Reference] = context.references


@dataclass
class Reference:
    """A reference to an element that has not been fully processed yet."""

    element_id: str
    """The ID of the element that containing the reference."""

    property: str
    """The property on the element that contains the reference."""

    reference_id: str
    """The id of the reference."""


class ParseContext:
    """Context for parsing BPMN elements from XML dictionaries."""

    def __init__(self):
        self.elements_by_id: dict[str, ElementDescriptor] = {}
        """A mapping from element ID to element descriptor."""

        self.references: list[Reference] = []
        """A list of unresolved references."""

    def add_reference(self, reference: Reference) -> None:
        """Add an unresolved reference."""
        self.references.append(reference)

    def add_element(self, element: ElementDescriptor) -> None:
        """Add a processed element."""
        if (id_value := getattr(element, "id", None)) or (id_value := getattr(element, "@id", None)):
            self.elements_by_id[id_value] = element


class Parser:
    """A parser for BPMN files."""

    def __init__(self, moddle_extensions: Optional[list[Path]] = None, ns_map: Optional[dict[str, str]] = None):
        load_default_plugins()
        self.ns_map = NAMESPACES.copy()
        if ns_map:
            self.ns_map.update(ns_map)
        self.moddle_extensions = moddle_extensions or []
        for extension_path in self.moddle_extensions:
            load_moddle_file(extension_path)
        convert_moddle_registry()

    def parse_file(self, xml_file: Path) -> ParseResult:
        """
        Parse a BPMN XML file into internal representation.

        Args:
            xml_file: The path to a BPMN XML file

        Returns:
            Definitions object
        """
        xml = xml_file.read_text(encoding="utf-8")
        return self.parse_string(xml)

    def parse_string(self, xml_str: str) -> ParseResult:
        """
        Parse a BPMN XML string into internal representation.

        Args:
            xml_str: A BPMN XML string

        Returns:
            Dictionary containing parsed nodes and flows
        """
        from pybpmn_parser.factory import create_bpmn

        # Validate XML first
        validation_result = validate(xml_str)
        for error in validation_result.errors:
            print(error)
        validation_result.raise_for_errors()

        # Parse root element
        root = xmltodict.parse(xml_str)
        context = ParseContext()
        definition_element = create_bpmn(root, context, self.ns_map)
        return ParseResult(definition_element, context)
