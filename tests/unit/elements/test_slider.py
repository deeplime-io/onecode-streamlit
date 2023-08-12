from onecode import Mode, Project

from onecode_st import Slider


def test_execute_single_slider():
    Project().mode = Mode.EXECUTE

    widget = Slider(
        key="Slider",
        value=0.6,
        step=0.1
    )

    assert widget() == 0.6
    assert widget.key == "slider"
    assert widget.label == "'''Slider'''"
    assert widget._label == "Slider"


def test_extract_all_slider():
    Project().mode = Mode.EXTRACT_ALL

    widget = Slider(
        key="Slider",
        value=[0.5, 12.3],
        label="My Slider",
        optional="$x$",
        count=2,
        min=0.1,
        max=15.6,
        step=0.1
    )

    assert widget() == ('slider', {
        "key": "slider",
        "kind": "Slider",
        "value": [0.5, 12.3],
        "min": 0.1,
        "max": 15.6,
        "step": 0.1,
        "label": "My Slider",
        "disabled": '_DATA_["x"]',
        "optional": True,
        "count": "2"
    })
