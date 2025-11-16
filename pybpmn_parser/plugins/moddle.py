"""This module provides parsers for Moddle's JSON-based definition files."""

import json
import keyword
from dataclasses import Field, dataclass, field, make_dataclass
from enum import EnumType, StrEnum
from graphlib import TopologicalSorter
from itertools import chain
from pathlib import Path
from typing import Any, List, Optional

from pydantic.alias_generators import to_snake

from pybpmn_parser.core import QName
from pybpmn_parser.element_registry import register_element
from pybpmn_parser.element_registry import registry as element_registry
from pybpmn_parser.plugins.moddle_types import (
    BUILTIN_TYPES,
    ModdlePackage,
    ModdleType,
    TypeProperty,
    XMLSerialization,
    lower_first_char,
)

dc_moddle = ModdlePackage(
    name="DC", prefix="dc", uri="http://www.omg.org/spec/DD/20100524/DC", xml=None, types=[], enumerations=[]
)

di_moddle = ModdlePackage(
    name="DI",
    prefix="di",
    uri="http://www.omg.org/spec/DD/20100524/DI",
    xml=XMLSerialization(tagAlias="lowerCase", typePrefix=None),
    types=[],
    enumerations=[],
)

bpmndi_moddle = ModdlePackage(
    name="BPMNDI", prefix="bpmndi", uri="http://www.omg.org/spec/BPMN/20100524/DI", xml=None, types=[], enumerations=[]
)

bpmn_moddle = ModdlePackage(
    name="BPMN20",
    prefix="bpmn",
    uri="http://www.omg.org/spec/BPMN/20100524/MODEL",
    xml=XMLSerialization(tagAlias="lowerCase", typePrefix="t"),
    types=[],
    enumerations=[],
)


class ModdleRegistry:
    """Registry for Moddle packages."""

    def __init__(self):
        self.packages: list[ModdlePackage] = []
        """List of all Moddle packages."""

        self.namespace_map: dict[str, str] = {}
        """Mapping of namespace prefixes to their URIs."""

        self.package_map: dict[str, Optional[ModdlePackage]] = {
            "http://www.omg.org/spec/BPMN/20100524/MODEL": bpmn_moddle,  # BPMN placeholder
            "http://www.omg.org/spec/BPMN/20100524/DI": bpmndi_moddle,  # BPMNDI placeholder
            "http://www.omg.org/spec/DD/20100524/DC": dc_moddle,  # DC placeholder
            "http://www.omg.org/spec/DD/20100524/DI": di_moddle,  # DI placeholder
        }
        """Mapping of package prefixes and package URIs to its extension parser class."""

        self.type_map: dict[QName, ModdleType | EnumType] = {}
        """Mapping of type names to their extension parser class."""

    def _type_is_registered(self, type_q_name: QName) -> bool:
        """Check if a type is registered."""
        if type_q_name in self.type_map:
            return True
        if type_q_name.uri in element_registry.registered_namespaces:
            return True
        if type_q_name.local in BUILTIN_TYPES:
            return True
        return type_q_name.local == "Element"

    def register_package(self, package: ModdlePackage) -> None:
        """Register a Moddle package."""
        if package.prefix in self.package_map or package.uri in self.package_map:
            return

        for pkg in package.package_dependencies():
            if pkg not in self.package_map and pkg != package.uri:
                raise ValueError(f"Unknown package dependency: {pkg}")

        self.package_map[package.prefix] = package
        self.package_map[package.uri] = package
        self.namespace_map[package.prefix] = package.uri
        self.packages.append(package)

        for type_q_name in package.type_dependency_tree():
            if self._type_is_registered(type_q_name):
                continue
            moddle_type = package.get_type_by_name(type_q_name.local)
            if isinstance(moddle_type, (ModdleType, EnumType)):
                self.type_map[type_q_name] = moddle_type
            else:
                raise ValueError(f"Unknown type: {type_q_name}")

    def get_type(self, type_q_name: QName) -> Any:
        """Get a Moddle type by name."""
        if type_q_name in self.type_map:
            return self.type_map[type_q_name]

        for package in self.packages:
            type_ = package.get_type_by_name(type_q_name.local)
            if type_:
                return type_

        return None

    def dependency_tree(self) -> tuple[QName, ...]:
        """Create a dependency tree for parsing ModdlePlugins in the correct order."""
        graph = {}
        for package in self.packages:
            graph.update(package.type_dependencies())
        ts = TopologicalSorter[QName](graph)
        return tuple(ts.static_order())


registry = ModdleRegistry()
"""The Moddle registry."""


def filter_package_types(package: ModdlePackage) -> list[ModdleType]:
    """Convert a Moddle package into BPMN elements."""
    valid_types = []
    for type_ in package.type_dependency_tree():
        # Don't include built-in types. "Element" is a BPMN Extension.
        if type_.local in BUILTIN_TYPES or type_.local == "Element":
            continue

        # Check if types from other packages are already registered.
        if type_.uri != package.uri:
            type_name = QName(local=lower_first_char(type_.local), uri=type_.uri)
            if type_name in element_registry.by_qname:
                continue
            else:  # pragma: no cover
                print(f"Unknown type: {type_name}")
                continue

        moddle_type = package.get_type_by_name(type_.local)
        if isinstance(moddle_type, ModdleType):
            # Skip types that extend another type.
            if moddle_type.extends:
                continue
            valid_types.append(moddle_type)
        elif isinstance(moddle_type, StrEnum):
            # Skip enums
            continue
        else:
            print(f"Unknown type: {type_} ({type(moddle_type)})")
    return valid_types


def convert_moddle_registry() -> None:
    """Register all Moddle extension types."""
    type_order = registry.dependency_tree()
    filtered_types = {
        typ_.normalized_name for typ_ in chain.from_iterable([filter_package_types(pkg) for pkg in registry.packages])
    }

    for moddle_type_name in type_order:
        if moddle_type_name not in filtered_types:
            continue
        local_name = moddle_type_name.local
        if local_name in BUILTIN_TYPES:
            continue

        moddle_type = registry.get_type(moddle_type_name)
        if isinstance(moddle_type, ModdleType):
            parser = convert_moddle_to_element(moddle_type)
            register_element(parser)


@dataclass
class DataclassField:
    """Dataclass field representation."""

    name: str
    type: Any
    field: Field


def convert_moddle_to_element(definition: ModdleType) -> type:
    """
    Create an Element dataclass model for a Moddle extension type.

    Args:
        definition: ModdlePlugin definition

    Returns:
        A dynamically created dataclass model
    """
    cls_tag = lower_first_char(definition.tag) if definition.package.use_lowercase else definition.tag
    ns_uri = definition.normalized_name.uri
    cls_name = definition.name
    base_classes = get_parser_base_classes(definition) or ()
    meta_class = type("Meta", (), {"namespace": ns_uri, "name": cls_tag})

    dataclass_fields = convert_moddle_properties(definition)
    dc_fields_as_tuple = [(dc.name, dc.type, dc.field) for dc in dataclass_fields]
    return make_dataclass(
        cls_name, dc_fields_as_tuple, bases=base_classes, namespace={"Meta": meta_class}, kw_only=True
    )


def convert_moddle_properties(definition: ModdleType) -> list[DataclassField]:
    """
    Converts a Moddle definition's properties into corresponding dataclass fields.

    This function processes the properties of a given ModdleType definition. It validates
    type information, detects circular references, and resolves field types based on the
    provided element registry. Depending on the property type (attributes, elements, or
    text body), it constructs the appropriate dataclass field representation. If an
    unknown field type or mismatched references are encountered, an error is raised.
    The resulting fields are useful for creating dataclass representations from Moddle definitions.

    Args:
        definition: The Moddle definition containing properties to be processed.

    Returns:
        A list of dataclass field representations corresponding to the Moddle definition's properties.

    Raises:
        ValueError: If a field has an unknown or unresolved type or any unsupported format.
    """
    dataclass_fields: list[DataclassField] = []

    for fld in definition.properties:
        is_builtin = fld.normalized_type.local in BUILTIN_TYPES

        if fld.type == definition.name:  # Avoid circular references
            continue

        if fld.normalized_type in element_registry.by_qname:
            missing_type = False
        else:
            true_type = QName(local=lower_first_char(fld.normalized_type.local), uri=fld.normalized_type.uri)
            missing_type = true_type not in element_registry.by_qname

        if not is_builtin and missing_type and not fld.is_reference:
            raise ValueError(f"Unknown field type: {fld.normalized_type}")

        type_hint = get_property_type_hint(fld)
        fld_name = get_valid_name(fld.name)

        if fld.is_attr:
            field_def = DataclassField(
                name=fld_name,
                type=Optional[type_hint],
                field=field(default=fld.default, metadata={"name": fld.name, "type": "Attribute"}),
            )
        elif not fld.is_body and not fld.is_virtual:
            metadata_name = fld.normalized_type.local if fld.name != fld.normalized_type.local else fld.name
            metadata_name = lower_first_char(metadata_name) if definition.package.use_lowercase else metadata_name
            field_def = DataclassField(
                name=fld_name,
                type=Optional[type_hint],
                field=field(default=fld.default, metadata={"name": metadata_name, "type": "Element"}),
            )
        elif fld.is_body:
            field_def = DataclassField(
                name=fld_name,
                type=Optional[type_hint],
                field=field(default=fld.default, metadata={"name": "#text", "type": "Element"}),
            )
        else:
            raise ValueError(f"Unknown field type: {fld.type} ({type_hint}) for {fld.name}")

        dataclass_fields.append(field_def)
    return dataclass_fields


def get_property_type_hint(fld: TypeProperty) -> type:
    """
    Returns the appropriate type for a field based on its properties and the available types.

    Args:
        fld: PluginProperty object representing the field.

    Returns:
        The appropriate type hint for the field
    """
    if fld.is_reference:
        return str

    if fld.normalized_type.local in BUILTIN_TYPES:
        type_hint = BUILTIN_TYPES[fld.normalized_type.local]
    elif fld.normalized_type in element_registry.by_qname:
        type_hint = element_registry.by_qname[fld.normalized_type].type
    else:
        true_type = QName(local=lower_first_char(fld.normalized_type.local), uri=fld.normalized_type.uri)
        type_hint = element_registry.by_qname[true_type].type

    if fld.is_attr:
        return type_hint

    if fld.is_many:
        type_hint = List[type_hint]  # type: ignore[valid-type]

    return type_hint


def get_parser_base_classes(moddle_type: ModdleType) -> tuple[type, ...] | None:
    """Figure out the base classes for a Moddle extension type."""
    if not moddle_type.superClass:
        return None

    super_classes = filter_ignorable_superclasses(moddle_type.normalized_superclass)
    missing_classes = {class_name for class_name in super_classes if class_name not in element_registry.by_qname}
    final_missing_classes = set()

    for name in missing_classes:
        lowered_name = QName(local=lower_first_char(name.local), uri=name.uri)
        if lowered_name in element_registry.by_qname:
            super_classes.remove(name)
            super_classes.append(lowered_name)
        else:
            final_missing_classes.add(name)

    if final_missing_classes:
        raise ValueError(f"Unknown super class(es): {','.join(map(str, missing_classes))}")

    return tuple(element_registry.by_qname[super_class].type for super_class in super_classes)


def filter_ignorable_superclasses(super_classes: list[QName]) -> list[QName]:
    """Filter out classes that are ignorable."""
    classes = {sc for sc in super_classes if sc.local != "Element"}
    return list(classes)


def get_valid_name(name: str) -> str:
    """Get a valid name for a dataclass."""
    new_name = name.replace(":", "_")
    new_name = to_snake(new_name)
    return new_name if not keyword.iskeyword(new_name) else f"{new_name}_"


def load_moddle_file(file_path: Path) -> ModdlePackage:
    """Read a Moddle extension JSON file."""
    extension_contents = json.loads(file_path.read_text(encoding="utf-8"))
    pkg = ModdlePackage(**extension_contents)
    registry.register_package(pkg)
    return pkg
