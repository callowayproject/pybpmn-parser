"""Represents a BPMN 2.0 Parallel Gateway."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.gateway import Gateway
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class ParallelGateway(Gateway):
    """A Parallel Gateway is used to synchronize (combine) parallel flows and to create parallel flows."""

    class Meta:
        name = "parallelGateway"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
