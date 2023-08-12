# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

from typing import List

import onecode

from ..output_streamlit_element import OutputStreamlitElement


class PlotlyOutput(OutputStreamlitElement, onecode.PlotlyOutput):
    @staticmethod
    def imports() -> List[str]:
        """
        Returns:
            Python import statements required by the Streamlit code.

        """
        return ["import plotly"]

    @staticmethod
    def streamlit() -> str:
        """
        Returns:
            The Streamlit code to show a figure corresponding to the output Plotly file.

        """
        return """
value = os.path.relpath(value)  # allows compat with Windows
if not os.path.exists(value) and not os.path.isfile(value):
    st.warning(f'Invalid file path: {{value}}')

else:
    fig = plotly.io.read_json(value)

    st.subheader(f'{label} - {os.path.basename(value)}')
    st.plotly_chart(fig)

"""
