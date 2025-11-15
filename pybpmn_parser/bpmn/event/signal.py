"""Represents a BPMN signal element."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Signal(RootElement):
    """
    Signals are triggers generated in the Pool they are published.

    They are typically used for broadcast communication within and across Processes, across Pools, and
    between Process diagrams.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    structure_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "structureRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "signal"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
