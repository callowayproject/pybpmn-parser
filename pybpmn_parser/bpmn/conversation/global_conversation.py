"""Represents a GlobalConversation."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.collaboration.collaboration import Collaboration
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class GlobalConversation(Collaboration):
    """A GlobalConversation is a reusable, atomic Conversation definition callable from within any Collaboration."""

    class Meta:
        name = "globalConversation"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
