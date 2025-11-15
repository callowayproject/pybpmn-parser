"""Representation for BPMN 2.0 activity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.common.flow_node import FlowNode
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.activities.loop_characteristics import (
        LoopCharacteristics,
        MultiInstanceLoopCharacteristics,
        StandardLoopCharacteristics,
    )
    from pybpmn_parser.bpmn.activities.resource_role import ResourceRole
    from pybpmn_parser.bpmn.data.data_association import DataInputAssociation, DataOutputAssociation
    from pybpmn_parser.bpmn.data.io_specification import IoSpecification
    from pybpmn_parser.bpmn.data.property import Property
    from pybpmn_parser.bpmn.process.performer import HumanPerformer, Performer, PotentialOwner


@register_element
@dataclass(kw_only=True)
class Activity(FlowNode):  # Is Abstract
    """
    An Activity is a Process step that can be atomic (Tasks) or decomposable (Sub-Processes).

    Activities are executed by either a system (automated) or humans (manual).
    """

    io_specification: Optional[IoSpecification] = field(
        default=None,
        metadata={
            "name": "ioSpecification",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """The inputs and outputs, as well as the InputSets and OutputSets, for the Activity."""

    properties: list[Property] = field(
        default_factory=list,
        metadata={
            "name": "property",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Modeler-defined properties added to an Activity."""

    data_input_associations: list[DataInputAssociation] = field(
        default_factory=list,
        metadata={
            "name": "dataInputAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """An optional reference to the `DataInputAssociations`.

    A `DataInputAssociation` defines how the DataInput of the Activity's `InputOutputSpecification` is populated."""

    data_output_associations: list[DataOutputAssociation] = field(
        default_factory=list,
        metadata={
            "name": "dataOutputAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """An optional reference to the `DataOutputAssociations`."""

    potential_owners: list[PotentialOwner] = field(
        default_factory=list,
        metadata={
            "name": "potentialOwner",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Potential owners of a User Task are persons who can claim and work on it."""

    human_performers: list[HumanPerformer] = field(
        default_factory=list,
        metadata={
            "name": "humanPerformer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """People can be assigned to Activities in various roles."""

    performers: list[Performer] = field(
        default_factory=list,
        metadata={
            "name": "performer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """People can be assigned to Activities in various roles."""

    resources: list[ResourceRole] = field(
        default_factory=list,
        metadata={
            "name": "resourceRole",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """Defines the resource that will perform or will be responsible for the Activity.

    The resource, e.g., a performer, can be specified in the form of a specific individual, a group, an organization
    role or position, or an organization."""

    standard_loop_characteristics: Optional[StandardLoopCharacteristics] = field(
        default=None,
        metadata={
            "name": "standardLoopCharacteristics",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """This defines looping behavior based on a boolean condition.

    The Activity will loop as long as the boolean condition is true.
    The condition is evaluated for every loop iteration, and may be evaluated at the beginning
    or at the end of the iteration."""

    multi_instance_loop_characteristics: Optional[MultiInstanceLoopCharacteristics] = field(
        default=None,
        metadata={
            "name": "multiInstanceLoopCharacteristics",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """This defines the creation of a specified number of Activity instances.

    The instances MAY execute in parallel or MAY be sequential."""

    loop_characteristics: Optional[LoopCharacteristics] = field(
        default=None,
        metadata={
            "name": "loopCharacteristics",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """An Activity may be performed once or may be repeated.

    If repeated, the Activity must have `loopCharacteristics` that define the repetition criteria
    (if the `isExecutable` attribute of the Process is set to true)."""

    is_for_compensation: bool = field(
        default=False,
        metadata={
            "name": "isForCompensation",
            "type": "Attribute",
        },
    )
    """A flag that identifies whether this Activity is intended for compensation.

    If false, then this Activity executes as a result of normal execution flow.
    If true, this Activity is only activated when a Compensation Event is detected and initiated under
    Compensation Event visibility scope."""

    start_quantity: int = field(
        default=1,
        metadata={
            "name": "startQuantity",
            "type": "Attribute",
        },
    )
    """This attribute defines the number of tokens that must arrive before the Activity can begin.

    The default value is 1. The value must not be less than 1.
    Note that any value greater than 1 is an advanced type of modeling and should be used with caution."""

    completion_quantity: int = field(
        default=1,
        metadata={
            "name": "completionQuantity",
            "type": "Attribute",
        },
    )
    """This attribute defines the number of tokens that must be generated from the Activity.

    The default value is 1. The value MUST NOT be less than 1.
    This number of tokens will be sent down any outgoing Sequence Flow, assuming it's conditions are satisfied.
    Note that any value greater than 1 is an advanced type of modeling and should be used with caution."""

    default: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """The Sequence Flow that receives a token when `conditionExpression`s on other outgoing Sequence Flows are false.

    The default Sequence Flow should not have a `conditionExpression`. Any such Expression is ignored."""

    class Meta:
        name = "activity"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
