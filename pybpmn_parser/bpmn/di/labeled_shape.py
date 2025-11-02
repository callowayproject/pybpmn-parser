"""Model definition for LabeledShape."""

from __future__ import annotations

from dataclasses import dataclass

from pybpmn_parser.bpmn.di.shape import Shape

__NAMESPACE__ = "http://www.omg.org/spec/DD/20100524/DI"


@dataclass(kw_only=True)
class LabeledShape(Shape):
    """A LabeledShape represents a shape that owns a collection of labels."""

    class Meta:
        name = "labeledShape"
        namespace = "http://www.omg.org/spec/DD/20100524/DI"
