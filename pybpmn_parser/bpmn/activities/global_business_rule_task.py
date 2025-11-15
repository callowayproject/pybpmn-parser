"""Represents a Global Business Rule Task."""

from __future__ import annotations

from dataclasses import dataclass, field

from pybpmn_parser.bpmn.process.global_task import GlobalTask
from pybpmn_parser.bpmn.types import ImplementationValue
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class GlobalBusinessRuleTask(GlobalTask):
    """A type of Global Task that represents a Business Rule Task."""

    implementation: str | ImplementationValue = field(
        default=ImplementationValue.UNSPECIFIED,
        metadata={
            "type": "Attribute",
        },
    )

    class Meta:
        name = "globalBusinessRuleTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
