"""Represents a Timer Event Definition."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.common.expression import Expression


@register_element
@dataclass(kw_only=True)
class TimerEventDefinition(EventDefinition):
    """Defines a timer event."""

    class Meta:
        name = "timerEventDefinition"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    time_date: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "timeDate",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    time_duration: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "timeDuration",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    time_cycle: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "timeCycle",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[TimerEventDefinition]:
        """Parse an XML element into this class."""
        from pybpmn_parser.bpmn.common.expression import Expression

        if obj is None:
            return None

        baseclass = EventDefinition.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "time_date": Expression.parse(obj.find("./bpmn:timeDate", NAMESPACES)),
                "time_duration": Expression.parse(obj.find("./bpmn:timeDuration", NAMESPACES)),
                "time_cycle": Expression.parse(obj.find("./bpmn:timeCycle", NAMESPACES)),
            }
        )
        return cls(**attribs)
