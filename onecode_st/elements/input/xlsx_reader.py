import os
from typing import Any, List, Optional, Union

import onecode
import pandas as pd

from ..input_streamlit_element import InputStreamlitElement


class XlsxReader(InputStreamlitElement, onecode.FileInput):
    def __init__(
        self,
        key: str,
        value: Optional[Union[str, List[str]]],
        label: Optional[str] = None,
        optional: Union[bool, str] = False,
        hide_when_disabled: bool = False,
        tags: Optional[List[str]] = None,
        **kwargs: Any
    ):
        """
        A XLSX-file reader returning a Pandas DataFrame and displayed as a table in Streamlit.

        Args:
            key: ID of the element. It must be unique as it is the key used to store data in
                Project(), otherwise it will lead to conflicts at runtime in both execution and
                Streamlit modes. The key will be transformed into snake case and slugified to avoid
                any special character or whitespace. Note that an ID cannot start with `_`. Try to
                choose a key that is meaningful for your context (see examples projects).
            value: Path to the CSV file. CSV file must exists, even for the Streamlit mode.
            label: Label to display on top of the table.
            optional: Specify whether the value may be None. `optional` can either be a fixed
                boolean (`False` or `True`) or a conditional expression dependent of other elements.
            hide_when_disabled: If element is optional, set it to True to hide it from the
                interface, otherwise it will be shown disabled.
            tags: Optional meta-data information about the expected file. This information is only
                used by the `Mode.EXTRACT_ALL` when dumping attributes to JSON.
            **kwargs: Extra user meta-data to attach to the element. Argument names cannot overwrite
                existing attributes or methods name such as `streamlit`, `_value`, etc.

        Raises:
            ValueError: if the `key` is empty or starts with `_`.
            AttributeError: if one the `kwargs` conflicts with an existing attribute or method.

        !!! example
            ```py
            import pandas as pd
            from onecode import xlsx_reader, Mode, Project

            Project().mode = Mode.EXECUTE
            widget = xlsx_reader(
                key="XlsxReader",
                value="/path/to/file.xlsx",
                label="My Excel Reader",
                tags=['XLSX']
            )

            pd.testing.assert_frame_equal(widget, pd.read_excel("/path/to/file.xlsx"))
            ```

        """
        super().__init__(
            key,
            value,
            label,
            None,  # count
            optional,
            hide_when_disabled,
            tags=tags,
            **kwargs
        )

    @staticmethod
    def imports() -> List[str]:
        """
        Returns:
            Python import statements required by the Streamlit code.

        """
        return ["import pandas as pd"]

    @property
    def _value_type(self) -> type:
        """
        Get the CsvReader value type: Pandas DataFrame `pd.DataFrame`.

        """
        return pd.DataFrame

    @property
    def value(self) -> Optional[pd.DataFrame]:
        """
        Returns:
            The Pandas DataFrame loaded from the provided file path, otherwise None if the
            file does not exists.

        """
        if self._value is not None:
            filepath = onecode.Project().get_input_path(self._value)
            return pd.read_excel(filepath) if os.path.exists(filepath) else None

        return None

    def _validate(
        self,
        value: pd.DataFrame
    ) -> None:
        """
        Raises:
            ValueError: if the DataFrame is empty.

        """
        if value.empty:
            raise ValueError(f"[{self.key}] Empty dataframe")

    def streamlit(
        self,
        id: str
    ) -> str:
        """
        Returns:
            The Streamlit code for a Pandas DataFrame (`st.dataframe`).

        !!! note
            A file selector (`st.file_uploader`) is provided on top of the table.

        """
        label = self.label
        key = self.key

        file_key = f'_file_{key}'

        return f"""
# XlsxReader {key}
{file_key} = st.file_uploader(
    f{label} + ': select CSV file',
    type=['xlsx'],
    disabled={self.disabled},
    key={id}
)
if {file_key} is not None:
    {key} = pd.read_excel({file_key})
    if {file_key}.size // 1e6 > 200:
        st.write(
            f'File too big ({{{file_key}.size // 1e6}} Mo)'
            ', data has been truncated to the first 10k rows'
        )
        {key} = {key}[:10000]
    st.dataframe({key})
else:
    {key} = None

"""
