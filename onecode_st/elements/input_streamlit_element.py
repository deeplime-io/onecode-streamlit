# SPDX-FileCopyrightText: 2023 DeepLime <contact@deeplime.io>
# SPDX-License-Identifier: MIT

from abc import abstractmethod
from typing import List

from ..base.enums import Keyword
from ..utils.format import convert_expr, indent_block


class InputStreamlitElement():
    """
    `InputElement` mixin for Streamlit mode. By inheriting it, it is mandatory to define:
    - [`streamlit()`][onecode_st.InputStreamlitElement.streamlit]: method returning the Streamlit
        code to be generated.

    `imports()` and `init()` may be reimplemented if required by the element.

    !!! warning
        When inheriting, you must order this mixin first:
        ```py
        class CsvReader(InputStreamlitElement, onecode.CsvReader):  # correct
        class CsvReader(onecode.CsvReader, InputStreamlitElement):  # wrong!
        ```
        Otherwise the `disabled` and `count` properties will not overwrite the default OneCode ones.

    Attributes overwritten:
        label: Human readable name ready for Streamlit usage.
        count: Number of occurence of the element as string ready for Streamlit usage.
        disabled: Disabled status as string ready for Streamlit.

    """

    @property
    def label(self) -> str:
        """
        Get the label with triple-quotes and escaped to handle human-readable string.
        It is primarly meant to be used as-is in the Streamlit generated code for the
        `label` parameter.
        See [`streamlit()`][onecode.InputElement.streamlit] for more information.

        Returns:
            The string to be used in `streamlit()` for the `label` parameter.

        !!! example
            ```py
            from onecode import Mode, Project, slider

            Project().mode = Mode.CONSOLE
            x = slider("Hello l'aspirateur!", None, optional=True)

            assert x.label == "'''Hello l\\'aspirateur!'''"
            ```

        """
        name = self._label.replace("'", "\\'")
        return f"'''{name}'''"

    @property
    def count(self) -> str:
        """
        Returns:
            The number of occurence of the element as a string for Streamlit.

        """
        return str(self._count) if isinstance(self._count, int) else convert_expr(self._count)

    @property
    def disabled(self) -> str:
        """
        Returns:
            Whether the element should be disabled as string for Streamlit.

        """
        return 'False' if self._disabled is False \
            else f'_optional_{self.key}' if self._disabled is True \
            else convert_expr(self._disabled)

    @staticmethod
    def imports() -> List[str]:
        """
        Re-implement this function in case your Streamlit code requires specific Python package
        import. This function should return a list of import statement as string.

        Note that the following packages are already imported (not needed to return them in that
        list): `os`, `json`, `uuid`, `pydash`, `streamlit as st`.

        !!! example
            ```py
            @staticmethod
            def imports() -> List[str]:
                return [
                    "import numpy as np",
                    "import plotly"
                ]
            ```

        """
        return []

    @staticmethod
    def init() -> str:
        """
        Re-implement this function in case your Streamlit code requires specific initialization
        statements. Note that all variables starting with a `_` are reserved.

        !!! example
            ```py
            @staticmethod
            def init() -> str:
                return '''
                    def x(angle):
                        return np.deg2rad(angle%360)
                '''
            ```

        """
        return ''

    @abstractmethod
    def streamlit(
        self,
        id: str
    ) -> str:   # pragma: no cover
        """
        You must re-implement this function to return the expected Streamlit block code for
        this element. This block code will be written out to the generated Streamlit App code.

        Typical attributes that will be useful:
        - `label`: can be directly piped to the Streamlit widget `label` parameter. This attribute
            has been automatically setup for you to use and will properly escape the potential
            troublesome characters.

        - `disabled`: can be directly piped to the Streamlit `disabled` widget parameters. This
            attribute has been automatically setup for you to use and will properly take the
            `optional` argument into account regardless of `optional` being an expression, a
            boolean or None. Therefore, do not use `optional` or `hide_when_disabled`, use
            `disabled` directly.

        - `key`: it must be used as the variable name for the Streamlit widget.

        - all other attributes that are specific to your widget, e.g. `min`, `max`, `step` for
            a Slider, etc.

        Args:
            id: Must be used as the `id` parameter of the Streamlit widget. This variable is
                automatically setup to take uniqueness wrt `count`.

        Returns:
            The Streamlit block code to be output in the generated Streamlit App code.

        !!! example
            ```py
                def streamlit(
                    self,
                    id: str
                ) -> str:

                    return f'''
            # Slider
            {self.key} = st.slider(
                {self.label},
                min_value={self.min},
                max_value={self.max},
                value={self.value},
                step={self.step},
                disabled={self.disabled},
                key={id}
            )

            '''
            ```

        !!! tip
            Remember: no need to use `optional`, `hide_when_disabled` and `count`, they are
            already automatically taken into account to make your life easier. Use `disabled`,
            `label`, `key` and `id`

        """
        pass

    def _build_streamlit(self) -> str:
        """
        Function called when Project mode is Streamlit mode. The Streamlit block code will be
        prepared using the element parameters (such as `count`, `optional`, `hide_when_disabled`,
        etc.) as well as the block code returned by the
        [`streamlit()`][onecode.InputElement.streamlit] function. This function makes it easy to
        extend the `InputElement` without worrying about the `count`, `optional` and
        `hide_when_disabled` attributes.

        Returns:
            The full block code generated by this `InputElement` to be written out to the generated
            Streamlit app code.

        """
        code_gen = ''

        if self.optional and self.disabled == f'_optional_{self.key}':
            code_gen += f"""
_optional_{self.key} = not st.checkbox(
    'Enable ' + {self.label},
    value=True,
    key='_optional_{self.key}'
)
"""

        if self.count is None:
            if self.optional and self.hide_when_disabled:
                code_gen += f"if not ({self.disabled}):"
                code_gen += indent_block(self.streamlit(f"'{self.key}'"))
            else:
                code_gen += self.streamlit(f"'{self.key}'")

            code_gen += f"""
{Keyword.DATA}['{self.key}'] = {self.key} if not ({self.disabled}) else None

"""

        else:
            if self.optional and self.hide_when_disabled:
                inner_code = f"if not ({self.disabled}):"
                inner_code += indent_block(self.streamlit(f"{'f'}'{self.key}_{{_c}}'"), indent=8)
            else:
                inner_code = indent_block(self.streamlit(f"{'f'}'{self.key}_{{_c}}'"))

            code_gen += f"""
{Keyword.DATA}['{self.key}'] = []
for _c in range(int({self.count})):
    {inner_code}
    {Keyword.DATA}['{self.key}'].append({self.key} if not ({self.disabled}) else None)
"""
        return code_gen
