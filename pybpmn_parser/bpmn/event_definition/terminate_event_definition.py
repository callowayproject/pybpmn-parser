"""Represents a Terminate Event Definition."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event_definition import EventDefinition


@dataclass(kw_only=True)
class TerminateEventDefinition(EventDefinition):
    """The definition of a terminate event."""

    pass
