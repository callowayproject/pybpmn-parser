"""Model definition for bounds."""

from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DC"

from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Bounds:
    """Bounds specify an area in some (x, y) coordinate system."""

    class Meta:
        name = "Bounds"
        namespace = "http://www.omg.org/spec/DD/20100524/DC"

    x: float = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    """A real number that represents the x-coordinate of the rectangle."""
    y: float = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    """A real number that represents the y-coordinate of the rectangle."""

    width: float = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    """A real number that represents the width of the rectangle."""

    height: float = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    """A real number that represents the height of the rectangle."""
