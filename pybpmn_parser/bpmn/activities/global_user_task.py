"""Represents a Global User Task."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.process.global_task import GlobalTask
from pybpmn_parser.bpmn.types import ImplementationValue
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.activities.rendering import Rendering


@register_element
@dataclass(kw_only=True)
class GlobalUserTask(GlobalTask):
    """A type of Global Task that represents a User Task."""

    rendering: list[Rendering] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    implementation: ImplementationValue = field(
        default=ImplementationValue.UNSPECIFIED,
        metadata={
            "type": "Attribute",
        },
    )

    class Meta:
        name = "globalUserTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
