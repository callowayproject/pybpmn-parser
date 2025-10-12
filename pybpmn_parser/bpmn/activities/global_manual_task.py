"""Represents a Global Manual Task."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.process.global_task import GlobalTask


@dataclass(kw_only=True)
class GlobalManualTask(GlobalTask):
    """A type of Global Task that represents a Manual Task."""

    pass
