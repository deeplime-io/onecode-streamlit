# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

from typing import List

import onecode

from ..output_streamlit_element import OutputStreamlitElement


class CsvOutput(OutputStreamlitElement, onecode.FileOutput):
    @staticmethod
    def imports() -> List[str]:
        """
        Returns:
            Python import statements required by the Streamlit code.

        """
        return ["from pyarrow import csv as pacsv"]

    @staticmethod
    def streamlit() -> str:
        """
        Returns:
            The Streamlit code to show a table corresponding to the output CSV file.

        """
        return """
value = os.path.relpath(value)  # allows compat with Windows
if not os.path.exists(value) and not os.path.isfile(value):
    st.warning(f'Invalid file path: {{value}}')

else:
    df = pacsv.read_csv(value).to_pandas()
    file_size = df.size // 1e6
    if file_size > 200:
        st.write(f'File too big ({file_size} Mo), data has been truncated to the first 10k rows')
        df = df[:10000]

    st.subheader(f'{label} - {os.path.basename(value)}')
    st.dataframe(df)

"""
