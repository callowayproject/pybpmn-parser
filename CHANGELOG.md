# Changelog

## 0.3.1 (2026-01-07)

[Compare the full difference.](https://github.com/callowayproject/pybpmn-parser/compare/0.3.0...0.3.1)

### Fixes

- Fix type hinting and update some documentation. [ad2d616](https://github.com/callowayproject/pybpmn-parser/commit/ad2d616cd7388fced8457a08b552366b3eeb034f)

## 0.3.0 (2026-01-07)

[Compare the full difference.](https://github.com/callowayproject/pybpmn-parser/compare/0.2.0...0.3.0)

### New

- Add `.secrets.baseline` to track detected secrets and enhance security. [8146b7a](https://github.com/callowayproject/pybpmn-parser/commit/8146b7ad8fc4fa8b0050e2f25498644a47df805a)

### Other

- Bump the github-actions group with 2 updates. [da4efe4](https://github.com/callowayproject/pybpmn-parser/commit/da4efe44ba52f457c6f4af6aef12bb8864c391c2)

  Bumps the github-actions group with 2 updates: [actions/checkout](https://github.com/actions/checkout) and [actions/download-artifact](https://github.com/actions/download-artifact).

  Updates `actions/checkout` from 5 to 6

  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v5...v6)

  Updates `actions/download-artifact` from 6 to 7

  - [Release notes](https://github.com/actions/download-artifact/releases)
  - [Commits](https://github.com/actions/download-artifact/compare/v6...v7)

  ______________________________________________________________________

  **updated-dependencies:** - dependency-name: actions/checkout
  dependency-version: '6'
  dependency-type: direct:production
  update-type: version-update:semver-major
  dependency-group: github-actions

  **signed-off-by:** dependabot[bot] <support@github.com>

- Comment out unused `detect-secrets` hook in pre-commit configuration. [0f22e2a](https://github.com/callowayproject/pybpmn-parser/commit/0f22e2a60523bca0bdfc7d266f1113a1518dbfd2)

### Updates

- Refactor: Remove redundant `reference/index.md`, update navigation links, and add `GH_TOKEN` to `bump-version` workflow env. [e8b9c7a](https://github.com/callowayproject/pybpmn-parser/commit/e8b9c7aa72fc87557760a21aeb1928cc9bd4d72d)

- Refactor: Introduce `ParseContext` for managing elements and references during BPMN parsing, update context handling across factory and core modules, and add `pytest-sugar` dependency. [eb92bc0](https://github.com/callowayproject/pybpmn-parser/commit/eb92bc0a7e57f69a0213dfbc12e30004fad36226)

- Refactor: Convert BPMN node connection fields to consistently use arrays instead of strings. [93cdf5d](https://github.com/callowayproject/pybpmn-parser/commit/93cdf5d2d9630e098765e3843b2f13ee2f663218)

- Refactor: Replace deprecated `read_text` with `files.joinpath(...).read_text()`. [ad3be1b](https://github.com/callowayproject/pybpmn-parser/commit/ad3be1bc3f7d57116d8f07c4cc23817ae4714400)

- Refactor: Add `is_reference` metadata attribute to various BPMN model fields across activity and common classes. [0c3a219](https://github.com/callowayproject/pybpmn-parser/commit/0c3a219606b919bbba35d02ad1bdbd54c1acee47)

- Refactor: Simplify string formatting and exception handling in `core.py`. [14ccca6](https://github.com/callowayproject/pybpmn-parser/commit/14ccca617b43d04afad6249378ac747337181fe0)

- Refactor: Remove union types from `implementation` and `method` fields across activity classes. [a5b47e8](https://github.com/callowayproject/pybpmn-parser/commit/a5b47e8ff35ed4a64ae522e2e15f76d43cb550bb)

- Remove unused `--baseline` argument from detect-secrets hook in pre-commit config. [27270c7](https://github.com/callowayproject/pybpmn-parser/commit/27270c795b91a13cceb582f0b530fc7507bd6599)

- Update `.secrets.baseline` to include new filter path and refresh metadata timestamp. [86cdd19](https://github.com/callowayproject/pybpmn-parser/commit/86cdd19d52844b616a5bf6306bc54fbc38816164)

- Update changelog for unreleased changes, including fixes, new features, updates, and code refactoring. [120f273](https://github.com/callowayproject/pybpmn-parser/commit/120f2735c2b9162cf076a13636842520aa8e3877)

- Remove "Next Steps" sections and outdated example references to streamline documentation. [698041f](https://github.com/callowayproject/pybpmn-parser/commit/698041fe1497183ac1d00e33307d7cfe4e180a60)

- Update `miwg-test-suite-2025` fixtures to include expanded BPMNDiagram details. [ad0482d](https://github.com/callowayproject/pybpmn-parser/commit/ad0482d11c221c7a96da513d7547db5ed6663e58)

- Update dependency versions in `uv.lock` to ensure compatibility with the latest releases. [4c931f7](https://github.com/callowayproject/pybpmn-parser/commit/4c931f7f85f6ed780cbc9dbf1389e595e6937112)

- Refactor factory and core modules for improved clarity and efficiency; introduce `index_ids` utility and encapsulate parsing output in `ParseResult`. [a908f0c](https://github.com/callowayproject/pybpmn-parser/commit/a908f0ca57762e159ba68bf1e74757905d926abc)

## 0.2.0 (2025-12-30)

[Compare the full difference.](https://github.com/callowayproject/pybpmn-parser/compare/0.1.0...0.2.0)

### Fixes

- Fix minor docstring formatting issue in `core.py` (`enum_as` argument description). [e8df97a](https://github.com/callowayproject/pybpmn-parser/commit/e8df97a573532b0390a76c2eb49a650c3a470239)

- Fix Meta `name` attribute casing for `AdHocSubProcess` to ensure naming consistency. [12db631](https://github.com/callowayproject/pybpmn-parser/commit/12db631b071024b97ba7e52fbbfe2006b0dd4600)

### New

- Add factory, registry, and parsing improvements for robust BPMN element creation and handling. [34133f2](https://github.com/callowayproject/pybpmn-parser/commit/34133f28ecf25ea151017fec869515e09d189f97)

- Add Moddle registry, type declarations, and BPMN model definitions for advanced BPMN 2.0 parsing. [707a435](https://github.com/callowayproject/pybpmn-parser/commit/707a4354c6a582c4e2a8601fd6a881ed34b0a229)

- Add metadata name attributes for BPMN elements and enhance naming consistency. [b648aee](https://github.com/callowayproject/pybpmn-parser/commit/b648aee5ca4c6f254f583da193514e3eeff35ff4)

- Add BPMN color models and schema support for background, border, and text colors. [a7c8733](https://github.com/callowayproject/pybpmn-parser/commit/a7c87337d8bf16cece55cabe53947199e8a039a3)

- Add DC, DI, and BPMNDI element definitions and models for BPMN 2.0 parsing. [ff1f0d6](https://github.com/callowayproject/pybpmn-parser/commit/ff1f0d668c4ccd82d900b371de0f0fa1df0654fb)

- Add BPMN 2.0 activity representations and parsing functionality. [13f039a](https://github.com/callowayproject/pybpmn-parser/commit/13f039af68856924554033e93937dcbf45835be0)

- Add role-specific responsibility documentation for API, database, and testing engineers. [1f25828](https://github.com/callowayproject/pybpmn-parser/commit/1f25828fba10e36770b78709b1c0a960592aafb3)

### Other

- Streamline `README.md` by removing redundant sections and improving clarity in project description and usage details. [593e2be](https://github.com/callowayproject/pybpmn-parser/commit/593e2bee001261ffb4e5c41ae1ff85f8c207cc17)

- Call `load_classes()` in BPMN module to initialize loaded namespaces. [1188b72](https://github.com/callowayproject/pybpmn-parser/commit/1188b7251f39cb6cf4bc3f7bf8f104e18355d684)

### Updates

- Remove "Next Steps" sections and outdated example references to streamline documentation. [698041f](https://github.com/callowayproject/pybpmn-parser/commit/698041fe1497183ac1d00e33307d7cfe4e180a60)

- Update `miwg-test-suite-2025` fixtures to include expanded BPMNDiagram details. [ad0482d](https://github.com/callowayproject/pybpmn-parser/commit/ad0482d11c221c7a96da513d7547db5ed6663e58)

- Update dependency versions in `uv.lock` to ensure compatibility with the latest releases. [4c931f7](https://github.com/callowayproject/pybpmn-parser/commit/4c931f7f85f6ed780cbc9dbf1389e595e6937112)

- Refactor factory and core modules for improved clarity and efficiency; introduce `index_ids` utility and encapsulate parsing output in `ParseResult`. [a908f0c](https://github.com/callowayproject/pybpmn-parser/commit/a908f0ca57762e159ba68bf1e74757905d926abc)

- Update dependency versions in `uv.lock` to incorporate the latest packages. [db2ddf2](https://github.com/callowayproject/pybpmn-parser/commit/db2ddf28666ef922eed4fbdf49dcd2d021215bfe)

- Remove examples and associated documentation for Exclusive Gateway, Parallel Gateway, and Sequential Flow to clean up the codebase and streamline documentation. [06a236f](https://github.com/callowayproject/pybpmn-parser/commit/06a236fec907f74a93e529a963e72294946b4ebe)

- Update `gen_doc_stubs.py` to adjust paths for modular structure and improve navigation formatting. [afc15cd](https://github.com/callowayproject/pybpmn-parser/commit/afc15cda281e4c3d5c906ab689bd37e2bd3b198e)

- Remove unused `load_classes` call from `parse.py` for code cleanup. [c6a51c0](https://github.com/callowayproject/pybpmn-parser/commit/c6a51c059f7242d833abe7f79a5c0c8467d1bf57)

- Remove unused `extension schema` validation logic and associated references for code simplification. [8abd1d1](https://github.com/callowayproject/pybpmn-parser/commit/8abd1d166df4cae7939458bd5a3a2aa8bc9f943b)

- Refactor `create_element_from_dict` to delegate property handling to `_handle_known_property` and `_handle_unknown_property` for improved clarity and extensibility. [8257fa5](https://github.com/callowayproject/pybpmn-parser/commit/8257fa5b4dbd0a4012b9aa2eef97d3d6e2c10664)

- Remove unused `strtobool` function and refactor sequence conversion logic into `_convert_sequence` for clarity and reuse. [f403ee7](https://github.com/callowayproject/pybpmn-parser/commit/f403ee7cb288d34cc49868aacc974881c62ea56f)

- Refactor `event_type` property in `StartEvent` for clarity and efficiency; simplify logic and remove redundant definitions. [d673ac3](https://github.com/callowayproject/pybpmn-parser/commit/d673ac374b731c26781695e8a1ba297b599af64f)

- Remove BPMN color module and associated definitions, tests, and dependencies. Add comprehensive tests for `StartEvent` and `ModdleRegistry`. Refactor existing tests and parser logic for clarity and coverage. [f5d37c6](https://github.com/callowayproject/pybpmn-parser/commit/f5d37c6d598b24c156c079afc06bf430090045b2)

- Remove unused `parse` methods across BPMN element classes to simplify and streamline codebase. [cce9f16](https://github.com/callowayproject/pybpmn-parser/commit/cce9f1608a6c0e25bd750905e3469906060c68a8)

- Remove `UndefinedType` and replace `Undefined` default value with `None` for simplicity and clarity. [32da048](https://github.com/callowayproject/pybpmn-parser/commit/32da0488383c8735b3077cc813cdbb0a355ab4ea)

- Remove obsolete tests, example tags, and moddle extension parsing logic. Add comprehensive BPMN JSON fixture for testing. [ccecf36](https://github.com/callowayproject/pybpmn-parser/commit/ccecf36534eec651ba5163798283ac840d3eac20)

- Remove unused function and refactor QName parsing logic. [3ba55e7](https://github.com/callowayproject/pybpmn-parser/commit/3ba55e7ada16949bb37da032fc0e8d415086fec8)

- Update metadata attributes for documentation element to ensure proper parsing. [57f7765](https://github.com/callowayproject/pybpmn-parser/commit/57f7765222b3a05ef36307931216f19a69b72e2e)

- Remove unused import and commented-out code, update Meta name for formal expressions, and add missing DI namespace definition. [99fb704](https://github.com/callowayproject/pybpmn-parser/commit/99fb7041ec0622a7f4c5ed40b1d347ad876e0871)

- Update pre-commit hooks, dependencies, and Python version to maintain compatibility and improve project standards. [f6a90a7](https://github.com/callowayproject/pybpmn-parser/commit/f6a90a74682df46b64e87d99abc162794bf5480a)

## 0.1.0 (2025-09-15)

### Other

- Initial commit. [07c2762](https://github.com/callowayproject/pybpmn-parser/commit/07c2762bc4ddae66d13c859f6a1d1ef8e768b17f)

  Updates `github/codeql-action` from 3 to 4

  - [Release notes](https://github.com/github/codeql-action/releases)
  - [Changelog](https://github.com/github/codeql-action/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/github/codeql-action/compare/v3...v4)

  Updates `actions/attest-build-provenance` from 2 to 3

  - [Release notes](https://github.com/actions/attest-build-provenance/releases)
  - [Changelog](https://github.com/actions/attest-build-provenance/blob/main/RELEASE.md)
  - [Commits](https://github.com/actions/attest-build-provenance/compare/v2...v3)

  ______________________________________________________________________

  **updated-dependencies:** - dependency-name: actions/checkout
  dependency-version: '5'
  dependency-type: direct:production
  update-type: version-update:semver-major
  dependency-group: github-actions

  **signed-off-by:** dependabot[bot] <support@github.com>

- [pre-commit.ci] pre-commit autoupdate. [04deb4c](https://github.com/callowayproject/pybpmn-parser/commit/04deb4c6f1f867a168b73c6f7d2f9508c9761f1e)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.14.0 → v0.14.10](https://github.com/astral-sh/ruff-pre-commit/compare/v0.14.0...v0.14.10)

- Streamline `README.md` by removing redundant sections and improving clarity in project description and usage details. [593e2be](https://github.com/callowayproject/pybpmn-parser/commit/593e2bee001261ffb4e5c41ae1ff85f8c207cc17)

- Call `load_classes()` in BPMN module to initialize loaded namespaces. [1188b72](https://github.com/callowayproject/pybpmn-parser/commit/1188b7251f39cb6cf4bc3f7bf8f104e18355d684)

### Updates

- Update dependency versions in `uv.lock` to incorporate the latest packages. [db2ddf2](https://github.com/callowayproject/pybpmn-parser/commit/db2ddf28666ef922eed4fbdf49dcd2d021215bfe)

- Remove examples and associated documentation for Exclusive Gateway, Parallel Gateway, and Sequential Flow to clean up the codebase and streamline documentation. [06a236f](https://github.com/callowayproject/pybpmn-parser/commit/06a236fec907f74a93e529a963e72294946b4ebe)

- Update `gen_doc_stubs.py` to adjust paths for modular structure and improve navigation formatting. [afc15cd](https://github.com/callowayproject/pybpmn-parser/commit/afc15cda281e4c3d5c906ab689bd37e2bd3b198e)

- Remove unused `load_classes` call from `parse.py` for code cleanup. [c6a51c0](https://github.com/callowayproject/pybpmn-parser/commit/c6a51c059f7242d833abe7f79a5c0c8467d1bf57)

- Remove unused `extension schema` validation logic and associated references for code simplification. [8abd1d1](https://github.com/callowayproject/pybpmn-parser/commit/8abd1d166df4cae7939458bd5a3a2aa8bc9f943b)

- Refactor `create_element_from_dict` to delegate property handling to `_handle_known_property` and `_handle_unknown_property` for improved clarity and extensibility. [8257fa5](https://github.com/callowayproject/pybpmn-parser/commit/8257fa5b4dbd0a4012b9aa2eef97d3d6e2c10664)

- Remove unused `strtobool` function and refactor sequence conversion logic into `_convert_sequence` for clarity and reuse. [f403ee7](https://github.com/callowayproject/pybpmn-parser/commit/f403ee7cb288d34cc49868aacc974881c62ea56f)

- Refactor `event_type` property in `StartEvent` for clarity and efficiency; simplify logic and remove redundant definitions. [d673ac3](https://github.com/callowayproject/pybpmn-parser/commit/d673ac374b731c26781695e8a1ba297b599af64f)

- Remove BPMN color module and associated definitions, tests, and dependencies. Add comprehensive tests for `StartEvent` and `ModdleRegistry`. Refactor existing tests and parser logic for clarity and coverage. [f5d37c6](https://github.com/callowayproject/pybpmn-parser/commit/f5d37c6d598b24c156c079afc06bf430090045b2)

- Remove unused `parse` methods across BPMN element classes to simplify and streamline codebase. [cce9f16](https://github.com/callowayproject/pybpmn-parser/commit/cce9f1608a6c0e25bd750905e3469906060c68a8)

- Remove `UndefinedType` and replace `Undefined` default value with `None` for simplicity and clarity. [32da048](https://github.com/callowayproject/pybpmn-parser/commit/32da0488383c8735b3077cc813cdbb0a355ab4ea)

- Remove obsolete tests, example tags, and moddle extension parsing logic. Add comprehensive BPMN JSON fixture for testing. [ccecf36](https://github.com/callowayproject/pybpmn-parser/commit/ccecf36534eec651ba5163798283ac840d3eac20)

- Remove unused function and refactor QName parsing logic. [3ba55e7](https://github.com/callowayproject/pybpmn-parser/commit/3ba55e7ada16949bb37da032fc0e8d415086fec8)

- Update metadata attributes for documentation element to ensure proper parsing. [57f7765](https://github.com/callowayproject/pybpmn-parser/commit/57f7765222b3a05ef36307931216f19a69b72e2e)

- Remove unused import and commented-out code, update Meta name for formal expressions, and add missing DI namespace definition. [99fb704](https://github.com/callowayproject/pybpmn-parser/commit/99fb7041ec0622a7f4c5ed40b1d347ad876e0871)

- Update pre-commit hooks, dependencies, and Python version to maintain compatibility and improve project standards. [f6a90a7](https://github.com/callowayproject/pybpmn-parser/commit/f6a90a74682df46b64e87d99abc162794bf5480a)

## 0.1.0 (2025-09-15)

### Other

- Initial commit. [07c2762](https://github.com/callowayproject/pybpmn-parser/commit/07c2762bc4ddae66d13c859f6a1d1ef8e768b17f)
