"""Represents an ExtensionElements tag."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.element_registry import register_element


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
