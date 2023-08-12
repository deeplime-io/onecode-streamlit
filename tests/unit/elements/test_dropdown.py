from onecode import Mode, Project

from onecode_st import Dropdown


def test_execute_single_dropdown_single_choice():
    Project().mode = Mode.EXECUTE

    widget = Dropdown(
        key="Dropdown",
        value="A",
        options=["A", "B"]
    )

    assert widget() == "A"
    assert widget.key == "dropdown"
    assert widget.label == "'''Dropdown'''"
    assert widget._label == "Dropdown"


def test_extract_all_dropdown():
    Project().mode = Mode.EXTRACT_ALL

    widget = Dropdown(
        key="Dropdown",
        value=[["A", "B"], ["C"]],
        label="My Dropdown",
        optional="$x$",
        count=2,
        multiple=True,
        options=["A", "B", "C"]
    )

    assert widget() == ('dropdown', {
        "key": "dropdown",
        "kind": "Dropdown",
        "value": [["A", "B"], ["C"]],
        "label": "My Dropdown",
        "disabled": '_DATA_["x"]',
        "optional": True,
        "count": "2",
        "multiple": True,
        "options": ["A", "B", "C"]
    })
