"""Represents a Start Event."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pybpmn_parser.bpmn.event.catch_event import CatchEvent
from pybpmn_parser.bpmn.types import StartEventType
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class StartEvent(CatchEvent):
    """The Start Event indicates where a particular Process will start."""

    is_interrupting: bool = field(
        default=True,
        metadata={
            "name": "isInterrupting",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "startEvent"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    @property
    def event_type(self) -> StartEventType:
        """Return the event type."""
        definitions: list[tuple[list[Any], StartEventType]] = [
            (self.message_event_definition, StartEventType.MESSAGE),
            (self.timer_event_definition, StartEventType.TIMER),
            (self.conditional_event_definition, StartEventType.CONDITIONAL),
            (self.signal_event_definition, StartEventType.SIGNAL),
            (self.escalation_event_definition, StartEventType.ESCALATION),
            (self.error_event_definition, StartEventType.ERROR),
            (self.compensate_event_definition, StartEventType.COMPENSATION),
        ]

        specific_count = 0
        matched_type = StartEventType.UNKNOWN

        for event_defs, type_enum in definitions:
            if count := len(event_defs):
                specific_count += count
                if matched_type == StartEventType.UNKNOWN:
                    matched_type = type_enum

        total_defs = specific_count + len(self.event_definition) + len(self.event_definition_ref)

        if total_defs > 1:
            return StartEventType.PARALLEL_MULTIPLE if self.parallel_multiple else StartEventType.MULTIPLE

        return StartEventType.NONE if total_defs == 0 else matched_type
