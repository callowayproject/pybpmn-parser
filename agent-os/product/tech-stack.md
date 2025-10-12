# Tech Stack

## Core Language & Runtime
- **Language:** Python 3.12+
- **Type System:** Python type hints with full typing coverage
- **Package Manager:** uv (modern Python package manager)
- **Build System:** Hatchling (PEP 517 compliant build backend)

## Core Libraries
- **XML Parsing:** lxml 6.0+ (high-performance XML processing)
- **Data Modeling:** Pydantic 2.11+ (data validation using Python type annotations)
- **XML Binding:** pydantic-xml 2.17+ (XML serialization/deserialization for Pydantic)
- **Functional Programming:** returns 0.23+ (type-safe error handling)
- **Schema Validation:** xmlschema 4.1+ (XML Schema validator)
- **XML to Dict:** xmltodict 0.14+ (XML to Python dict conversion)

## Development Tools
- **Version Management:** bump-my-version (semantic versioning)
- **Changelog Generation:** generate-changelog (automated changelog from git commits)
- **Pre-commit Hooks:** pre-commit (git hooks for code quality)
- **Package Development:** uv (fast Python package installer and resolver)

## Testing Infrastructure
- **Test Framework:** pytest 8.0+ (Python testing framework)
- **Coverage Analysis:** pytest-cov 7.0+ (test coverage reporting)
- **Coverage Tool:** coverage (code coverage measurement)
- **Async Testing:** pytest-asyncio (async/await testing support)
- **Mocking:** pytest-mock (pytest plugin for mock)
- **Network Isolation:** pytest-socket (disable network calls in tests)
- **HTTP Testing:** httpx (async HTTP client for testing)

## Code Quality & Formatting
- **Linter/Formatter:** Ruff (fast Python linter and formatter)
- **Code Formatter:** Black 23.3+ (opinionated Python formatter)
- **Type Checking:** mypy (static type checker for Python)
- **Docstring Linting:** pydoclint (Google-style docstring linter)
- **Docstring Coverage:** interrogate (docstring coverage analysis)

## Documentation
- **Documentation Generator:** MkDocs 1.4.3+ (static site generator)
- **Theme:** MkDocs Material 9.1.0+ (material design theme)
- **API Documentation:** mkdocstrings[python] (auto-generate API docs from docstrings)
- **Extensions:**
  - mkdocs-gen-files 0.5+ (programmatically generate documentation pages)
  - mkdocs-literate-nav 0.6+ (navigation from markdown files)
  - mkdocs-section-index 0.3.5+ (section index pages)
  - griffe-pydantic (Pydantic model documentation)
  - mkdocs-click (CLI documentation from click)
  - mkdocs-include-markdown-plugin (include external markdown)
  - mkdocs-git-revision-date-localized-plugin (git revision dates)
  - mkdocs-git-authors-plugin (git authors information)
  - mkdocs-git-committers-plugin (git committers information)

## CI/CD & Version Control
- **Version Control:** Git
- **Code Hosting:** GitHub (https://github.com/callowayproject/pybpmn-parser)
- **CI/CD:** GitHub Actions (automated testing and deployment workflows)
- **Documentation Hosting:** GitHub Pages (https://callowayproject.github.io/pybpmn_parser)

## Project Configuration
- **Python Project:** pyproject.toml (PEP 621 compliant project configuration)
- **Ruff Configuration:** Comprehensive linting rules including flake8, isort, pydocstyle
- **Black Configuration:** Line length 119
- **Coverage Configuration:** Branch coverage with 90% minimum
- **Pre-commit Configuration:** .pre-commit-config.yaml (automated code quality checks)

## Supported BPMN Standards
- **BPMN 2.0:** Full specification compliance
- **XML Schema:** XSD validation support
- **Vendor Extensions:**
  - Camunda (built-in support)
  - Custom extensions via plugin system
  - Moodle types (in development)

## Performance Considerations
- **XML Parser:** lxml with C extensions for performance
- **Validation:** Lazy validation with streaming where possible
- **Memory Management:** Efficient handling of large BPMN files
- **Caching:** Strategic caching of parsed elements and schemas

## Distribution
- **Package Repository:** PyPI (Python Package Index)
- **Package Format:** Wheel and source distributions
- **License:** Open source (see LICENSE file)
- **Python Support:** Python 3.12+ only (modern Python features)
