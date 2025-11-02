"""Model definition for Label."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.di.node import Node
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.dc.bounds import Bounds

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DI"


@register_element
@dataclass(kw_only=True)
class Label(Node):
    """
    A label is a node owned by another element that depicts an aspect of that element within its own separate bounds.
    """

    class Meta:
        name = "label"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"

    bounds: Optional[Bounds] = field(
        default=None,
        metadata={
            "name": "Bounds",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/DD/20100524/DC",
        },
    )
    """The bounds (x, y, width, and height) of the label relative to the origin of a containing plane."""
