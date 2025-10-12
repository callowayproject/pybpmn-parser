"""The Auditing element and its model associations allow defining attributes related to auditing."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.foundation.base_element import BaseElement


@dataclass(kw_only=True)
class Auditing(BaseElement):
    """
    The Auditing element and its model associations allow defining attributes related to auditing.

    It leverages the BPMN extensibility mechanism. This element is used by FlowElements and Process.
    BPMN 2.0 implementations can define their own set of attributes and their intended semantics.
    """

    pass
