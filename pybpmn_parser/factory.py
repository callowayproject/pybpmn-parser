"""A factory to create BPMN elements from an XML dictionary."""

import re
from typing import Any, Callable, Optional

from pydantic.alias_generators import to_snake

from pybpmn_parser.bpmn.infrastructure.definitions import Definitions
from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.core import QName
from pybpmn_parser.element_registry import ElementDescriptor, registry

IGNORE_ATTRIBUTES = re.compile(r"@xmlns:.+")


SCALAR_CONVERTER: dict[str, Callable[[str], Any]] = {
    "str": str,
    "int": int,
    "float": float,
    "bool": lambda x: x.lower() == "true",
}


def attr_is_ignored(attr_name: str) -> bool:
    """
    Check if an attribute is ignored.

    Args:
        attr_name: The name of the attribute to check.

    Returns:
        True if the attribute is ignored, False otherwise.
    """
    return attr_name in IGNORE_ATTRIBUTES.findall(attr_name)


def get_attribute_name(base_name: str, descriptor: ElementDescriptor, nsmap: dict[str, str]) -> QName:
    """
    Get the attribute name for the factory.
    """
    attr_name = base_name[1:] if base_name.startswith("@") else base_name
    qname = QName.from_str(attr_name, nsmap, default_uri=descriptor.q_name.uri)

    if qname.uri is None:
        qname = QName(local=qname.local, uri=descriptor.q_name.uri)

    return qname


def get_property_name(base_name: str, descriptor: ElementDescriptor, nsmap: dict[str, str]) -> str:
    """
    Get the property name for the factory.

    Args:
        base_name: The base name of the attribute.
        descriptor: The element descriptor.
        nsmap: The namespace map.

    Returns:
        The property name.
    """
    attr_name = base_name[1:] if base_name.startswith("@") else base_name
    qname = QName.from_str(attr_name, nsmap, default_uri=descriptor.q_name.uri)

    if qname.uri is None:
        qname = QName(local=qname.local, uri=descriptor.q_name.uri)

    if qname in descriptor.properties:
        return descriptor.properties[qname].property_name
    else:
        return to_snake(attr_name.replace(":", "_"))


def _handle_unknown_property(
    key: str,
    value: Any,
    descriptor: ElementDescriptor,
    parent_uri: str,
    ns_map: dict[str, str],
) -> dict[str, Any]:
    """
    Handles an unknown property found during element processing.

    This function processes a given key and its corresponding value that do not match
    directly to any recognized property descriptor. It attempts to resolve and map the key
    to a known attribute name or property using the descriptor and namespace map. If the
    attribute descriptor is identified, it creates new elements from the given value and
    maps them properly. If no descriptor is identified, the key-value pair is added as is
    to the provided item values.

    Arguments:
        key: The property key being evaluated.
        value: The associated value with the property key, which can be a list or a raw value.
        descriptor: Descriptor providing information about the current element's structure.
        parent_uri: URI of the parent element in the hierarchy.
        ns_map: Dictionary providing namespace mapping for resolution of keys.

    Returns:
        A dictionary containing the updated property values.
    """
    property_name = get_property_name(key, descriptor, ns_map)
    attr_name = get_attribute_name(key, descriptor, ns_map)
    attr_descriptor = registry.by_qname.get(attr_name)
    new_values: dict[str, Any] = {}

    if attr_descriptor:
        if isinstance(value, list):
            new_values[property_name] = [
                create_element_from_dict(child_val, attr_descriptor, parent_uri, ns_map) for child_val in value
            ]
        else:
            new_values[property_name] = create_element_from_dict(value, attr_descriptor, parent_uri, ns_map)
    else:
        # Unknown to the registry as well: keep raw value
        new_values[property_name] = value

    return new_values


def _handle_known_property(
    key: str,
    value: Any,
    descriptor: ElementDescriptor,
    parent_uri: str,
    ns_map: dict[str, str],
) -> dict[str, Any]:
    """
    Handles known properties of an element descriptor and updates item values.

    This function processes an XML element's key-value pair to map them to the
    corresponding property of an element descriptor. It supports scalar
    conversion, attributes without child elements, and child elements with
    possible nested descriptors. The function updates the item's values based on
    the processed property information.

    Args:
        key: The key representing the XML element.
        value: The value associated with the given XML element.
        descriptor: The descriptor that defines the properties of the XML element.
        parent_uri: A parent URI to resolve relative paths.
        ns_map: A dictionary mapping namespace prefixes to their URIs.

    Raises:
        KeyError: If the property descriptor for the given key cannot be found.

    Returns:
        A dictionary containing the updated property values.
    """
    properties = descriptor.properties
    property_name = get_property_name(key, descriptor, ns_map)
    attr_name = get_attribute_name(key, descriptor, ns_map)
    prop_descriptor = properties[attr_name]
    new_values: dict[str, Any] = {}

    # Scalar conversion
    if prop_descriptor.type in SCALAR_CONVERTER:
        new_values[property_name] = SCALAR_CONVERTER[prop_descriptor.type](value)
        return new_values

    # Simple attribute (no child elements)
    if prop_descriptor.is_attr:
        new_values[property_name] = value
        return new_values

    # Child element(s)
    child_qname = get_child_qname(attr_name, descriptor, key, ns_map)
    child_descriptor = registry.by_qname.get(child_qname)
    new_values[property_name] = get_child_value(
        value,
        child_descriptor,
        prop_descriptor.is_many,
        ns_map,
        parent_uri,
    )
    return new_values


def create_element_from_dict(
    element_dict: dict, descriptor: ElementDescriptor, parent_uri: str, nsmap: Optional[dict[str, str]] = None
) -> Any:
    """Create a BPMN element from a dictionary representation.

    Args:
        element_dict: A dictionary representing a BPMN element.
        descriptor: A descriptor for the BPMN element.
        parent_uri: The URI of the parent BPMN element.
        nsmap: An optional namespace map for resolving prefixed element names.

    Returns:
        The created BPMN element, or None if the element type is not supported.
    """
    if element_dict is None:
        return None

    if isinstance(element_dict, str):
        element_dict = {"#text": element_dict}

    if not isinstance(element_dict, dict):
        raise TypeError(f"element_dict must be a dictionary, not {type(element_dict)}, {element_dict}")

    ns_map = extract_nsmap_from_dict(element_dict, nsmap)

    item_values: dict[str, Any] = {}  # The values passed to the element constructor
    properties = descriptor.properties

    for key, value in element_dict.items():
        if attr_is_ignored(key):
            continue

        attr_name = get_attribute_name(key, descriptor, ns_map)
        if attr_name not in properties:
            item_values |= _handle_unknown_property(key, value, descriptor, parent_uri, ns_map)
            continue

        item_values |= _handle_known_property(key, value, descriptor, parent_uri, ns_map)

    return descriptor.type.from_kwargs(**item_values)


def get_child_value(
    value: Any, child_descriptor: Any | None, is_many: bool, ns_map: dict[str, str], parent_uri: str
) -> Any:
    """
    Processes a value and its descriptor to generate the corresponding child element or list of child elements.

    This function determines if the given value and descriptor should generate a single child element
    or a list of elements and applies transformations accordingly. It can handle cases where the value
    is already a list or needs to be wrapped as a single element.

    Args:
        value: The base value to process.
        child_descriptor: Descriptor providing details about how the value maps to a child element. If None, the
            original value is returned as-is.
        is_many: Indicates whether the descriptor expects multiple child elements.
        ns_map: A dictionary mapping namespace prefixes to their corresponding URIs.
        parent_uri: The parent namespace URI for the resulting child elements.

    Returns:
        A processed value representing either a single child element or a list of child elements
        based on the descriptor and the provided input.
    """
    if child_descriptor is None:
        return value
    elif is_many or isinstance(value, list):
        if not isinstance(value, list):
            value = [value]
        return [create_element_from_dict(item, child_descriptor, parent_uri, ns_map) for item in value]
    else:
        return create_element_from_dict(value, child_descriptor, parent_uri, ns_map)


def get_child_qname(attr_name: QName, descriptor: ElementDescriptor, key: str, ns_map: dict[str, str]) -> QName | None:
    """
    Compute the qualified name (QName) for a child element based on the provided information.

    This function determines the QName using the type_qname from the descriptor if
    available. If the type_qname is not present, it parses the QName from the key
    according to the provided namespace mapping.

    Args:
        attr_name: The qualified name of the attribute to process.
        descriptor: The element descriptor containing metadata about the element properties.
        key: The string representation of the child element name.
        ns_map: The namespace map to use for resolving the QName.

    Returns:
        The computed QName of the child element. Returns None if the QName cannot be resolved.
    """
    return descriptor.properties[attr_name].type_qname or QName.from_str(key, ns_map)


def extract_nsmap_from_dict(element_dict: dict, nsmap: dict[str, str] | None) -> dict[str, str]:
    """Extract a namespace map from an XML dictionary."""
    xmlns_keys = [key for key in element_dict if key.startswith("@xmlns")]
    ns_map = nsmap.copy() if nsmap else {}
    for xmlns_key in xmlns_keys:
        if ":" in xmlns_key:
            prefix = xmlns_key.split(":")[1]
            ns_map[prefix] = element_dict[xmlns_key]
        else:
            ns_map["default"] = element_dict[xmlns_key]
    return ns_map


def create_bpmn(root_xml_dict: dict, initial_nsmap: Optional[dict[str, str]] = None) -> Definitions:
    """
    Create a BPMN element from a root XML dictionary.

    Pass the dict resulting from xmltodict.

    Args:
        root_xml_dict: A root XML dictionary.
        initial_nsmap: An optional namespace map for resolving prefixed element names.

    Returns:
        The created BPMN element, or None if the element type is not supported.
    """
    nsmap = NAMESPACES.copy()
    initial_nsmap = initial_nsmap or {}
    nsmap.update(initial_nsmap)
    output = []

    for key, value in root_xml_dict.items():
        nsmap.update(extract_nsmap_from_dict(value, nsmap))
        default_uri = nsmap.get("default", None)
        qname = QName.from_str(key, nsmap, default_uri=default_uri)
        descriptor = registry.by_qname[qname]
        output.append(create_element_from_dict(value, descriptor, qname.uri, nsmap))

    if not output:
        raise ValueError("No BPMN definitions found.")
    if len(output) > 1:
        raise ValueError("Expected exactly one BPMN definition, but found multiple.")
    return output[0]
