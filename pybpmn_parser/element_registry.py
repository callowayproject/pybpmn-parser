"""A registry for mapping element names to dataclasses."""

from dataclasses import dataclass, fields
from inspect import signature
from typing import Any, Optional, Union, get_args, get_origin

from typing_extensions import type_repr

from pybpmn_parser.bpmn import get_loaded_namespace
from pybpmn_parser.core import QName


@dataclass
class ElementProperty:
    """A property of a BPMN element."""

    property_name: str
    """The name of the attribute on the element class."""

    type: str
    """The type of the attribute on the element class."""

    type_qname: Optional[QName] = None
    """The base type of the attribute on the element class. Automatically set based on the type."""

    is_attr: bool = False
    """Whether the attribute is serialized as an XML attribute."""

    is_many: bool = False
    """Whether the attribute is an array or a single value. Automatically set based on the type."""

    is_optional: bool = False
    """Whether the attribute is optional. Automatically set based on the type."""

    is_reference: bool = False
    """Whether the attribute is a reference to another element."""


@dataclass
class ElementDescriptor:
    """A descriptor for a BPMN element."""

    type: Any
    """The class of the BPMN element."""

    name: str
    """The XML name of the BPMN element."""

    q_name: QName
    """The qualified name of the BPMN element."""

    properties: dict[QName, ElementProperty]
    """A mapping of BPMN attribute names to ElementProperty objects."""


class ElementRegistry:
    """A registry for BPMN elements."""

    def __init__(self):
        self.by_qname: dict[QName, Any] = {}
        self.by_name: dict[str, Any] = {}
        self.registered_namespaces: set[str] = set()

    def register(self, element: Any) -> None:
        """Register an element in the registry."""
        if not hasattr(element, "Meta"):
            raise ValueError(f"Element {element} does not have a Meta class.")
        q_name = QName(uri=element.Meta.namespace, local=element.Meta.name)

        descriptor = descriptor_from_class(element)
        self.by_qname[q_name] = descriptor
        self.by_name[q_name.local] = descriptor
        self.registered_namespaces.add(q_name.uri)


def dataclass_fields(data_class: Any) -> dict[str, dict]:
    """Get the fields of a dataclass."""
    return {fld.name: dict(fld.metadata) for fld in fields(data_class)}


def descriptor_from_class(element_class: Any) -> ElementDescriptor:
    """Create a descriptor from a BPMN element class."""
    from typing import get_type_hints

    q_name = QName(uri=element_class.Meta.namespace, local=element_class.Meta.name)
    property_name_map = {}
    parent_locals = get_loaded_namespace()
    parent_locals.update({element_class.__name__: element_class})  # Add the current class for recursive types
    hints = get_type_hints(element_class, localns=parent_locals)
    fieldz = dataclass_fields(element_class)

    for name, type_hint in hints.items():
        element_qname = QName(
            uri=fieldz[name].get("namespace", q_name.uri),
            local=fieldz[name].get("name", name),
        )
        prop = type_hint_to_property(name, type_hint, fieldz[name])
        property_name_map[element_qname] = prop

    return ElementDescriptor(type=element_class, name=q_name.local, q_name=q_name, properties=property_name_map)


def type_hint_to_property(name: str, type_hint: Any, field_metadata: dict[str, Any]) -> ElementProperty:
    """
    Converts a type hint represented as a dictionary into an `ElementProperty` object.

    This function introspects a provided type hint, extracting metadata and attributes of the type hint to create an
    `ElementProperty`. The extracted information includes whether the type is optional, represents multiple items, or
    is associated with an attribute. The function relies on type inspection utilities to derive these characteristics
    and use them to initialize the `ElementProperty`.

    Args:
        name: The name associated with the type hint or field.
        type_hint: The type hint which defines the expected type or structure.
        field_metadata: Metadata associated with the field, containing information about whether the field is an
            attribute or an element.

    Returns:
        Returns an `ElementProperty` object that captures the metadata, name, and type information
        inferred from the type hint.
    """
    from typing_inspection.introspection import AnnotationSource, inspect_annotation

    annotation = inspect_annotation(
        type_hint, annotation_source=AnnotationSource.DATACLASS, unpack_type_aliases="eager"
    )
    type_ = annotation.type
    origin = get_origin(type_)
    args = get_args(type_)

    is_attr = field_metadata.get("type", "Element") == "Attribute"
    is_optional = origin == Union and type(None) in args
    is_many = origin is list or (origin == Union and list in args)
    is_reference: bool = field_metadata.get("is_reference", False)
    base_type = get_base_type(type_)
    q_name = QName(uri=base_type.Meta.namespace, local=base_type.Meta.name) if hasattr(base_type, "Meta") else None

    return ElementProperty(
        property_name=name,
        type=type_repr(base_type),
        type_qname=q_name,
        is_attr=is_attr,
        is_optional=is_optional,
        is_many=is_many,
        is_reference=is_reference,
    )


registry = ElementRegistry()


def register_element(element: Any) -> Any:
    """Register an element in the global element registry."""

    def from_kwargs(cls: Any, **kwargs) -> Any:
        """
        Add extra kwargs to the dataclass when the element is created.

        Based on: https://blog.jcharistech.com/2024/02/11/pydantic-dataclasses-how-to-allow-extra-kwargs/
        """
        # fetch the constructor's signature
        cls_fields = set(signature(cls).parameters)

        # split the kwargs into native ones and new ones
        native_args, new_args = {}, {}
        for name, val in kwargs.items():
            if name in cls_fields:
                native_args[name] = val
            else:
                new_args[name] = val

        # use the native ones to create the class ...
        ret = cls(**native_args)
        extra_kwargs = {}

        # ... and add the new ones by hand
        for new_name, new_val in new_args.items():
            setattr(ret, new_name, new_val)
            extra_kwargs[new_name] = new_val
        ret.__extra_kwargs__ = extra_kwargs

        return ret

    element.from_kwargs = classmethod(from_kwargs)
    registry.register(element)
    return element


def get_base_type(type_: type) -> Any:
    """
    Extract the most basic type from complex type annotations.

    This function handles various typing constructs including:
    - Optional types (Union[T, None])
    - List types (list[T])
    - Dictionary types (dict[K, V])
    - Union types (Union[T1, T2, ...])

    Examples:
        Optional[list[str]] -> str
        list[str] -> str
        str -> str
        list[dict[str, int]] -> dict
        Union[int, float] -> Raises ValueError (multiple non-None types)

    Args:
        type_: The type annotation to extract the base type from

    Returns:
        The base type

    Raises:
        ValueError: If Union contains multiple non-None types
    """
    origin = get_origin(type_)
    args = get_args(type_)

    # Handle simple types without origin
    if origin is None:
        return type_

    # Handle Optional (Union with None) types
    if origin is Union:
        # Filter out None type
        non_none_args = tuple(arg for arg in args if arg is not type(None))

        # Handle empty args after filtering
        if not non_none_args:
            return None

        # Handle multiple non-None types in Union
        if len(non_none_args) > 1:
            raise ValueError(f"Cannot handle multiple types in Union: {non_none_args}")

        # Recursively get base type of the remaining argument
        return get_base_type(non_none_args[0])

    # Handle list type
    if origin is list:
        return get_base_type(args[0]) if args else list
    # Handle dict type
    return dict if origin is dict else type_
