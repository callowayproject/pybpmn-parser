"""Represents an end event."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event.throw_event import ThrowEvent


@dataclass(kw_only=True)
class EndEvent(ThrowEvent):
    """The End Event indicates where a Process will end."""

    pass
