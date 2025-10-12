"""An Artifact allows showing additional information about a Process that is not directly related to its Flows."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.foundation.base_element import BaseElement


@dataclass(kw_only=True)
class Artifact(BaseElement):  # Is Abstract
    """An Artifact allows showing additional information about a Process that is not directly related to its Flows."""

    pass
