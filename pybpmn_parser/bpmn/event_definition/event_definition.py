"""Represents an Event Definition."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.foundation.base_element import RootElement


@dataclass(kw_only=True)
class EventDefinition(RootElement):  # Is Abstract
    """The abstract base class for event definitions."""

    pass
