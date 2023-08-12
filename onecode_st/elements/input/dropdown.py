# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

import onecode

from ...utils.format import convert_expr
from ..input_streamlit_element import InputStreamlitElement


class Dropdown(InputStreamlitElement, onecode.Dropdown):
    def streamlit(
        self,
        id: str
    ) -> str:
        """
        Returns:
            The Streamlit code for a dropdown menu (`st.multiselect` | `selectbox`).

        """
        label = self.label
        key = self.key
        options_key = f'_options_{key}'
        default_key = f'_default_{key}'

        if isinstance(self.options, str):
            options = convert_expr(self.options)
        else:
            options = self.options

        if self.multiple:
            widget = 'st.multiselect'
            default_param = 'default'
            val = f"['''{self.value}''']" if isinstance(self.value, str) else self.value
        else:
            widget = 'st.selectbox'
            default_param = 'index'
            val = f"'''{self.value}'''" if isinstance(self.value, str) else self.value

        return f"""
try:
    {options_key} = {options}
except:
    {options_key} = []

if {self.multiple}: # is dropdown multiple?
    {default_key} = [v for v in {val} if v in {options_key}]
else:
    {default_key} = pydash.find_index({options_key}, lambda x: x == {val})
    {default_key} = {default_key} if {default_key} >= 0 else 0

# Dropdown {key}
{key} = {widget}(
    {label},
    {default_param}={default_key},
    options={options_key},
    disabled={self.disabled},
    key={id}
)

"""
