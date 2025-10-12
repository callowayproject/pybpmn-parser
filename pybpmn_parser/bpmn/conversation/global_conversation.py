"""Represents a GlobalConversation."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.collaboration.collaboration import Collaboration


@dataclass(kw_only=True)
class GlobalConversation(Collaboration):
    """A GlobalConversation is a reusable, atomic Conversation definition callable from within any Collaboration."""

    pass
