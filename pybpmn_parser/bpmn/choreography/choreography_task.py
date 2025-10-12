"""Represents a Choreography Task."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.choreography.choreography_activity import ChoreographyActivity
from pybpmn_parser.bpmn.types import NAMESPACES

if TYPE_CHECKING:
    from lxml import etree as ET


@dataclass(kw_only=True)
class ChoreographyTask(ChoreographyActivity):
    """
    A Choreography Task is an atomic Activity in a Choreography Process.

    It represents an Interaction, which is one or two Message exchanges between two Participants.
    """

    message_flow_ref: list[str] = field(
        default_factory=list,
        metadata={
            "name": "messageFlowRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 1,
            "max_occurs": 2,
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ChoreographyTask]:
        """Create an instance of this class from an XML element."""
        if obj is None:
            return None

        baseclass = ChoreographyActivity.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update({"message_flow_ref": [elem.text for elem in obj.findall("./bpmn:messageFlowRef", NAMESPACES)]})
        return cls(**attribs)
