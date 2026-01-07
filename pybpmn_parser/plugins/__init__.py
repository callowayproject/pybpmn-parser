"""Moddle extension converter."""

DEFAULT_PLUGINS = ["camunda.json", "activiti.json", "zeebe.json"]


def load_default_plugins() -> None:
    """
    Loads and registers the default plugins used by the application.

    Note:
        For best results, the `pybpmn_parser.bpmn.load_classes` function should be called before this.

    This function reads the default plugin definitions from resources, parses
    them into Moddle package configurations, and registers these packages in
    the global registry. After registering the plugins, the Moddle registry is
    converted to its final usable state.
    """
    import json
    from importlib.resources import files

    from .moddle import ModdlePackage, convert_moddle_registry, registry

    plugin_files = files("pybpmn_parser.plugins.moddle_models")
    for plugin in DEFAULT_PLUGINS:
        extension_contents = json.loads(plugin_files.joinpath(plugin).read_text(encoding="utf-8"))
        pkg = ModdlePackage(**extension_contents)
        registry.register_package(pkg)

    convert_moddle_registry()
