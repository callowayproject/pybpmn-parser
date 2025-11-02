"""Model definitions for Diagram."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DI"

from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Diagram:
    """A diagram is a container for a graph of diagram elements that depicts all or part of a model."""

    class Meta:
        name = "diagram"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """The name of the diagram."""

    documentation: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """The documentation of the diagram."""

    resolution: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """The printing resolution of the diagram is expressed in Units Per Inch (UPI)."""

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """The unique identifier of the diagram."""
