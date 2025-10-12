"""Run the Kitchen sink BPMN file."""

from pathlib import Path

import lxml.etree as ET  # noqa: N812

from pybpmn_parser.bpmn.infrastructure.definitions import Definitions


def test_kitchen_sink(fixture_dir: Path):
    """Run the Kitchen sink BPMN file."""
    bpmn_file = fixture_dir / "kitchen-sink.bpmn"
    bpmn = bpmn_file.read_text(encoding="utf-8")
    root: ET.Element = ET.fromstring(bpmn.encode("utf-8"))
    Definitions.parse(root)
