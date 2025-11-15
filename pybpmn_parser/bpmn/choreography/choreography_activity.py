"""The base class for choreography tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.common.flow_node import FlowNode
from pybpmn_parser.bpmn.types import ChoreographyLoopType
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.common.correlation_key import CorrelationKey


@register_element
@dataclass(kw_only=True)
class ChoreographyActivity(FlowNode):  # Is Abstract
    """The base class for choreography tasks."""

    participant_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "participantRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 2,
            "is_reference": True,
        },
    )
    correlation_keys: list[CorrelationKey] = field(
        default_factory=list,
        metadata={
            "name": "correlationKey",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    initiating_participant_ref: str = field(
        metadata={
            "name": "initiatingParticipantRef",
            "type": "Attribute",
            "required": True,
            "is_reference": True,
        }
    )
    loop_type: ChoreographyLoopType = field(
        default=ChoreographyLoopType.NONE,
        metadata={
            "name": "loopType",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "choreographyActivity"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
