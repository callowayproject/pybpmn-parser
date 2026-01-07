"""Represents the loop characteristics of an activity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.foundation.base_element import BaseElement
from pybpmn_parser.bpmn.types import MultiInstanceFlowCondition
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.activities.complex_behavior_definition import ComplexBehaviorDefinition
    from pybpmn_parser.bpmn.common.expression import Expression
    from pybpmn_parser.bpmn.data.data_input import DataInput
    from pybpmn_parser.bpmn.data.data_output import DataOutput


@register_element
@dataclass(kw_only=True)
class LoopCharacteristics(BaseElement):
    """
    The presence of LoopCharacteristics signifies that the Activity has looping behavior.

    LoopCharacteristics is an abstract class.
    """

    class Meta:
        name = "loopCharacteristics"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"


@register_element
@dataclass(kw_only=True)
class MultiInstanceLoopCharacteristics(LoopCharacteristics):
    """Allows for the creation of a desired number of Activity instances."""

    loop_cardinality: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "loopCardinality",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    loop_data_input_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "loopDataInputRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    loop_data_output_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "loopDataOutputRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "is_reference": True,
        },
    )
    input_data_item: Optional[DataInput] = field(
        default=None,
        metadata={
            "name": "inputDataItem",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    output_data_item: Optional[DataOutput] = field(
        default=None,
        metadata={
            "name": "outputDataItem",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    complex_behavior_definitions: list[ComplexBehaviorDefinition] = field(
        default_factory=list,
        metadata={
            "name": "complexBehaviorDefinition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    completion_condition: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "completionCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    is_sequential: bool = field(
        default=False,
        metadata={
            "name": "isSequential",
            "type": "Attribute",
        },
    )
    behavior: MultiInstanceFlowCondition = field(
        default=MultiInstanceFlowCondition.ALL,
        metadata={
            "type": "Attribute",
        },
    )
    one_behavior_event_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "oneBehaviorEventRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )
    none_behavior_event_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "noneBehaviorEventRef",
            "type": "Attribute",
            "is_reference": True,
        },
    )

    class Meta:
        name = "multiInstanceLoopCharacteristics"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"


@register_element
@dataclass(kw_only=True)
class StandardLoopCharacteristics(LoopCharacteristics):
    """The StandardLoopCharacteristics class defines looping behavior based on a boolean condition."""

    loop_condition: Optional[Expression] = field(
        default=None,
        metadata={
            "name": "loopCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    test_before: bool = field(
        default=False,
        metadata={
            "name": "testBefore",
            "type": "Attribute",
        },
    )
    loop_maximum: Optional[int] = field(
        default=None,
        metadata={
            "name": "loopMaximum",
            "type": "Attribute",
        },
    )

    class Meta:
        name = "standardLoopCharacteristics"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
