"""Represents an ExtensionElements tag."""

from __future__ import annotations

from typing import Any

import lxml.etree as ET

from pybpmn_parser.plugins.registry import registry


# @dataclass(kw_only=True)
class ExtensionElements:
    """Representation of an extensionElements tag."""

    # extensions: list[Any] = field(
    #     default_factory=list,
    #     metadata={
    #         "type": "Wildcard",
    #         "namespace": "##other",
    #     },
    # )
    # """Definitions of extension elements."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the ExtensionElements object."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def parse(cls, obj: ET.Element) -> ExtensionElements:
        """Parse an ExtensionElements object."""
        extensions = {}

        for child in obj.iterchildren():
            extension_parsers = registry.get_parser_for_tag(child.tag, child.prefix)
            for extension_parser in extension_parsers:
                element_tag = extension_parser.element_name().split("}")[-1]
                prefix = extension_parser.__xml_ns__
                extensions[f"{prefix}_{element_tag}"] = extension_parser.from_xml_tree(child)

        return cls(**extensions)
