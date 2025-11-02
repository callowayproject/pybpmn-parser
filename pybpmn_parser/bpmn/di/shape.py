"""Model definition for a shape."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.di.node import Node

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DI"

from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.dc.bounds import Bounds


@register_element
@dataclass(kw_only=True)
class Shape(Node):
    """A shape represents a node that has bounds that are relevant to the origin of a containing plane."""

    class Meta:
        name = "shape"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"

    bounds: Bounds = field(
        metadata={
            "name": "Bounds",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/DD/20100524/DC",
            "required": True,
        }
    )
