"""Parse a BPMN file."""

from pathlib import Path
from typing import Any, Optional

import xmltodict

from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.factory import create_bpmn
from pybpmn_parser.plugins import load_default_plugins
from pybpmn_parser.plugins.moddle import convert_moddle_registry, load_moddle_file
from pybpmn_parser.validator import validate


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

    def parse_file(self, xml_file: Path) -> Any:
        """
        Parse a BPMN XML file into internal representation.

        Args:
            xml_file: The path to a BPMN XML file

        Returns:
            Definitions object
        """
        xml = xml_file.read_text(encoding="utf-8")
        return self.parse_string(xml)

    def parse_string(self, xml_str: str) -> Any:
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
        root = xmltodict.parse(xml_str)
        result = create_bpmn(root, self.ns_map)
        if isinstance(result, list) and len(result) == 1:
            return result[0]
        return result
