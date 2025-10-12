"""Represents a BPMN 2.0 Parallel Gateway."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.gateway import Gateway


@dataclass(kw_only=True)
class ParallelGateway(Gateway):
    """A Parallel Gateway is used to synchronize (combine) parallel flows and to create parallel flows."""

    pass
