import os
import shutil

import pandas as pd
from onecode import Mode, Project

from onecode_st import CsvReader
from tests.utils.flow_cli import (
    _clean_flow,
    _generate_csv_file,
    _generate_flow_name
)


def test_execute_single_csv_reader():
    _, folder, _ = _generate_flow_name()
    tmp = _clean_flow(folder)
    folder_path = os.path.join(tmp, folder)

    csv_file = _generate_csv_file(folder_path, 'test.csv')

    Project().mode = Mode.EXECUTE

    widget = CsvReader(
        key="CsvReader",
        value=csv_file
    )

    pd.testing.assert_frame_equal(widget(), pd.read_csv(csv_file))
    assert widget.key == "csvreader"
    assert widget.label == "'''CsvReader'''"
    assert widget._label == "CsvReader"

    try:
        shutil.rmtree(folder_path)
    except Exception:
        pass


def test_extract_all_csv_reader():
    Project().mode = Mode.EXTRACT_ALL

    widget = CsvReader(
        key="CsvReader",
        value=["/path/to/file.csv"],
        label="My CsvReader",
        optional="$x$",
        count=2,
        tags=["CSV"]
    )

    assert widget() == ('csvreader', {
        "key": "csvreader",
        "kind": "CsvReader",
        "value": ["/path/to/file.csv"],
        "label": "'''My CsvReader'''",
        "disabled": '_DATA_["x"]',
        "optional": True,
        "count": "2",
        "tags": ["CSV"]
    })
