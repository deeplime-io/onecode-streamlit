from onecode import Mode, Project

from onecode_st import RadioButton


def test_execute_single_radio_button():
    Project().mode = Mode.EXECUTE

    widget = RadioButton(
        key="RadioButton",
        value="A",
        options=["A", "B"]
    )

    assert widget() == "A"
    assert widget.key == "radiobutton"
    assert widget.label == "'''RadioButton'''"
    assert widget._label == "RadioButton"


def test_extract_all_radio_button():
    Project().mode = Mode.EXTRACT_ALL

    widget = RadioButton(
        key="RadioButton",
        value=["A", "C"],
        label="My RadioButton",
        optional="$x$",
        count=2,
        options=["A", "B", "C"],
        horizontal=True
    )

    assert widget() == ('radiobutton', {
        "key": "radiobutton",
        "kind": "RadioButton",
        "value": ["A", "C"],
        "label": "'''My RadioButton'''",
        "disabled": '_DATA_["x"]',
        "optional": True,
        "count": "2",
        "options": ["A", "B", "C"],
        "horizontal": True
    })
