"""Represents the BPMN throw event object."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.event import Event
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from lxml import etree as ET

    from pybpmn_parser.bpmn.data.data_association import DataInputAssociation
    from pybpmn_parser.bpmn.data.data_input import DataInput
    from pybpmn_parser.bpmn.data.input_set import InputSet
    from pybpmn_parser.bpmn.event_definition.cancel_event_definition import CancelEventDefinition
    from pybpmn_parser.bpmn.event_definition.compensate_event_definition import CompensateEventDefinition
    from pybpmn_parser.bpmn.event_definition.conditional_event_definition import ConditionalEventDefinition
    from pybpmn_parser.bpmn.event_definition.error_event_definition import ErrorEventDefinition
    from pybpmn_parser.bpmn.event_definition.escalation_event_definition import EscalationEventDefinition
    from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
    from pybpmn_parser.bpmn.event_definition.link_event_definition import LinkEventDefinition
    from pybpmn_parser.bpmn.event_definition.message_event_definition import MessageEventDefinition
    from pybpmn_parser.bpmn.event_definition.signal_event_definition import SignalEventDefinition
    from pybpmn_parser.bpmn.event_definition.terminate_event_definition import TerminateEventDefinition
    from pybpmn_parser.bpmn.event_definition.timer_event_definition import TimerEventDefinition


@register_element
@dataclass(kw_only=True)
class ThrowEvent(Event):  # Is Abstract
    """Throw events are used to "emit" a particular type of event."""

    data_inputs: list[DataInput] = field(
        default_factory=list,
        metadata={
            "name": "dataInput",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    data_input_associations: list[DataInputAssociation] = field(
        default_factory=list,
        metadata={
            "name": "dataInputAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    input_set: Optional[InputSet] = field(
        default=None,
        metadata={
            "name": "inputSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    timer_event_definitions: list[TimerEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "timerEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    terminate_event_definitions: list[TerminateEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "terminateEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    signal_event_definitions: list[SignalEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "signalEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    message_event_definitions: list[MessageEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "messageEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    link_event_definitions: list[LinkEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "linkEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    escalation_event_definitions: list[EscalationEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "escalationEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    error_event_definitions: list[ErrorEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "errorEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    conditional_event_definitions: list[ConditionalEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "conditionalEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    compensate_event_definitions: list[CompensateEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "compensateEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    cancel_event_definitions: list[CancelEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "cancelEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    event_definitions: list[EventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "eventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    event_definition_refs: list[str] = field(
        default_factory=list,
        metadata={
            "name": "eventDefinitionRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )

    class Meta:
        name = "throwEvent"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[ThrowEvent]:
        """Parse the XML element and return an object of this class."""
        from pybpmn_parser.bpmn.data.data_association import DataInputAssociation
        from pybpmn_parser.bpmn.data.data_input import DataInput
        from pybpmn_parser.bpmn.data.input_set import InputSet
        from pybpmn_parser.bpmn.event_definition.cancel_event_definition import CancelEventDefinition
        from pybpmn_parser.bpmn.event_definition.compensate_event_definition import CompensateEventDefinition
        from pybpmn_parser.bpmn.event_definition.conditional_event_definition import ConditionalEventDefinition
        from pybpmn_parser.bpmn.event_definition.error_event_definition import ErrorEventDefinition
        from pybpmn_parser.bpmn.event_definition.escalation_event_definition import EscalationEventDefinition
        from pybpmn_parser.bpmn.event_definition.event_definition import EventDefinition
        from pybpmn_parser.bpmn.event_definition.link_event_definition import LinkEventDefinition
        from pybpmn_parser.bpmn.event_definition.message_event_definition import MessageEventDefinition
        from pybpmn_parser.bpmn.event_definition.signal_event_definition import SignalEventDefinition
        from pybpmn_parser.bpmn.event_definition.terminate_event_definition import TerminateEventDefinition
        from pybpmn_parser.bpmn.event_definition.timer_event_definition import TimerEventDefinition

        if obj is None:
            return None

        baseclass = Event.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "cancel_event_definitions": [
                    CancelEventDefinition.parse(elem)
                    for elem in obj.findall("./bpmn:cancelEventDefinition", NAMESPACES)
                ],
                "compensate_event_definitions": [
                    CompensateEventDefinition.parse(elem)
                    for elem in obj.findall("./bpmn:compensateEventDefinition", NAMESPACES)
                ],
                "conditional_event_definitions": [
                    ConditionalEventDefinition.parse(elem)
                    for elem in obj.findall("./bpmn:conditionalEventDefinition", NAMESPACES)
                ],
                "data_inputs": [DataInput.parse(elem) for elem in obj.findall("./bpmn:dataInput", NAMESPACES)],
                "data_input_associations": [
                    DataInputAssociation.parse(elem) for elem in obj.findall("./bpmn:dataInputAssociation", NAMESPACES)
                ],
                "error_event_definitions": [
                    ErrorEventDefinition.parse(elem) for elem in obj.findall("./bpmn:errorEventDefinition", NAMESPACES)
                ],
                "escalation_event_definitions": [
                    EscalationEventDefinition.parse(elem)
                    for elem in obj.findall("./bpmn:escalationEventDefinition", NAMESPACES)
                ],
                "event_definitions": [
                    EventDefinition.parse(elem) for elem in obj.findall("./bpmn:eventDefinition", NAMESPACES)
                ],
                "event_definition_refs": [elem.text for elem in obj.findall("./bpmn:eventDefinitionRef", NAMESPACES)],
                "input_set": InputSet.parse(obj.find("./bpmn:inputSet", NAMESPACES)),
                "link_event_definitions": [
                    LinkEventDefinition.parse(elem) for elem in obj.findall("./bpmn:linkEventDefinition", NAMESPACES)
                ],
                "message_event_definitions": [
                    MessageEventDefinition.parse(elem)
                    for elem in obj.findall("./bpmn:messageEventDefinition", NAMESPACES)
                ],
                "signal_event_definitions": [
                    SignalEventDefinition.parse(elem)
                    for elem in obj.findall("./bpmn:signalEventDefinition", NAMESPACES)
                ],
                "terminate_event_definitions": [
                    TerminateEventDefinition.parse(elem)
                    for elem in obj.findall("./bpmn:terminateEventDefinition", NAMESPACES)
                ],
                "timer_event_definitions": [
                    TimerEventDefinition.parse(elem) for elem in obj.findall("./bpmn:timerEventDefinition", NAMESPACES)
                ],
            }
        )

        return cls(**attribs)
