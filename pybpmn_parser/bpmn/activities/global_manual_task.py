"""Represents a Global Manual Task."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.process.global_task import GlobalTask
from pybpmn_parser.element_registry import register_element


@register_element
@dataclass(kw_only=True)
class GlobalManualTask(GlobalTask):
    """A type of Global Task that represents a Manual Task."""

    class Meta:
        name = "globalManualTask"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
