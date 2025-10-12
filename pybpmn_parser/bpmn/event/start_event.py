"""Represents a Start Event."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.event.catch_event import CatchEvent
from pybpmn_parser.bpmn.types import StartEventType

if TYPE_CHECKING:
    from lxml import etree as ET


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

    @classmethod
    def parse(cls, obj: Optional[ET.Element]) -> Optional[StartEvent]:
        """Parse XML into this class."""
        if obj is None:
            return None
        baseclass = CatchEvent.parse(obj)
        attribs = {field.name: getattr(baseclass, field.name) for field in fields(baseclass)}
        attribs.update(
            {
                "is_interrupting": str(obj.get("isInterrupting")).lower() == "true",
            }
        )
        return cls(**attribs)

    @property
    def event_type(self) -> StartEventType:  # noqa: C901
        """Return the event type."""
        num_msg_defs = len(self.message_event_definition)
        num_timer_defs = len(self.timer_event_definition)
        num_cond_defs = len(self.conditional_event_definition)
        num_sig_defs = len(self.signal_event_definition)
        num_escal_defs = len(self.escalation_event_definition)
        num_comp_defs = len(self.compensate_event_definition)
        num_error_defs = len(self.error_event_definition)
        num_defs = len(self.event_definition)
        num_event_refs = len(self.event_definition_ref)
        total_defs = (
            num_msg_defs
            + num_timer_defs
            + num_cond_defs
            + num_sig_defs
            + num_escal_defs
            + num_comp_defs
            + num_error_defs
            + num_defs
            + num_event_refs
        )
        if total_defs > 1:
            if self.parallel_multiple:
                return StartEventType.PARALLEL_MULTIPLE
            else:
                return StartEventType.MULTIPLE

        if total_defs == 0:
            return StartEventType.NONE

        if num_msg_defs:
            return StartEventType.MESSAGE

        if num_timer_defs:
            return StartEventType.TIMER

        if num_cond_defs:
            return StartEventType.CONDITIONAL

        if num_sig_defs:
            return StartEventType.SIGNAL

        if num_escal_defs:
            return StartEventType.ESCALATION

        if num_error_defs:
            return StartEventType.ERROR

        if num_comp_defs:
            return StartEventType.COMPENSATION

        return StartEventType.UNKNOWN
