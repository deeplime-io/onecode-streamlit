from onecode import Mode, Project

from onecode_st import Checkbox


def test_execute_single_checkbox():
    Project().mode = Mode.EXECUTE

    widget = Checkbox(
        key="Checkbox",
        value=True
    )

    assert widget() is True
    assert widget.key == "checkbox"
    assert widget.label == "'''Checkbox'''"
    assert widget._label == "Checkbox"


def test_extract_all_checkbox():
    Project().mode = Mode.EXTRACT_ALL

    widget = Checkbox(
        key="Checkbox",
        value=[True, True],
        label="My Checkbox",
        optional="$x$",
        count=2
    )

    assert widget() == ('checkbox', {
        "key": "checkbox",
        "kind": "Checkbox",
        "value": [True, True],
        "label": "'''My Checkbox'''",
        "disabled": '_DATA_["x"]',
        "optional": True,
        "count": "2"
    })
