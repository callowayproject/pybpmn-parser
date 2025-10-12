"""Represents a Cancel Event Definition."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event_definition import EventDefinition


@dataclass(kw_only=True)
class CancelEventDefinition(EventDefinition):
    """The definition of a cancel event."""

    pass
