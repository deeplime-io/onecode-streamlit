# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import onecode

from ..output_streamlit_element import OutputStreamlitElement


class FileOutput(OutputStreamlitElement, onecode.FileOutput):
    @staticmethod
    def streamlit() -> str:
        """
        Returns:
            The Streamlit code to show the basic output file information as text.

        """
        return """
value = os.path.relpath(value)  # allows compat with Windows
if not os.path.exists(value) and not os.path.isfile(value):
    st.warning(f'Invalid file path: {{value}}')

else:
    st.subheader(f'{label} - {os.path.basename(value)}')
    st.info(f'''
File Info\n
- Path: {value}\n
- Size: {round(os.path.getsize(value) / 1e6, 4)} Mo
    ''')
"""
