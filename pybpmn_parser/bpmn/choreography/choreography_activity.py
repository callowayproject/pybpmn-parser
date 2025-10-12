"""The base class for choreography tasks."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.flow_node import FlowNode
from pybpmn_parser.bpmn.types import NAMESPACES, ChoreographyLoopType

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.correlation_key import CorrelationKey


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ChoreographyActivity]:
        """Create an instance of this class from an XML element."""
        from pybpmn_parser.bpmn.common.correlation_key import CorrelationKey

        if obj is None:
            return None

        baseclass = FlowNode.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "participant_refs": [elem.text for elem in obj.findall("./bpmn:participantRef", NAMESPACES)],
                "correlation_keys": [
                    CorrelationKey.parse(elem) for elem in obj.findall("./bpmn:correlationKey", NAMESPACES)
                ],
                "initiating_participant_ref": obj.get("initiatingParticipantRef").text,
                "loop_type": ChoreographyLoopType(obj.get("loopType", ChoreographyLoopType.NONE)),
            }
        )

        return cls(**attribs)
