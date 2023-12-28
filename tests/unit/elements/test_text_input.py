from onecode import Mode, Project

from onecode_st import TextInput


def test_execute_single_text_input():
    Project().mode = Mode.EXECUTE

    widget = TextInput(
        key="TextInput",
        value="My Text"
    )

    assert widget() == "My Text"
    assert widget.key == "textinput"
    assert widget.label == "'''TextInput'''"
    assert widget._label == "TextInput"


def test_extract_all_text_input():
    Project().mode = Mode.EXTRACT_ALL

    widget = TextInput(
        key="TextInput",
        value=["OneCode", "rocks!"],
        label="My TextInput",
        optional="$x$",
        count=2,
        max_chars=500,
        placeholder="My Placeholder"
    )

    assert widget() == ('textinput', {
        "key": "textinput",
        "kind": "TextInput",
        "value": ["OneCode", "rocks!"],
        "label": "'''My TextInput'''",
        "disabled": '_DATA_["x"]',
        "optional": True,
        "count": "2",
        "max_chars": 500,
        "placeholder": "My Placeholder",
        "multiline": False
    })
