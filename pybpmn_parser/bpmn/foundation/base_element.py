"""BPMN BaseElements and shallow subclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pybpmn_parser.element_registry import register_element

if TYPE_CHECKING:
    from pybpmn_parser.bpmn.foundation.documentation import Documentation
    from pybpmn_parser.bpmn.foundation.extension_elements import ExtensionElements


@register_element
@dataclass(kw_only=True)
class BaseElement:  # Is Abstract
    """
    BaseElement is the abstract super class for most BPMN elements.

    It provides the attributes id and documentation, which other elements will inherit.
    """

    class Meta:
        name = "baseElement"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    """This attribute is used to uniquely identify BPMN elements.

    The `id` is REQUIRED if this element is referenced or intended to be referenced by something else.
    If the element is not currently referenced and is never intended to be referenced, the `id` MAY be omitted."""

    documentation: list[Documentation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """This attribute is used to annotate the BPMN element, such as descriptions and other documentation."""

    extension_elements: Optional[ExtensionElements] = field(
        default=None,
        metadata={
            "name": "extensionElements",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        },
    )
    """This element is used to add additional information to the element."""


@register_element
@dataclass(kw_only=True)
class RootElement(BaseElement):
    """RootElement is the abstract super class for all BPMN elements that are contained within Definitions."""

    class Meta:
        name = "rootElement"
        namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL"
