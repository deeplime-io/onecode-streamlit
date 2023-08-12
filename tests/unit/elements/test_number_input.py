from onecode import Mode, Project

from onecode_st import NumberInput


def test_execute_single_number_input():
    Project().mode = Mode.EXECUTE

    widget = NumberInput(
        key="NumberInput",
        value=5.1,
        min=5,
        max=6
    )

    assert widget() == 5.1
    assert widget.key == "numberinput"
    assert widget.label == "'''NumberInput'''"
    assert widget._label == "NumberInput"


def test_extract_all_number_input():
    Project().mode = Mode.EXTRACT_ALL

    widget = NumberInput(
        key="NumberInput",
        value=[0.5, 12.3],
        label="My NumberInput",
        optional="$x$",
        count=2,
        min=0.1,
        max=15.6,
        step=0.1
    )

    assert widget() == ('numberinput', {
        "key": "numberinput",
        "kind": "NumberInput",
        "value": [0.5, 12.3],
        "min": 0.1,
        "max": 15.6,
        "step": 0.1,
        "label": "My NumberInput",
        "disabled": '_DATA_["x"]',
        "optional": True,
        "count": "2"
    })
