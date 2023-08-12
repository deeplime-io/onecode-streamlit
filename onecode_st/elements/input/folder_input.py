# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

from typing import List

import onecode

from ..input_streamlit_element import InputStreamlitElement


class FolderInput(InputStreamlitElement, onecode.FolderInput):
    @staticmethod
    def imports() -> List[str]:
        """
        Returns:
            Python import statements required by the Streamlit code.

        """
        return [
            "import tkinter as tk",
            "from tkinter import filedialog"
        ]

    @staticmethod
    def init() -> str:
        """
        Returns:
            The Python statements that must be initialized before being used by the Streamlit code.

        """
        return """_root = tk.Tk()
_root.withdraw()
_root.wm_attributes('-topmost', 1)
"""

    def streamlit(
        self,
        id: str
    ) -> str:
        """
        Returns:
            The Streamlit code for a folder selection (`st.text_input` for the path combined with a
            `tkinter.filedialog.askdirectory` for the file selection).

        """
        label = self.label
        key = self.key

        button_key = f'_button_{key}'
        file_key = f'_file_{key}'
        file_id = f'"_file_" + {id}'

        # if there is a count, it's too complicated to set defaults
        # => so default to None
        if self.value is not None and self.count is None:
            value = f"'''{self.value}'''"
        else:
            value = 'None'

        return f"""
# FolderInput {key}
left, right = st.columns([3, 1])
with right:
    {button_key} = right.button('Select folder', disabled={self.disabled}, key="button_" + {id})

{file_key} = st.session_state[{file_id}] if {file_id} in st.session_state else {value}
if {button_key}:
    {file_key} = filedialog.askdirectory(
        master=_root,
        title='Select folder'
    )
    st.session_state[{file_id}] = {file_key}

with left:
    {key} = left.text_input({label}, {file_key}, disabled={self.disabled}, key={id})
"""
