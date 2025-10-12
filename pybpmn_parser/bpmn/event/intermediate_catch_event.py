"""Represents an intermediate catch event."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event.catch_event import CatchEvent


@dataclass(kw_only=True)
class IntermediateCatchEvent(CatchEvent):
    """The IntermediateCatchEvent catches an event that happens somewhere between the start and end of a Process."""

    pass
