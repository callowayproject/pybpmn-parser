"""Represents an intermediate throw event."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event.throw_event import ThrowEvent


@dataclass(kw_only=True)
class IntermediateThrowEvent(ThrowEvent):
    """The IntermediateThrowEvent triggers an event somewhere between the start and end of a Process."""

    pass
