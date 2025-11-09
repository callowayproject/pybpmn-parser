"""Run the Kitchen sink BPMN file."""

import json
from pathlib import Path

from pybpmn_parser.core import dataclass_to_dict
from pybpmn_parser.parse import Parser
from tests._utils import assert_attributes


def test_kitchen_sink(fixture_dir: Path):
    """Run the Kitchen sink BPMN file."""
    parser = Parser()
    bpmn_file = fixture_dir / "kitchen-sink.bpmn"
    expected_file = fixture_dir / "kitchen-sink.json"
    bpmn = parser.parse_file(bpmn_file)
    bpmn_model = dataclass_to_dict(bpmn, skip_empty=True)
    expected_json = json.loads(expected_file.read_text(encoding="utf-8"))
    assert_attributes(bpmn_model, expected_json)
