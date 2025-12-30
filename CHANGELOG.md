# Changelog

## Unreleased (2025-12-30)

[Compare the full difference.](https://github.com/callowayproject/pybpmn-parser/compare/0.1.0...HEAD)

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
