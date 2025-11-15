"""Represents the BPMN catch event object."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

from pybpmn_parser.bpmn.event import Event
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.data.data_association import DataOutputAssociation
    from pybpmn_parser.bpmn.data.data_output import DataOutput
    from pybpmn_parser.bpmn.data.output_set import OutputSet
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
class CatchEvent(Event):  # Is Abstract
    """Catch events are used to "receive" or "catch" a particular type of event."""

    data_output: List[DataOutput] = field(
        default_factory=list,
        metadata={
            "name": "dataOutput",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Data that is produced."""

    data_output_association: List[DataOutputAssociation] = field(
        default_factory=list,
        metadata={
            "name": "dataOutputAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    output_set: Optional[OutputSet] = field(
        default=None,
        metadata={
            "name": "outputSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    timer_event_definition: List[TimerEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "timerEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    terminate_event_definition: List[TerminateEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "terminateEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    signal_event_definition: List[SignalEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "signalEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    message_event_definition: List[MessageEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "messageEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    link_event_definition: List[LinkEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "linkEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    escalation_event_definition: List[EscalationEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "escalationEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    error_event_definition: List[ErrorEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "errorEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    conditional_event_definition: List[ConditionalEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "conditionalEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    compensate_event_definition: List[CompensateEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "compensateEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    cancel_event_definition: List[CancelEventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "cancelEventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    event_definition: List[EventDefinition] = field(
        default_factory=list,
        metadata={
            "name": "eventDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    event_definition_ref: List[str] = field(
        default_factory=list,
        metadata={
            "name": "eventDefinitionRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    parallel_multiple: bool = field(
        default=False,
        metadata={
            "name": "parallelMultiple",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "catchEvent"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
