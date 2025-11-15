"""Represents a BPMN IoSpecification element."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.data.data_input import DataInput
    from pybpmn_parser.bpmn.data.data_output import DataOutput
    from pybpmn_parser.bpmn.data.input_set import InputSet
    from pybpmn_parser.bpmn.data.output_set import OutputSet


@register_element
@dataclass(kw_only=True)
class IoSpecification(BaseElement):
    """The ioSpecification defines the inputs and outputs and the InputSets and OutputSets for the Activity."""

    data_inputs: list[DataInput] = field(
        default_factory=list,
        metadata={
            "name": "dataInput",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """A reference to the InputSets defined by the InputOutputSpecification.

    Every InputOutputSpecification must define at least one InputSet."""

    data_outputs: list[DataOutput] = field(
        default_factory=list,
        metadata={
            "name": "dataOutput",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """A reference to the OutputSets defined by the InputOutputSpecification.

    Every InputOutputSpecification must define at least one OutputSet."""

    input_sets: list[InputSet] = field(
        default_factory=list,
        metadata={
            "name": "inputSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 1,
        },
    )
    """The Data Inputs that are required to start the Activity.

    An optional reference to the Data Inputs of the InputOutputSpecification.
    If the InputOutputSpecification defines no Data Input, it means no data is required to start the Activity.
    This is an ordered set."""

    output_sets: list[OutputSet] = field(
        default_factory=list,
        metadata={
            "name": "outputSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "min_occurs": 1,
        },
    )
    """The Data Outputs that are required to finish the Activity.

    An optional reference to the Data Outputs of the InputOutputSpecification.
    If the InputOutputSpecification defines no Data Output, it means no data is required to finish the Activity.
    This is an ordered set."""

    class Meta:
        name = "ioSpecification"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
