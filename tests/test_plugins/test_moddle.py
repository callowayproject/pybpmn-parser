"""Unit tests for the plugins module."""

import pytest

from pybpmn_parser.core import QName
from pybpmn_parser.element_registry import registry as element_registry
from pybpmn_parser.plugins.moddle import ModdleRegistry
from pybpmn_parser.plugins.moddle_types import BUILTIN_TYPES, ModdlePackage, ModdleType


class TestTypeIsRegistered:
    """Unit tests for the _type_is_registered method."""

    def test_registered_in_type_map(self, mocker):
        """Test when the type is in the type_map."""
        registry = ModdleRegistry()
        type_q_name = QName(local="TestType", uri="http://example.com")
        mocker.patch.object(registry, "type_map", {type_q_name: object()})

        result = registry._type_is_registered(type_q_name)
        assert result is True

    def test_registered_in_element_registry(self, mocker):
        """Test when the URI is in registered namespaces."""
        registry = ModdleRegistry()
        type_q_name = QName(local="OtherType", uri="http://example.org")
        mocker.patch.object(element_registry, "registered_namespaces", {"http://example.org"})

        result = registry._type_is_registered(type_q_name)
        assert result is True

    def test_registered_in_builtin_types(self):
        """Test when the local name is in BUILTIN_TYPES."""
        registry = ModdleRegistry()
        local_type_name = next(iter(BUILTIN_TYPES))  # Pick any existing built-in type
        type_q_name = QName(local=local_type_name)

        result = registry._type_is_registered(type_q_name)
        assert result is True

    def test_registered_as_element(self):
        """Test when the local name is 'Element'."""
        registry = ModdleRegistry()
        type_q_name = QName(local="Element")

        result = registry._type_is_registered(type_q_name)
        assert result is True

    def test_not_registered(self):
        """Test when the type is not registered."""
        registry = ModdleRegistry()
        type_q_name = QName(local="UnknownType", uri="http://not-registered.com")

        result = registry._type_is_registered(type_q_name)
        assert result is False


class TestRegisterPackage:
    """Tests for the register_package method in ModdleRegistry."""

    def test_register_valid_package(self):
        """Test registering a valid Moddle package."""
        registry = ModdleRegistry()
        moddle_type = ModdleType(name="TestType", tag="testTag")
        package = ModdlePackage(name="TestPackage", prefix="tp", uri="http://example.com", types=[moddle_type])

        registry.register_package(package)
        assert registry.package_map["tp"] == package
        assert registry.package_map["http://example.com"] == package

    def test_register_duplicate_package(self):
        """Test handling of duplicate package registration."""
        registry = ModdleRegistry()
        package = ModdlePackage(name="TestPackage", prefix="tp", uri="http://example.com", types=[])
        registry.register_package(package)

        # Attempt to register the same package again
        registry.register_package(package)
        assert len(registry.packages) == 1

    def test_register_package_with_dependencies(self):
        """Test registering a package with dependencies."""
        registry = ModdleRegistry()
        dependency_package = ModdlePackage(
            name="DependencyPackage", prefix="dep", uri="http://dependency.com", types=[]
        )
        dependent_package = ModdlePackage(
            name="DependentPackage",
            prefix="depPkg",
            uri="http://dependent.com",
            types=[],
        )

        # Add dependency to the registry
        registry.register_package(dependency_package)
        # Ensure registration doesn't fail if dependency already exists
        registry.register_package(dependent_package)

        assert "dep" in registry.package_map
        assert "depPkg" in registry.package_map

    def test_register_package_with_unknown_dependency(self):
        """Test registering a package with an unknown dependency raises an error."""
        registry = ModdleRegistry()
        moddle_type = ModdleType(name="TestType", tag="testTag", superClass=["{http://example.com}superClass"])
        package_with_dependency = ModdlePackage(
            name="TestPackageWithDependency",
            prefix="tpd",
            uri="http://example-with-dependency.com",
            types=[moddle_type],
        )

        with pytest.raises(ValueError, match="Unknown package dependency"):
            registry.register_package(package_with_dependency)

    def test_register_package_with_unknown_type(self):
        """Test registering a package with an unknown type raises an error."""
        registry = ModdleRegistry()
        moddle_type = ModdleType(name="UnknownType", tag="UnknownTag", superClass=["UnknownSuperClass"])
        invalid_package = ModdlePackage(
            name="InvalidPackage",
            prefix="inv",
            uri="http://invalid.com",
            types=[moddle_type],
        )

        with pytest.raises(ValueError, match="Unknown type"):
            registry.register_package(invalid_package)
