"""Tests for the A.*.* MIWG suite."""

import json
from pathlib import Path

import pytest
from pytest import param

from pybpmn_parser.core import dataclass_to_dict
from pybpmn_parser.parse import Parser
from tests._utils import assert_attributes


@pytest.mark.parametrize(
    ["test_name"],
    [
        param("A.1.0", id="A.1.0"),
        param("A.2.0", id="A.2.0"),
        param("A.2.1", id="A.2.1"),
        param("A.3.0", id="A.3.0"),
        param("A.4.0", id="A.4.0"),
        param("A.4.1", id="A.4.1"),
        param("B.1.0", id="B.1.0"),
        param("B.2.0", id="B.2.0"),
        param("C.1.0", id="C.1.0"),
        param("C.1.1", id="C.1.1"),
        param("C.2.0", id="C.2.0"),
        param("C.3.0", id="C.3.0"),
        param("C.4.0", id="C.4.0"),
        param("C.5.0", id="C.5.0"),
        param("C.6.0", id="C.6.0"),
        param("C.7.0", id="C.7.0"),
        param("C.8.0", id="C.8.0"),
        param("C.8.1", id="C.8.1"),
        param("C.9.0", id="C.9.0"),
        param("C.9.1", id="C.9.1"),
        param("C.9.2", id="C.9.2"),
    ],
)
def test_miwg(test_name: str, fixture_dir: Path):
    """Import a MIWG test suite file and validate the attributes."""
    parser = Parser()
    file_path = fixture_dir / "miwg-test-suite-2025" / f"{test_name}.bpmn"
    expected_file = fixture_dir / "miwg-test-suite-2025" / f"{test_name}.json"
    bpmn_model = parser.parse_file(file_path)
    expected_json = json.loads(expected_file.read_text(encoding="utf-8"))
    assert_attributes(bpmn_model, expected_json)
