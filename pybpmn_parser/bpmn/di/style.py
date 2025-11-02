"""Model definition for a style."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DI"

from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Style:
    """A style is a container for properties that affect the formatting of a set of diagram elements."""

    class Meta:
        name = "style"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """The unique id of this element."""
