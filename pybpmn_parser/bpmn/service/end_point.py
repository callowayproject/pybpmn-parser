"""Represents an EndPoint."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.foundation.base_element import RootElement


@dataclass(kw_only=True)
class EndPoint(RootElement):
    """The EndPoint element may be extended with endpoint reference definitions introduced in other specifications."""

    pass
