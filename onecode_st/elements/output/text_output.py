# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import onecode

from ..output_streamlit_element import OutputStreamlitElement


class TextOutput(OutputStreamlitElement, onecode.FileOutput):
    @staticmethod
    def streamlit() -> str:
        """
        Returns:
            The Streamlit code to preview text of a file.

        """
        return """
value = os.path.relpath(value)  # allows compat with Windows
if not os.path.exists(value) and not os.path.isfile(value):
    st.warning(f'Invalid file path: {{value}}')

else:
    with open(value, 'r') as f:
        txt = f.read()

    if len(txt) > truncate_at:
        txt = txt[:truncate_at]
        st.warning(f'File trucated at {truncate_at} characters')

    st.subheader(f'{label} - {os.path.basename(value)}')
    st.code(txt)
"""
