import os
import shutil

from onecode import FileFilter, Mode, Project

from onecode_st import FileInput
from tests.utils.flow_cli import (
    _clean_flow,
    _generate_csv_file,
    _generate_flow_name
)


def test_execute_single_file_input_single_selection():
    _, folder, _ = _generate_flow_name()
    tmp = _clean_flow(folder)
    folder_path = os.path.join(tmp, folder)

    csv_file = _generate_csv_file(folder_path, 'test.csv')

    Project().mode = Mode.EXECUTE

    widget = FileInput(
        key="FileInput",
        value=csv_file
    )

    assert widget() == csv_file
    assert widget.key == "fileinput"
    assert widget.label == "'''FileInput'''"
    assert widget._label == "FileInput"

    widget = FileInput(
        key="FileInput",
        value="test.csv"
    )

    assert widget() == os.path.join(folder_path, 'data', 'test.csv')

    try:
        shutil.rmtree(folder_path)
    except Exception:
        pass


def test_extract_all_file_input():
    Project().mode = Mode.EXTRACT_ALL

    widget = FileInput(
        key="FileInput",
        value=["/path/to/file.jpg"],
        label="My FileInput",
        optional="$x$",
        count=2,
        multiple=True,
        tags=["Core"],
        types=[FileFilter.IMAGE]
    )

    assert widget() == ('fileinput', {
        "key": "fileinput",
        "kind": "FileInput",
        "value": ["/path/to/file.jpg"],
        "label": "My FileInput",
        "disabled": '_DATA_["x"]',
        "optional": True,
        "count": "2",
        "tags": ["Core"],
        "types": [("Image", ".jpg .png .jpeg")],
        "multiple": True
    })
