"""Type declarations for Moodle plugins."""

from collections import defaultdict
from enum import StrEnum, auto
from graphlib import TopologicalSorter
from typing import Any, Dict, Mapping, Optional

from pydantic import BaseModel, ConfigDict, Field

from pybpmn_parser.bpmn.types import NAMESPACES
from pybpmn_parser.core import QName


class UndefinedType:
    """Represents an undefined value."""

    def __repr__(self):
        return "Undefined"

    def __bool__(self):
        return False


Undefined = UndefinedType()


def lower_first_char(string: str) -> str:
    """Lower the first character of a string."""
    return string[0].lower() + string[1:]


class LiteralValue(BaseModel):
    """A Moddle literal value."""

    name: str = Field(..., description="Value of the literal.")


class ModdleEnumeration(BaseModel):
    """A Moddle enumeration."""

    name: str = Field(..., description="Name of the enumeration.")
    literal_values: list[LiteralValue] = Field(..., alias="literalValues", description="Values of the enumeration.")


class TypeProperty(BaseModel):
    """The definition of a Moddle type property."""

    name: str = Field(..., description="Name of the property.")
    type: str = Field(..., description="Type of the property.")
    description: Optional[str] = Field(default=None, description="Description of the property.")
    is_attr: bool = Field(alias="isAttr", default=False, description="Is the property serialized as XML attribute?.")
    is_id: bool = Field(alias="isId", default=False, description="Is current property map to XML node id?")
    is_many: bool = Field(alias="isMany", default=False, description="Is the property an array or a single?")
    is_body: bool = Field(alias="isBody", default=False, description="Is the property serialized as body element?")
    is_reference: bool = Field(
        alias="isReference", default=False, description="Is the property referencing to another element?"
    )
    is_virtual: bool = Field(
        alias="isVirtual", default=False, description="Is the property a virtual property (not serialized)?"
    )
    default: Any = Field(default=Undefined, description="Default value of the property.")
    redefines: Optional[str] = Field(default=None, description="Name of the property to redefine.")
    replaces: Optional[str] = Field(default=None, description="Name of the property to replace.")
    xml: Optional[Mapping[str, str]] = Field(default=None, description="Defines XML serialization details.")
    normalized_name: Optional[QName] = Field(
        default=None, description="Normalized name of the property. Set during property registration.", exclude=True
    )
    normalized_type: Optional[QName] = Field(
        default=None, description="Normalized type of the property. Set during property registration.", exclude=True
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ModdleTypeMeta(BaseModel):
    """Metadata about a Moddle type."""

    allowed_in: list[str] = Field(
        ..., alias="allowedIn", description="List of elements this plugin type is allowed in."
    )


class ModdleType(BaseModel):
    """A Moddle type that is part of a Moddle package."""

    name: str = Field(..., description="Name of the type.")
    tag: Optional[str] = Field(default=None, description="XML tag name to parse.")
    description: Optional[str] = Field(default=None, description="Description of the type.")
    superClass: list[str] = Field(default_factory=list, description="Names of the super classes.")
    extends: Optional[list[str]] = Field(default_factory=list, description="Name of the type to extend.")
    isAbstract: bool = Field(default=False, description="Is the type abstract?")
    meta: Optional[ModdleTypeMeta] = Field(default=None, description="Metadata about this plugin type.")
    properties: list[TypeProperty] = Field(default_factory=list, description="Properties contained in the type.")
    normalized_name: Optional[QName] = Field(
        default=None, description="Normalized name of the type. Set during type registration.", exclude=True
    )
    traits: Optional[list[QName]] = Field(
        default_factory=list, description="Traits described by other type's extends property.", exclude=True
    )
    package: Optional["ModdlePackage"] = Field(
        default=None, description="The package this type belongs to. Set during registration."
    )
    normalized_extends: Optional[list[QName]] = Field(
        default=None, description="Normalized extends of the type. Set during registration.", exclude=True
    )
    normalized_superclass: Optional[list[QName]] = Field(
        default=None, description="Normalized superclass of the type. Set during registration.", exclude=True
    )


class XMLSerialization(BaseModel):
    """Defines XML serialization details."""

    tag_alias: str = Field(default="lowerCase", alias="tagAlias")
    type_prefix: Optional[str] = Field(default=None, alias="typePrefix")


class ModdlePackage(BaseModel):
    """A Moddle package that extends BPMN."""

    name: str = Field(..., description="Name of the package.")
    prefix: str = Field(
        ..., description="The prefix uniquely identifies elements in a package if more multiple packages are in place."
    )
    uri: str = Field(..., description="The associated XML namespace URI.")
    xml: Optional[XMLSerialization] = Field(default=None, description="Defines XML serialization details.")
    types: list[ModdleType] = Field(..., description="Types contained in the package.")
    enumerations: list[ModdleEnumeration] = Field(
        default_factory=list, description="Enumerations contained in the package."
    )
    enums: Optional[dict[str, StrEnum]] = Field(
        default_factory=dict, description="Python StrEnums from enumerations defined in the package."
    )

    def model_post_init(self, context: Any, /) -> None:
        """Finish initialization of the types and their properties."""
        nsmap = {self.prefix: self.uri, **NAMESPACES}
        self.finalize_enums()
        for moddle_type in self.types:
            self.finalize_type(moddle_type, nsmap)

    def finalize_enums(self) -> None:
        """Finalize the enumeration definitions."""
        self.enums = {}
        for enumeration in self.enumerations:
            values = [(literal.name, auto()) for literal in enumeration.literal_values]
            self.enums[enumeration.name] = StrEnum(enumeration.name, values)

    def finalize_type(self, moddle_type: ModdleType, nsmap: dict[str, str]) -> None:
        """Finish setting up a Moddle type."""
        moddle_type.normalized_name = QName.from_str(moddle_type.name, nsmap=nsmap, default_prefix=self.prefix)

        if not moddle_type.tag:
            moddle_type.tag = (
                lower_first_char(moddle_type.normalized_name.local)
                if self.use_lowercase
                else moddle_type.normalized_name.local
            )

        for prop in moddle_type.properties:
            prop.normalized_name = QName.from_str(prop.name, nsmap=nsmap, default_prefix=self.prefix)
            prop.normalized_type = QName.from_str(prop.type, nsmap=nsmap, default_prefix=self.prefix)

        moddle_type.normalized_extends = [
            _normalize_name(extend, nsmap=nsmap, default_prefix=self.prefix) for extend in moddle_type.extends
        ]
        moddle_type.normalized_superclass = [
            _normalize_name(superclass, nsmap=nsmap, default_prefix=self.prefix)
            for superclass in moddle_type.superClass
        ]
        moddle_type.package = self

    def get_type_by_name(self, name: str) -> Optional[ModdleType | StrEnum]:
        """Get a Moddle plugin by name."""
        type_name = name.replace(f"{self.prefix}:", "")
        for type_ in self.types:
            if type_.name == type_name:
                return type_
        if type_name in self.enums:
            return self.enums[type_name]
        return None

    @property
    def use_lowercase(self) -> bool:
        """Check if the property name should be lowercased."""
        return self.xml.tag_alias == "lowerCase" if self.xml else False

    def package_dependencies(self) -> tuple[str, ...]:
        """Return the package URIs this package depends on."""
        d_tree = self.type_dependency_tree()
        unique_deps = {name.uri for name in d_tree}
        return tuple(unique_deps)

    def type_dependencies(self) -> dict[QName, set[QName]]:
        """A dictionary of type names and their dependencies."""
        graph = defaultdict(set)
        for moddle_type in self.types:
            type_q_name = moddle_type.normalized_name
            for super_class in moddle_type.normalized_superclass:
                graph[type_q_name].add(super_class)
            for prop in moddle_type.properties:
                if prop.type != moddle_type.name and not prop.is_reference:
                    graph[type_q_name].add(prop.normalized_type)
            for extend in moddle_type.normalized_extends:
                graph[type_q_name].add(extend)

        return graph

    def type_dependency_tree(self) -> tuple[QName, ...]:
        """Create a dependency tree for this package's types in the correct order."""
        graph = self.type_dependencies()
        ts = TopologicalSorter[QName](graph)
        return tuple(ts.static_order())


def _normalize_name(name: str, nsmap: dict[str, str], default_prefix: str) -> QName:
    """Normalize a name."""
    if name.startswith("bpmn:") or name.startswith("di:"):
        prefix, local = name.split(":", 1)
        local = lower_first_char(local)
        name = f"{prefix}:{local}"
    return QName.from_str(name, nsmap=nsmap, default_prefix=default_prefix)


BUILTIN_TYPES = {
    "String": str,
    "Integer": int,
    "Boolean": bool,
    "Real": float,
    "dict": Dict[str, str],
}
