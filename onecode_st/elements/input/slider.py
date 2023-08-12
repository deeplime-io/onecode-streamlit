# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import onecode

from ..input_streamlit_element import InputStreamlitElement


class Slider(InputStreamlitElement, onecode.Slider):
    def streamlit(
        self,
        id: str
    ) -> str:
        """
        Returns:
            The Streamlit code for a slider (`st.slider`).

        """
        return f"""
# Slider {self.key}
{self.key} = st.slider(
    {self.label},
    min_value={self.min},
    max_value={self.max},
    value={self.value},
    step={self.step},
    disabled={self.disabled},
    key={id}
)

"""
