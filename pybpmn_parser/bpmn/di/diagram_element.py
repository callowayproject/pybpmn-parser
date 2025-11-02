"""Model definitions for DiagramElement."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DI"

from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class DiagramElement:
    """DiagramElement is the abstract supertype of all elements that can be nested in a diagram."""

    class Meta:
        name = "diagramElement"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """The unique identifier of the diagram element."""
