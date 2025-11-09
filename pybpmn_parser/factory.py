"""A factory to create BPMN elements from an XML dictionary."""

import re
from typing import Any, Callable, Optional

from pydantic.alias_generators import to_snake

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

    item_values = {}  # The values passed to the element constructor

    for key, value in element_dict.items():
        if attr_is_ignored(key):
            continue
        property_name = get_property_name(key, descriptor, ns_map)
        attr_name = get_attribute_name(key, descriptor, ns_map)
        is_known_property = attr_name in descriptor.properties

        if not is_known_property:
            attr_descriptor = registry.by_qname.get(attr_name, None)
            if attr_descriptor:
                if isinstance(value, list):
                    item_values[property_name] = [
                        create_element_from_dict(child_val, registry.by_qname[attr_name], parent_uri, ns_map)
                        for child_val in value
                    ]
                else:
                    item_values[property_name] = create_element_from_dict(
                        value, registry.by_qname[attr_name], parent_uri, ns_map
                    )
            else:
                item_values[property_name] = value
            continue

        property_type = descriptor.properties[attr_name].type
        if property_type in SCALAR_CONVERTER:
            item_values[property_name] = SCALAR_CONVERTER[property_type](value)
            continue

        if descriptor.properties[attr_name].is_attr:
            item_values[property_name] = value
            continue

        child_qname = get_child_qname(attr_name, descriptor, key, ns_map)
        child_descriptor = registry.by_qname.get(child_qname)
        is_many = descriptor.properties[attr_name].is_many

        item_values[property_name] = get_child_value(value, child_descriptor, is_many, ns_map, parent_uri)

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
        child_value = value
    elif is_many or isinstance(value, list):
        if not isinstance(value, list):
            value = [value]
        child_value = [create_element_from_dict(item, child_descriptor, parent_uri, ns_map) for item in value]
    else:
        child_element = create_element_from_dict(value, child_descriptor, parent_uri, ns_map)
        child_value = child_element
    return child_value


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
    if descriptor.properties[attr_name].type_qname:
        child_qname = descriptor.properties[attr_name].type_qname
    else:
        child_qname = QName.from_str(key, ns_map)
    return child_qname


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


def create_bpmn(root_xml_dict: dict, initial_nsmap: Optional[dict[str, str]] = None) -> Any:
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

    return output
