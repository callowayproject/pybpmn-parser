"""Representations of Tasks."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.activities.activity import Activity
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class Task(Activity):
    """
    A Task is an atomic Activity within a Process flow.

    A Task is used when the work in the Process cannot be broken down to a finer level of detail.
    """

    class Meta:
        name = "task"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
