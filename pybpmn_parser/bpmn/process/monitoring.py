"""The Monitoring and its model associations allow defining attributes related to monitoring."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Monitoring(BaseElement):
    """
    The Monitoring and its model associations allow defining attributes related to monitoring.

    It leverages the BPMN extensibility mechanism. This element is used by FlowElements and Process.
    BPMN 2.0.2 implementations can define their own set of attributes and their intended semantics.
    """

    class Meta:
        name = "monitoring"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
