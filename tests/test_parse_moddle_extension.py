from typing import List, Optional
from unittest.mock import create_autospec

import pytest
from pydantic_xml.serializers.factories.primitive import AttributeSerializer, ElementSerializer

from pybpmn_parser.plugins.moodle_types import ModdlePackage, ModdleType, TypeProperty
from pybpmn_parser.plugins.parse_moddle_extension import convert_moddle_to_extensions, create_plugin_model

AVAILABLE_TYPES = {"string": str, "integer": int}
NAMESPACE = "nspace"
NSMAP = {NAMESPACE: "http://example.com/schema"}


class TestConvertModdleToExtensions:
    """Unit tests for the convert_moddle_to_extensions function."""

    def test_convert_empty_package(self):
        """Test convert_moddle_to_extensions with an empty ModdlePackage."""
        package = create_autospec(ModdlePackage, instance=True)
        package.types = []
        package.prefix = "test"
        package.uri = "http://test.com"

        result = convert_moddle_to_extensions(package)
        assert result is None

    def test_convert_package_with_single_type(self):
        """Test convert_moddle_to_extensions where package has one type with no dependencies."""
        plugin_property = create_autospec(TypeProperty, instance=True)
        plugin_property.type = "TestType"
        plugin_property.is_attr = True
        plugin_property.name = "property1"

        moddle_plugin = create_autospec(ModdleType, instance=True)
        moddle_plugin.name = "TestType"
        moddle_plugin.superClass = []
        moddle_plugin.properties = [plugin_property]

        package = create_autospec(ModdlePackage, instance=True)
        package.types = [moddle_plugin]
        package.prefix = "test"
        package.uri = "http://test.com"

        result = convert_moddle_to_extensions(package)
        assert result is None  # Assuming function modifies in place, no return

    def test_convert_package_with_multiple_types(self):
        """Test convert_moddle_to_extensions with multiple types having dependencies."""
        plugin_prop1 = TypeProperty(name="prop1", type="BaseType", is_attr=False)
        plugin_prop2 = TypeProperty(name="prop2", type="DependentType", is_attr=False)
        base_type = ModdleType(name="BaseType", super_class=[], properties=[plugin_prop1])
        dependent_type = ModdleType(name="DependentType", super_class=["BaseType"], properties=[plugin_prop2])
        package = ModdlePackage(
            name="package", types=[base_type, dependent_type], prefix="test", uri="https://test.com"
        )

        result = convert_moddle_to_extensions(package)
        assert result is None  # Assuming function modifies in place, no return

    def test_convert_with_invalid_type(self):
        """Test convert_moddle_to_extensions with a type having unknown dependency."""
        plugin_property = create_autospec(TypeProperty, instance=True)
        plugin_property.type = "UnknownType"
        plugin_property.is_attr = False
        plugin_property.name = "property1"

        moddle_plugin = create_autospec(ModdleType, instance=True)
        moddle_plugin.name = "TestType"
        moddle_plugin.superClass = []
        moddle_plugin.properties = [plugin_property]

        package = create_autospec(ModdlePackage, instance=True)
        package.types = [moddle_plugin]
        package.prefix = "test"
        package.uri = "http://test.com"

        with pytest.raises(ValueError, match="Unknown field type: UnknownType"):
            convert_moddle_to_extensions(package)


class TestCreatePluginModel:
    """
    Unit tests for the create_plugin_model function.
    """

    def test_create_with_valid_definition(self):
        """Test creation of an extension type with valid inputs."""
        definition = ModdleType(
            name="TestType",
            properties=[
                TypeProperty(
                    name="attributeField",
                    type="string",
                    is_attr=True,
                    default="defaultValue",
                ),
                TypeProperty(
                    name="elementField",
                    type="integer",
                    is_attr=False,
                    is_body=False,
                    default=10,
                ),
            ],
        )

        result_type = create_plugin_model(definition, AVAILABLE_TYPES, NAMESPACE, NSMAP)
        instance = result_type(attribute_field="customValue", element_field=20)

        assert result_type.__name__ == "TestType"
        assert instance.attribute_field == "customValue"
        assert instance.element_field == 20

    def test_raises_error_with_unrecognized_field_type(self):
        """If the field type is unknown, raise an error."""
        definition = ModdleType(
            name="TestType",
            properties=[
                TypeProperty(
                    name="unknownField",
                    type="unknown",  # Type is not in AVAILABLE_TYPES
                    is_attr=True,
                ),
            ],
        )

        with pytest.raises(ValueError, match="Unknown field type: unknown"):
            create_plugin_model(definition, AVAILABLE_TYPES, NAMESPACE, NSMAP)

    def test_optional_field_has_optional_type(self):
        """The optional field should have an optional type."""
        definition = ModdleType(
            name="OptionalType",
            properties=[
                TypeProperty(name="optionalField", type="string", is_attr=True, default=""),
            ],
        )

        result_type = create_plugin_model(definition, AVAILABLE_TYPES, NAMESPACE, NSMAP)

        assert result_type.__annotations__ == {"optional_field": Optional[str]}
        instance = result_type()
        assert instance.optional_field == ""  # noqa: PLC1901

    def test_creates_list_field_when_is_many_is_true(self):
        """When is_many is true, the field should be a list."""
        definition = ModdleType(
            name="ListType",
            properties=[
                TypeProperty(
                    name="listField",
                    type="string",
                    is_attr=False,
                    is_many=True,
                ),
            ],
        )

        result_type = create_plugin_model(definition, AVAILABLE_TYPES, NAMESPACE, NSMAP)

        assert result_type.__annotations__ == {"list_field": List[str]}
        instance = result_type(list_field=["item1", "item2"])
        assert instance.list_field == ["item1", "item2"]

    def test_uses_attr_when_is_attr_is_true(self):
        """When is_attr is true, the field should be an attribute."""
        definition = ModdleType(
            name="AttrType",
            properties=[
                TypeProperty(
                    name="attrField",
                    type="string",
                    is_attr=True,
                ),
            ],
        )

        result_type = create_plugin_model(definition, AVAILABLE_TYPES, NAMESPACE, NSMAP)
        assert result_type.__annotations__ == {"attr_field": str}
        assert isinstance(result_type.__xml_serializer__._field_serializers["attr_field"], AttributeSerializer)
        instance = result_type(attr_field="value")
        assert instance.attr_field == "value"

    def test_uses_element_when_is_attr_and_is_body_are_false(self):
        """When is_attr and is_body are false, the field should be an element."""
        definition = ModdleType(
            name="AttrType",
            properties=[
                TypeProperty(
                    name="elementField",
                    type="string",
                ),
            ],
        )

        result_type = create_plugin_model(definition, AVAILABLE_TYPES, NAMESPACE, NSMAP)
        assert result_type.__annotations__ == {"element_field": str}
        assert isinstance(result_type.__xml_serializer__._field_serializers["element_field"], ElementSerializer)
        instance = result_type(element_field="value")
        assert instance.element_field == "value"

    def test_parses_xml_attributes(self):
        """Tests that XML attributes are correctly parsed and serialized."""
        definition = ModdleType(
            name="AttrType",
            properties=[
                TypeProperty(
                    name="attrField",
                    type="string",
                    is_attr=True,
                ),
            ],
        )
        xml_str = "<nspace:AttrType nspace:attrField='value' xmlns:nspace='http://example.com/schema'/>"

        result_type = create_plugin_model(definition, AVAILABLE_TYPES, NAMESPACE, NSMAP)

        result = result_type.from_xml(xml_str)
        assert result.attr_field == "value"

    def test_parses_xml_body(self):
        """Tests that XML bodies are correctly parsed and serialized."""
        definition = ModdleType(
            name="BodyType",
            properties=[
                TypeProperty(
                    name="bodyField",
                    type="string",
                    is_body=True,
                ),
            ],
        )
        xml_str = """
        <nspace:BodyType xmlns:nspace="http://example.com/schema">
            value
        </nspace:BodyType>
        """

        result_type = create_plugin_model(definition, AVAILABLE_TYPES, NAMESPACE, NSMAP)

        result = result_type.from_xml(xml_str)
        assert result.body_field == "value"

    def test_parses_element(self):
        """Tests that XML elements are correctly parsed and serialized."""
        definition = ModdleType(
            name="BodyType",
            properties=[
                TypeProperty(
                    name="elementField",
                    type="string",
                ),
            ],
        )
        xml_str = """
        <nspace:BodyType xmlns:nspace="http://example.com/schema">
            <nspace:elementField>value</nspace:elementField>
        </nspace:BodyType>
        """

        result_type = create_plugin_model(definition, AVAILABLE_TYPES, NAMESPACE, NSMAP)

        result = result_type.from_xml(xml_str)
        assert result.element_field == "value"

    def test_inherits_from_declared_super_class(self):
        """Tests that the plugin inherits from the declared super class."""
        superclass = ModdleType(
            name="SuperType",
            properties=[
                TypeProperty(
                    name="superField",
                    type="string",
                    is_attr=True,
                ),
            ],
        )
        modelclass = ModdleType(
            name="MyModel",
            super_class=["SuperType"],
            properties=[
                TypeProperty(
                    name="myField",
                    type="string",
                    is_attr=True,
                )
            ],
        )
        super_type = create_plugin_model(superclass, AVAILABLE_TYPES, NAMESPACE, NSMAP)
        available_types = {"SuperType": super_type, **AVAILABLE_TYPES}
        result_type = create_plugin_model(modelclass, available_types, NAMESPACE, NSMAP)

        assert issubclass(result_type, super_type)
