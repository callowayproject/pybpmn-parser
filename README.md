# PyBPMN Parser

A Python library for parsing and validating BPMN 2.0 XML into typed Python objects. It provides a small, focused API for loading BPMN files, schema validation, and an extensible plugin system for vendor-specific extensions.

Links:
- Source: https://github.com/callowayproject/pybpmn-parser
- Docs (MkDocs site): https://callowayproject.github.io/pybpmn_parser
- Changelog: ./CHANGELOG.md
- License: ./LICENSE

## Overview

PyBPMN Parser transforms BPMN XML documents into structured Python objects so you can analyze, traverse, and transform models programmatically.

## Key features

- Type-safe parsing to Python models
- Schema validation against BPMN 2.0
- Vendor extension support via [bpmn.io's Moddle extension mechanism](https://github.com/bpmn-io/bpmn-js-example-model-extension)
- Simple API: parse strings or files

## Example

```python
from pathlib import Path
from pybpmn_parser.parse import Parser

# Create a parser instance
parser = Parser()

# Parse a BPMN file
definitions = parser.parse_file(Path("my_process.bpmn"))

# Access processes, elements, etc.
for process in definitions.processes:
    print(process.id)
```

## Requirements

- Python 3.12 or newer
- uv (recommended) or pip/venv


## Installation and Setup

Using uv (recommended):

```bash
uv add pybpmn-parser
```

Using pip/venv (runtime only):
```bash
pip install pybpmn-parser
```

## How to Use

Parse from a string:
```python
from pybpmn_parser.parse import Parser

xml = """<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL" targetNamespace="http://bpmn.io/schema/bpmn">
  <process id="Process_1" />
</definitions>
"""

parser = Parser()
defs = parser.parse_string(xml)
```

Parse from a file path:
```python
from pathlib import Path
from pybpmn_parser.parse import Parser

parser = Parser()
defs = parser.parse_file(Path("./path/to/diagram.bpmn"))
```

Validation errors raise pybpmn_parser.validator.ValidationError with a human-readable message. See tests for examples of error messages.

## Vendor Extensions (Plugins)

There is built-in support for:

- Camunda extensions (https://github.com/camunda/camunda-bpmn-moddle)
- Zeebe extensions (https://github.com/camunda/zeebe-bpmn-moddle)
- Activiti extensions (https://github.com/igdianov/activiti-bpmn-moddle)

To use a custom extension, pass the Moddle definition file path to the parser:

```python
from pathlib import Path
from pybpmn_parser.parse import Parser

custom_extension_path = Path("./path/to/custom_extension.json")
parser = Parser(moddle_extensions=[custom_extension_path])
```


## Scripts and Common Commands

With uv:
- Run tests: `uv run pytest`
- Run tests with quick output: `uv run pytest -q`
- Coverage (HTML report is configured via pytest addopts): `uv run pytest` then open ./htmlcov/index.html
- Lint (Ruff): `uv run ruff check .`
- Format (Black via Ruff): `uv run ruff format .` or `uv run black .`
- Type stubs/docs (serve): `uv run mkdocs serve`
- Build docs: `uv run mkdocs build`

With pip/venv:
- Run tests: `pytest`
- Lint: `ruff check .`
- Format: `ruff format .` or `black .`
- Docs: `mkdocs serve` / `mkdocs build`

Note: pip doesn’t understand pyproject "dependency-groups"; prefer uv for installing dev/test/docs dependencies.


## Environment Variables

- No required environment variables are known at this time.
- TODO: Document any optional env vars (e.g., to customize schema locations or caching) if/when they are introduced.


## Tests

The repository uses pytest and pytest-cov. Configuration is in pyproject.toml ([tool.pytest.ini_options]).

Run the test suite:
```bash
uv run pytest
```

Selected tests illustrate library usage:
- tests/test_parse.py — parsing strings and files, common error cases
- tests/test_validator.py — validation error handling and messages
- tests/test_parse_moddle_extension.py — creating and registering moddle-based extensions
- tests/test_core.py — internal utility behavior

HTML coverage is written to ./htmlcov by default (see pyproject addopts).


## Project Structure

Top-level layout:

```
pybpmn_parser/          # Library code
  parse.py              # parse() and parse_file() entry points
  validator.py          # BPMN 2.0 XML validation
  plugins/              # Plugin system for vendor extensions
    registry.py         # Registry for extension parsers
    parse_moddle_extension.py
    moodle_types.py     # Moddle type definitions
  ...                   # Additional BPMN model packages/modules

docs/                   # MkDocs documentation (Material)
mkdocs.yml              # MkDocs configuration

tests/                  # Pytest test suite and fixtures
pyproject.toml          # Build, tooling, and test configuration
uv.lock                 # Locked dependency graph for uv
LICENSE                 # BSD 3-Clause License
CHANGELOG.md            # Release notes
```


## Development

- Use uv for dependency management and running tasks:
  - `uv sync` to install all groups (dev, test, docs)
  - `uv run ruff check .` and `uv run ruff format .`
  - `uv run pytest`
  - `uv run mkdocs serve`
- The docs site auto-generates API reference stubs from source via docs/gen_doc_stubs.py (mkdocs-gen-files).

Contributions are welcome. See CONTRIBUTING.md and CODE_OF_CONDUCT.md.


## License

BSD 3-Clause License. See LICENSE for details.
