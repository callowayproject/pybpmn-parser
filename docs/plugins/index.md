# Plugin Development Guide

PyBPMN Parser features a flexible plugin system that allows you to extend its functionality to support vendor-specific BPMN extensions and custom validation rules.

## What are Plugins?

Plugins are Python modules that extend PyBPMN Parser's capabilities by:

- **Adding support for vendor-specific extensions** (e.g., Camunda, Activiti, jBPM)
- **Registering custom namespaces** for proprietary BPMN elements
- **Extending element classes** with additional attributes and behaviors
- **Implementing custom validation rules** for domain-specific requirements

## When to Create a Plugin

Consider creating a plugin when you need to:

- Parse BPMN files that use vendor-specific extensions
- Add custom attributes to BPMN elements
- Implement organization-specific validation rules
- Support proprietary BPMN dialects

## Plugin Architecture

PyBPMN Parser uses a registry-based plugin system:

1. **Plugin Discovery** - Plugins are registered through the plugin registry
2. **Namespace Registration** - Each plugin declares the XML namespaces it handles
3. **Element Extension** - Plugins can extend base BPMN element classes
4. **Validation Hooks** - Plugins can add custom validation logic

## Available Resources

- **[Creating Plugins](creating.md)** - Step-by-step guide to building your first plugin
- **[Plugin Templates](templates.md)** - Ready-to-use templates for common plugin patterns
- **[Best Practices](best-practices.md)** - Recommendations for plugin development

## Quick Example

Here's a minimal plugin that adds support for a custom namespace:

```python
from pybpmn_parser.plugins import register_plugin

class CustomPlugin:
    """Support for custom BPMN extensions."""

    namespaces = {
        "custom": "http://example.com/custom"
    }

    def extend_element(self, element_type, namespace_data):
        """Extend an element with custom attributes."""
        return namespace_data

# Register the plugin
register_plugin(CustomPlugin())
```

## Next Steps

Ready to create your own plugin? Start with [Creating Plugins](creating.md) to learn the fundamentals.
