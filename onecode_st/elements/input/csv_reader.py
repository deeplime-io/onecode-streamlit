# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

from typing import List

import onecode

from ..input_streamlit_element import InputStreamlitElement


class CsvReader(InputStreamlitElement, onecode.CsvReader):
    @staticmethod
    def imports() -> List[str]:
        """
        Returns:
            Python import statements required by the Streamlit code.

        """
        return ["from pyarrow import csv as pacsv"]

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
# CsvReader {key}
{file_key} = st.file_uploader(
    f{label} + ': select CSV file',
    type=['csv'],
    disabled={self.disabled},
    key={id}
)
if {file_key} is not None:
    {key} = pacsv.read_csv({file_key}).to_pandas()
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
