"""A model definition of a BPMNShape."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.bpmn.di.labeled_shape import LabeledShape
from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.bpmndi.bpmnlabel import BPMNLabel
    from pybpmn_parser.bpmn.bpmndi.types import ParticipantBandKind

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/20100524/DI"


@register_element
@dataclass(kw_only=True)
class BPMNShape(LabeledShape):
    """A `BPMNShape` is a shape that can depict a BPMN model element."""

    class Meta:
        name = "BPMNShape"
        namespace = "http://www.omg.org/spec/BPMN/20100524/DI"

    label: Optional[BPMNLabel] = field(
        default=None,
        metadata={
            "name": "BPMNLabel",
            "type": "Element",
        },
    )
    """An optional label that is nested when the shape has a visible text label with its own bounding box."""

    bpmn_element: Optional[str] = field(
        default=None,
        metadata={
            "name": "bpmnElement",
            "type": "Attribute",
        },
    )
    """A reference to a BPMN node element that this shape depicts."""

    is_horizontal: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isHorizontal",
            "type": "Attribute",
        },
    )
    """
    An optional attribute that should be used only for Pools and Lanes.
    It determines if it should be depicted horizontally (true) or vertically (false).
    """

    is_expanded: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isExpanded",
            "type": "Attribute",
        },
    )
    """
    An optional attribute that should be used only for SubProcess, AdHocSubProcess, Transaction, SubChoreographies,
    CallActivities, and CallChoreographies.
    It determines if it should be depicted expanded (true) or collapsed (false).
    """

    is_marker_visible: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isMarkerVisible",
            "type": "Attribute",
        },
    )
    """
    An optional attribute that should be used only for Exclusive Gateway.
    It determines if the marker should be depicted on the shape (true) or not (false).
    """

    is_message_visible: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isMessageVisible",
            "type": "Attribute",
        },
    )
    """
    An optional attribute that should only be used for Participant Bands.
    It determines if an envelope decorator should be depicted linked to the Participant Band.
    """

    participant_band_kind: Optional[ParticipantBandKind] = field(
        default=None,
        metadata={
            "name": "participantBandKind",
            "type": "Attribute",
        },
    )
    """
    An optional attribute that should only be used for Participant Bands. If this attribute is present,
    the participant should be depicted as a Participant Band rather than a Pool.
    """

    choreography_activity_shape: Optional[str] = field(
        default=None,
        metadata={
            "name": "choreographyActivityShape",
            "type": "Attribute",
        },
    )
    """
    An optional attribute that should only be used for Participant Bands. It is REQUIRED for a `BPMNShape` depicting
    a Participant Band. This is REQUIRED to relate the Participant Band to the `BPMNShape` depicting the Choreography
    Activity that this Participant Band is related to.
    """
