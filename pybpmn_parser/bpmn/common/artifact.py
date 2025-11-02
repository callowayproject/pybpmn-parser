"""An Artifact allows showing additional information about a Process that is not directly related to its Flows."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Artifact(BaseElement):  # Is Abstract
    """An Artifact allows showing additional information about a Process that is not directly related to its Flows."""

    class Meta:
        name = "artifact"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
