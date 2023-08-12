# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import onecode

from ..input_streamlit_element import InputStreamlitElement


class NumberInput(InputStreamlitElement, onecode.NumberInput):
    def streamlit(
        self,
        id: str
    ) -> str:
        """
        Returns:
            The Streamlit code for a number input field (`st.number_input`).

        """
        return f"""
# NumberInput {self.key}
{self.key} = st.number_input(
    {self.label},
    min_value={self.min},
    max_value={self.max},
    value={self.value},
    step={self.step},
    disabled={self.disabled},
    key={id}
)

"""
