"""Represents an implicit throw event."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.event.throw_event import ThrowEvent


@dataclass(kw_only=True)
class ImplicitThrowEvent(ThrowEvent):
    """The ImplicitThrowEvent is a non-graphical Event used for complex Multi-Instance Activities."""

    pass
