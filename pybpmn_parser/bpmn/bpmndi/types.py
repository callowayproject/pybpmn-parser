"""Type definitions for BPMNDI."""

from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://www.omg.org/spec/BPMN/20100524/DI"


class MessageVisibleKind(Enum):
    """MessageVisibleKind applies only to Participant Band and Message Flow."""

    INITIATING = "initiating"
    """The envelope should not be shaded."""

    NON_INITIATING = "non_initiating"
    """The envelope should be shaded."""


class ParticipantBandKind(Enum):
    """ParticipantBandKind defines the type of Participant Band to depict."""

    TOP_INITIATING = "top_initiating"
    """The band should be depicted as a non-shaded top band."""

    MIDDLE_INITIATING = "middle_initiating"
    """The band should be depicted as a non-shaded middle band."""

    BOTTOM_INITIATING = "bottom_initiating"
    """The band should be depicted as a non-shaded bottom band."""

    TOP_NON_INITIATING = "top_non_initiating"
    """The band should be depicted as a shaded top band."""

    MIDDLE_NON_INITIATING = "middle_non_initiating"
    """The band should be depicted as a shaded middle band."""

    BOTTOM_NON_INITIATING = "bottom_non_initiating"
    """The band should be depicted as a shaded bottom band."""
