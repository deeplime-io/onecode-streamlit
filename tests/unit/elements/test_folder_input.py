import os
import shutil

from onecode import Mode, Project

from onecode_st import FolderInput
from tests.utils.flow_cli import _clean_flow, _generate_flow_name


def test_execute_folder_input():
    _, folder, _ = _generate_flow_name()
    tmp = _clean_flow(folder)
    folder_path = os.path.join(tmp, folder)

    os.makedirs(folder_path, exist_ok=True)

    Project().mode = Mode.EXECUTE

    widget = FolderInput(
        key="FolderInput",
        value=folder_path
    )

    assert widget() == folder_path
    assert widget.key == "folderinput"
    assert widget.label == "'''FolderInput'''"
    assert widget._label == "FolderInput"

    widget = FolderInput(
        key="FolderInput",
        value="/"
    )

    assert widget() == folder_path

    try:
        shutil.rmtree(folder_path)
    except Exception:
        pass


def test_extract_all_folder_input():
    Project().mode = Mode.EXTRACT_ALL

    widget = FolderInput(
        key="FolderInput",
        value=["/path/to"],
        label="My FolderInput",
        optional="$x$",
        count=2
    )

    assert widget() == ('folderinput', {
        "key": "folderinput",
        "kind": "FolderInput",
        "value": ["/path/to"],
        "label": "'''My FolderInput'''",
        "disabled": '_DATA_["x"]',
        "optional": True,
        "count": "2"
    })
