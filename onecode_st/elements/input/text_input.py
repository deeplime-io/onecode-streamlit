# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import onecode

from ..input_streamlit_element import InputStreamlitElement


class TextInput(InputStreamlitElement, onecode.TextInput):
    def streamlit(
        self,
        id: str
    ) -> str:
        """
        Returns:
            The Streamlit code for a text input field (`st.text`).

        """
        val = f'"{self.value}"' if self.value is not None else "''"
        default = f'"{self.placeholder}"'
        multiline = self.multiline

        if multiline is False:
            widget = 'st.text_input'
            extra = f'key={id}'
        else:
            widget = 'st.text_area'
            extra = f'''height={"None" if multiline is True else multiline},
    key={id}'''

        return f"""
# Text {self.key}
{self.key} = {widget}(
    {self.label},
    {val},
    disabled={self.disabled},
    max_chars={self.max_chars},
    placeholder={default},
    {extra}
)

"""
