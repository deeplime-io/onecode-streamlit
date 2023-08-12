import json
import os
import shutil

from onecode import Env, Mode, Project

from onecode_st import CsvOutput
from tests.utils.flow_cli import _clean_flow, _generate_flow_name


def test_execute_csv_output():
    _, folder, flow_id = _generate_flow_name()
    tmp = _clean_flow(folder)
    folder_path = os.path.join(tmp, folder)
    data_path = os.path.join(folder_path, 'data')
    os.makedirs(data_path)
    os.environ[Env.ONECODE_PROJECT_DATA] = data_path
    Project().reset()
    Project().mode = Mode.EXECUTE
    Project().current_flow = flow_id

    widget = CsvOutput(
        key="CsvOutput",
        value="my_file.csv",
        tags=["CSV"]
    )

    assert widget() == os.path.join(data_path, 'outputs', 'my_file.csv')
    assert widget.key == "csvoutput"
    assert widget.label == "'''CsvOutput'''"
    assert widget._label == "CsvOutput"

    with open(os.path.join(data_path, 'outputs', flow_id, 'MANIFEST.txt'), 'r') as f:
        assert json.loads(f.read()) == {
            "key": "csvoutput",
            "label": "CsvOutput",
            "value": os.path.join(data_path, 'outputs', 'my_file.csv'),
            "tags": ["CSV"],
            "kind": "CsvOutput"
        }

    try:
        shutil.rmtree(folder_path)
    except Exception:
        pass
