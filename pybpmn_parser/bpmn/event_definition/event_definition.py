"""Represents an Event Definition."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.foundation.base_element import RootElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class EventDefinition(RootElement):  # Is Abstract
    """The abstract base class for event definitions."""

    class Meta:
        name = "eventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
