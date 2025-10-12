"""Representations of Tasks."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.activities.activity import Activity


@dataclass(kw_only=True)
class Task(Activity):
    """
    A Task is an atomic Activity within a Process flow.

    A Task is used when the work in the Process cannot be broken down to a finer level of detail.
    """

    pass
