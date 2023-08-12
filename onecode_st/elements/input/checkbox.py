# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import onecode

from ..input_streamlit_element import InputStreamlitElement


class Checkbox(InputStreamlitElement, onecode.Checkbox):
    def streamlit(
        self,
        id: str
    ) -> str:
        """
        Returns:
            The Streamlit code for a checkbox (`st.checkbox`).

        """
        return f"""
# Checkbox {self.key}
{self.key} = st.checkbox(
    {self.label},
    {self.value},
    disabled={self.disabled},
    key={id}
)

"""
