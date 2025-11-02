"""Represents an ExtensionElements tag."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    import lxml.etree as ET


@register_element
@dataclass(kw_only=True)
class ExtensionElements:
    """Representation of an extensionElements tag."""

    class Meta:
        name = "extensionElements"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    # extensions: list[Any] = field(
    #     default_factory=list,
    #     metadata={
    #         "type": "Wildcard",
    #         "namespace": "##other",
    #     },
    # )
    # """Definitions of extension elements."""

    @classmethod
    def parse(cls, obj: ET.Element) -> ExtensionElements:
        """Parse an ExtensionElements object."""
        extensions: dict[str, Any] = {}

        # for child in obj.iterchildren():
        #     extension_parsers = registry.get_parser_for_tag(child.tag, child.prefix)
        #     for extension_parser in extension_parsers:
        #         element_tag = extension_parser.element_name().split("}")[-1]
        #         prefix = extension_parser.__xml_ns__
        #         extensions[f"{prefix}_{element_tag}"] = extension_parser.from_xml_tree(child)

        return cls(**extensions)
