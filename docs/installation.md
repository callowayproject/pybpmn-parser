---
title: Installation
summary: How to install PyBPMN Parser
date: 2025-09-15T12:32:13.355904+00:00
---

# Installation

PyBPMN Parser requires Python 3.8 or higher. This guide covers different installation methods.

## Requirements

- Python 3.8+
- pip (usually included with Python) or uv

## Installing from PyPI

The recommended way to install PyBPMN Parser is from PyPI using pip:

```bash
pip install pybpmn-parser
```

This installs the latest stable release with all required dependencies.

## Installing with uv

If you use [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
uv add pybpmn-parser
```

Or in a uv project:

```bash
uv pip install pybpmn-parser
```

## Installing from Source

To install the development version from the GitHub repository:

```bash
# Clone the repository
git clone https://github.com/callowayproject/pybpmn-parser.git
cd pybpmn-parser

# Install in development mode
pip install -e .
```

Or with uv:

```bash
git clone https://github.com/callowayproject/pybpmn-parser.git
cd pybpmn-parser
uv pip install -e .
```

## Verifying Installation

After installation, verify that PyBPMN Parser is installed correctly:

```python
import pybpmn_parser
from pybpmn_parser.parse import parse

# Test with minimal BPMN XML
xml = """<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             targetNamespace="http://bpmn.io/schema/bpmn">
    <process id="Process_1" />
</definitions>"""

definitions = parse(xml)
print(f"Successfully parsed! Found {len(definitions.processes)} process(es)")
```

Expected output:
```
Successfully parsed! Found 1 process(es)
```

## Optional Dependencies

PyBPMN Parser has minimal required dependencies (lxml for XML parsing). All core functionality works out of the box.

## Troubleshooting

### lxml Installation Issues

If you encounter issues installing lxml (especially on Windows):

```bash
# Install lxml separately first
pip install lxml

# Then install pybpmn-parser
pip install pybpmn-parser
```

### Python Version Issues

Ensure you're using Python 3.8 or higher:

```bash
python --version
```

If you have multiple Python versions, you may need to use `python3` or `python3.8+` explicitly:

```bash
python3 -m pip install pybpmn-parser
```

## Next Steps

Now that PyBPMN Parser is installed, continue to the [Quick Start](quickstart.md) guide to learn how to use it.
