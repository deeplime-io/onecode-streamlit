# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import onecode
import pydash

from ..input_streamlit_element import InputStreamlitElement


class RadioButton(InputStreamlitElement, onecode.RadioButton):
    def streamlit(
        self,
        id: str
    ) -> str:
        """
        Returns:
            The Streamlit code for a group of radio buttons (`st.radio`).

        """
        return f"""
# RadioButton {self.key}
{self.key} = st.radio(
    {self.label},
    options={self.options},
    index={pydash.find_index(self.options, lambda x: x == self.value)},
    disabled={self.disabled},
    horizontal={self.horizontal},
    key={id}
)

"""
